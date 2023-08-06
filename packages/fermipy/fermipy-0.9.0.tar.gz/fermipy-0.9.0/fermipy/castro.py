"""
Utilities for dealing with 'castro data', i.e., 2D table of likelihood values.

For example as a function of Energy and Energy Flux.
"""

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import copy
import logging
import os

import numpy as np
from scipy.interpolate import UnivariateSpline, splrep, splev
import scipy.optimize as opt
import scipy.special as spf
from scipy.integrate import quad
import scipy

import astropy.io.fits as pf
from astropy.coordinates import SkyCoord
from astropy.table import Table, Column

import fermipy.utils as utils
import fermipy.roi_model as roi_model
import fermipy.sourcefind as sourcefind

from fermipy.wcs_utils import wcs_add_energy_axis
from fermipy.fits_utils import read_energy_bounds, read_spectral_data
from fermipy.skymap import read_map_from_fits, Map
from fermipy.logger import Logger
from fermipy.logger import logLevel
from fermipy.sourcefind import find_peaks, refine_peak
from fermipy.spectrum import SpectralFunction

# Some useful functions

FluxTypes = ['NORM','FLUX','EFLUX','NPRED','DFDE','EDFDE']

PAR_NAMES = {"PowerLaw":["Prefactor","Index"],
             "LogParabola":["norm","alpha","beta"],
             "PLExpCutoff":["Prefactor","Index1","Cutoff"]}

        
class Interpolator(object):
    """ Helper class for interpolating a 1-D function from a
    set of tabulated values.  

    Safely deals with overflows and underflows
    """
    def __init__(self,x,y):
        """ C'tor, take input array of x and y value         
        """
        
        x = np.squeeze(np.array(x,ndmin=1))
        y = np.squeeze(np.array(y,ndmin=1))
        
        msk = np.isfinite(y)
        x = x[msk]
        y = y[msk]

        self._x = x
        self._y = y
        self._xmin = x[0]
        self._xmax = x[-1]
        self._ymin = y[0]
        self._ymax = y[-1]
        self._dydx_lo = (y[1]-y[0])/(x[1]-x[0])
        self._dydx_hi = (y[-1]-y[-2])/(x[-1]-x[-2])

        self._fn = UnivariateSpline(x,y,s=0,k=1)        
        self._sp = splrep(x,y,k=1,s=0)
        
    @property
    def xmin(self):
        """ return the minimum value over which the spline is defined
        """
        return self._xmin

    @property
    def xmax(self):
        """ return the maximum value over which the spline is defined
        """       
        return self._xmax

    @property
    def x(self):
        """ return the x values used to construct the split
        """       
        return self._x

    @property
    def y(self):
        """ return the y values used to construct the split
        """         
        return self._y

    def derivative(self,x,der=1):
        """ return the derivative a an array of input values

        x   : the inputs        
        der : the order of derivative         
        """ 
        return splev(x,self._sp,der=der)

    def __call__(self,x):
        """ Return the interpolated values for an array of inputs

        x : the inputs        

        Note that if any x value is outside the interpolation ranges
        this will return a linear extrapolation based on the slope
        at the endpoint
        """         
        x = np.array(x,ndmin=1)

        below_bounds = x < self._xmin
        above_bounds = x > self._xmax
        
        dxhi = np.array(x-self._xmax)
        dxlo = np.array(x-self._xmin)

        # UnivariateSpline will only accept 1-D arrays so this
        # passes a flattened version of the array.
        y = self._fn(x.ravel())
        y.resize(x.shape)
            
        y[above_bounds] = (self._ymax + dxhi[above_bounds]*self._dydx_hi)
        y[below_bounds] = (self._ymin + dxlo[below_bounds]*self._dydx_lo)
        return y
  

class LnLFn(object):
    """
    Helper class for interpolating a 1-D log-likelihood function from a
    set of tabulated values.  
    """
    def __init__(self,x,y,norm_type=0):
        """ C'tor, take input array of x and y value   

        norm_type :  code specifying the quantity used for the flux 
           0: Normalization w.r.t. to test source
           1: Flux of the test source ( ph cm^-2 s^-1 )
           2: Energy Flux of the test source ( MeV cm^-2 s^-1 )
           3: Number of predicted photons
           4: Differential flux of the test source ( ph cm^-2 s^-1 MeV^-1 )
           5: Differential energy flux of the test source ( MeV cm^-2 s^-1 MeV^-1 )           
        """
        self._interp = Interpolator(x,y)
        self._mle = None
        self._norm_type = norm_type

    @property
    def interp(self):
        """ return the underlying Interpolator object
        """ 
        return self._interp

    @property
    def norm_type(self):
        """ return a code specifying the quantity used for the flux 

           0: Normalization w.r.t. to test source
           1: Flux of the test source ( ph cm^-2 s^-1 )
           2: Energy Flux of the test source ( MeV cm^-2 s^-1 )
           3: Number of predicted photons
           4: Differential flux of the test source ( ph cm^-2 s^-1 MeV^-1 )
           5: Differential energy flux of the test source ( MeV cm^-2 s^-1 MeV^-1 )           
        """
        return self._norm_type        

    def _compute_mle(self):
        """ compute the maximum likelihood estimate, using the scipy.optimize.brentq method
        """
        if self._interp.y[0] == np.min(self._interp.y):
            self._mle = self._interp.x[0]
        else:
            ix0 = max(np.argmin(self._interp.y)-4,0)
            ix1 = min(np.argmin(self._interp.y)+4,len(self._interp.x)-1)            

            while np.sign(self._interp.derivative(self._interp.x[ix0])) == np.sign(self._interp.derivative(self._interp.x[ix1])):
                ix0 += 1
            
            self._mle = scipy.optimize.brentq(self._interp.derivative,
                                              self._interp.x[ix0], self._interp.x[ix1],
                                              xtol=1e-10*np.median(self._interp.x))    

    def mle(self):
        """ return the maximum likelihood estimate 

        This will return the cached value, if it exists
        """
        if self._mle is None:
            self._compute_mle()
        
        return self._mle
        

    def fn_mle(self):
        """ return the function value at the maximum likelihood estimate """
        return self._interp(self.mle())

    def TS(self):
        """ return the Test Statistic """
        return 2. * (self._interp(0.) - self._interp(self.mle()))

    
    def getLimit(self,alpha,upper=True):
        """ Evaluate the limits corresponding to a C.L. of (1-alpha)%.

        Parameters
        ----------
        alpha :  limit confidence level.
        upper :  upper or lower limits.
        """
        dlnl = utils.cl_to_dlnl(1.0-alpha)
        lnl_max = self.fn_mle()

        # This ultra-safe code to find an absolute maximum
        #fmax = self.fn_mle()
        #m = (fmax-self.interp.y > 0.1+dlnl) & (self.interp.x>self._mle)

        #if sum(m) == 0:
        #    xmax = self.interp.x[-1]*10
        #else:
        #    xmax = self.interp.x[m][0]

        # Matt has found that this is use an interpolator than an actual root-finder to 
        # find the root probably b/c of python overhead       
        #rf = lambda x: self._interp(x)+dlnl-lnl_max
        if upper:
            x = np.linspace(self._mle,self._interp.xmax,100)  
            #return opt.brentq(rf,self._mle,self._interp.xmax,xtol=1e-10*np.abs(self._mle))
        else:
            x = np.linspace(self._mle,self._interp.xmin,100) 
            #return opt.brentq(rf,self._interp.xmin,self._mle,xtol=1e-10*np.abs(self._mle))
            
        retVal =  np.interp(dlnl,lnl_max-self.interp(x),x)
        return retVal


    def getInterval(self,alpha):
        """ Evaluate the interval corresponding to a C.L. of (1-alpha)%.

        Parameters
        ----------
        alpha : limit confidence level.
        """
        lo_lim = self.getLimit(alpha,upper=False)
        hi_lim = self.getLimit(alpha,upper=True)
        return (lo_err,hi_err)


class SpecData(object):
    """ This class wraps spectral data, e.g., energy bin definitions,
    flux values and number of predicted photons
    """
    def __init__(self,emin,emax,dfde,flux,eflux,npred):
        """

        Parameters
        ----------

        emin :  `~numpy.ndarray`
           Array of lower bin edges.

        emax :  `~numpy.ndarray`
           Array of upper bin edges.
        
        """
        self._ebins = np.append(emin,emax[-1])
        self._emin = emin
        self._emax = emax
        self._log_ebins = np.log10(self._ebins)
        self._evals = np.sqrt(self.emin*self.emax)
        self._bin_widths = self._ebins[1:] - self._ebins[0:-1]
        self._dfde = dfde
        self._flux = flux
        self._eflux = eflux
        self._npred = npred
        self._ne = len(self.ebins)-1


    @property
    def log_ebins(self):
        """ return the log10 of the energy bin edges
        """ 
        return self._log_ebins

    @property
    def ebins(self):
        """ return the energy bin edges
        """
        return self._ebins

    @property
    def emin(self):
        """ return the lower energy bin edges
        """
        return self._emin

    @property
    def emax(self):
        """ return the lower energy bin edges
        """
        return self._emax
    
    @property
    def bin_widths(self):
        """ return the energy bin widths
        """
        return self._bin_widths

    @property
    def evals(self):
        """ return the energy centers
        """
        return self._evals

    @property
    def dfde(self):
        """ return the differential flux values
        """
        return self._dfde

    @property
    def eflux(self):
        """ return the energy flux values
        """
        return self._eflux

    @property
    def npred(self):
        """ return the number of predicted events
        """
        return self._npred

    @property
    def nE(self):
        """ return the number of energy bins
        """
        return self._ne


class CastroData_Base(object):
    """This class wraps the data needed to make a "Castro" plot,
    namely the log-likelihood as a function of normalization.

    In this case the x-axes and y-axes are generic
    Sub-classes can implement particul axes choices (e.g., EFlux v. Energy)
    """ 
    def __init__(self,norm_vals,nll_vals,norm_type):
        """ C'tor

        Parameters
        ----------
        norm_vals : `~numpy.ndarray`        
           The normalization values ( N X M array, 
           where N is the number for bins and M
           number of sampled values for each bin )
           
        nll_vals : `~numpy.ndarray`  
           The log-likelihood values ( N X M array, 
           where N is the number for bins and M
           number of sampled values for each bin )
           
        norm_type : str
           String specifying the quantity used for the normalization, 
           value depend on the sub-class details
        """
        self._norm_vals = norm_vals
        self._nll_vals = nll_vals
        self._loglikes = []        
        self._nll_null = 0.0
        self._norm_type = norm_type
        self._nx = self._norm_vals.shape[0]
        self._ny = self._norm_vals.shape[1]

        for i,(normv,nllv) in enumerate(zip(self._norm_vals,self._nll_vals)):            
            nllfunc = LnLFn(normv,nllv,self._norm_type)
            self._nll_null += self._nll_vals[i][0]
            self._loglikes.append(nllfunc)

    @property
    def nx(self):
        """ Return the number of profiles """
        return self._nx
    
    @property
    def ny(self):
        """ Return the number of profiles """
        return self._ny

    @property
    def norm_type(self):
        """ Return the normalization type flag """ 
        return self._norm_type

    @property
    def nll_null(self):
        """ Return the negative log-likelihood for the null-hypothesis """ 
        return self._nll_null

 
    def __getitem__(self,i):
        """ return the LnLFn object for the ith energy bin
        """
        return self._loglikes[i]

    def __call__(self,x):
        """Return the negative log-likelihood for an array of values,
        summed over the energy bins

        Parameters
        ----------
        x  : `~numpy.ndarray`  
           Array of N x M values

        Returns
        -------
        nll_val : `~numpy.ndarray`          
           Array of negative log-likelihood values.
        """
        nll_val = 0.
        # crude hack to force the fitter away from unphysical values
        if ( x < 0 ).any():
            return 1000.
        
        for i,xv in enumerate(x):
            nll_val += self._loglikes[i].interp(xv)
            
        return nll_val
        
    def derivative(self,x,der=1):
        """Return the derivate of the log-like summed over the energy
        bins

        Parameters
        ----------
        x   : `~numpy.ndarray`  
           Array of N x M values
           
        der : int
           Order of the derivate

        Returns
        -------
        der_val : `~numpy.ndarray`  
           Array of negative log-likelihood values.
        """
        der_val = 0.
        for i,xv in enumerate(x):
            der_val += self._loglikes[i].interp.derivative(xv,der=der)
        return der_val       

    def mles(self):
        """ return the maximum likelihood estimates for each of the energy bins
        """
        mle_vals = np.ndarray((self._nx))
        
        for i in range(self._nx):
            mle_vals[i] = self._loglikes[i].mle()
        return mle_vals

    def fn_mles(self):
        """ returns the summed likelihood at the maximum likelihood estimate

        Note that simply sums the maximum likelihood values at each bin, and 
        does not impose any sort of constrain between bins
        """
        mle_vals = self.mles()
        return self(mle_vals)

    def ts_vals(self):
        """ returns test statistic values for each energy bin
        """ 
        ts_vals = np.ndarray((self._nx))
        for i in range(self._nx):
            ts_vals[i] = self._loglikes[i].TS()
            pass
        return ts_vals 
    
    def getLimits(self,alpha,upper=True):
        """ Evaluate the limits corresponding to a C.L. of (1-alpha)%.

        Parameters
        ----------
        alpha :  limit confidence level.
        upper :  upper or lower limits.

        returns an array of values, one for each energy bin
        """
        limit_vals = np.ndarray((self._nx))
        
        for i in range(self._nx):
            limit_vals[i] = self._loglikes[i].getLimit(alpha,upper)
            pass
        return limit_vals
    
    def fitNormalization(self,specVals,xlims):
        """Fit the normalization given a set of spectral values that
        define a spectral shape

        This version is faster, and solves for the root of the derivatvie

        Parameters
        ----------
        specVals :  an array of (nebin values that define a spectral shape
        xlims    :  fit limits     

        returns the best-fit normalization value
        """
        fDeriv = lambda x : self.derivative(specVals*x)        
        try:
            result = scipy.optimize.brentq(fDeriv,xlims[0],xlims[1])
        except:
            if self.__call__(specVals*xlims[0]) < self.__call__(specVals*xlims[1]):
                return xlims[0]
            else:
                return xlims[1]
        return result
       
    def fitNorm_v2(self,specVals):
        """ Fit the normalization given a set of spectral values that define a spectral shape

        This version uses scipy.optimize.fmin
        
        Parameters
        ----------
        specVals :  an array of (nebin values that define a spectral shape
        xlims    :  fit limits     

        returns the best-fit normalization value
        """
        fToMin = lambda x : self.__call__(specVals*x)
        result = scipy.optimize.fmin(fToMin,0.,disp=False,xtol=1e-6)   
        return result
       
    def fit_spectrum(self,specFunc,initPars):
        """ Fit for the free parameters of a spectral function
        
        Parameters
        ----------
        specFunc :  The Spectral Function
        initPars :  The initial values of the parameters     


        Returns
        -------
        result   : tuple
           The output of scipy.optimize.fmin
        spec_out : `~numpy.ndarray`
           The best-fit spectral values
        TS_spec  : float
           The TS of the best-fit spectrum
        """

        def fToMin(x):
            return self.__call__(specFunc(x))
                
        result = scipy.optimize.fmin(fToMin,initPars,disp=False,xtol=1e-6)   
        spec_out = specFunc(result)
        TS_spec = self.TS_spectrum(spec_out)
        return result,spec_out,TS_spec
        
    def TS_spectrum(self,spec_vals):
        """ Calculate and the TS for a given set of spectral values
        """
        
        return 2. * (self._nll_null - self.__call__(spec_vals))


    @staticmethod
    def stack_nll(shape,components,weights=None):
        """
        """
        n_bins = shape[0]
        n_vals = shape[1]
   
        if weights is None:
            weights = np.ones((len(components)))

        norm_vals = np.zeros(shape)
        nll_vals = np.zeros(shape)
        for i in range(n_bins):
            norm_mins = np.array( [c._norm_vals[i][1] for c in components] )
            norm_maxs = np.array( [c._norm_vals[i][-1] for c in components] )
            log_norm_min = np.log10(norm_mins.min())
            log_norm_max = np.log10(norm_maxs.max())
            norm_vals[i][1:] = np.logspace(log_norm_min,log_norm_max,n_vals-1)
            pass
 
        for c,w in zip(components,weights):
            nll_vals += w*c(norm_vals)
            
        return norm_vals,nll_vals


class CastroData(CastroData_Base):
    """ This class wraps the data needed to make a "Castro" plot,
    namely the log-likelihood as a function of normalization for a
    series of energy bins.
    """
    def __init__(self,norm_vals,nll_vals,specData,norm_type):
        """ C'tor

        Parameters
        ----------
        norm_vals : `~numpy.ndarray`        
           The normalization values ( nEBins X N array, where N is the
           number of sampled values for each bin )
           
        nll_vals : `~numpy.ndarray`  
           The log-likelihood values ( nEBins X N array, where N is
           the number of sampled values for each bin )
           
        specData : `~fermipy.sed.SpecData`
           The specData object
           
        norm_type : str
           String specifying the quantity used for the normalization:
            NORM: Normalization w.r.t. to test source
            FLUX: Flux of the test source ( ph cm^-2 s^-1 )
            EFLUX: Energy Flux of the test source ( MeV cm^-2 s^-1 )
            NPRED: Number of predicted photons
            DFDE: Differential flux of the test source ( ph cm^-2 s^-1 MeV^-1 )
            E2DFDE: Differential energy flux of the test source ( MeV cm^-2 s^-1 MeV^-1 )           
        """
        super(CastroData,self).__init__(norm_vals,nll_vals,norm_type)
        self._specData = specData
 
    @property
    def nE(self):
        return self._nx

    @property
    def specData(self):
        """ Return the Spectral Data object """
        return self._specData

    @staticmethod
    def create_from_fits(fitsfile,norm_type='EFLUX',
                         hdu_scan="SCANDATA",
                         hdu_energies="EBOUNDS",
                         irow = None):

        if irow:
            tab_s = Table.read(fitsfile,hdu=hdu_scan)[irow]
        else:
            tab_s = Table.read(fitsfile,hdu=hdu_scan)[irow]
        tab_e = Table.read(fitsfile,hdu=hdu_energies)

        if norm_type in ['FLUX','EFLUX','DFDE']:        
            norm_vals = np.array(tab_s['NORM_SCAN']*tab_e['REF_%s'%norm_type][:,np.newaxis])
        elif norm_type == "NORM":
            norm_vals = np.array(tab_s['NORM_SCAN'])
        else:
            raise Exception('Unrecognized normalization type: %s'%norm_type)
            
        nll_vals = -np.array(tab_s['DLOGLIKE_SCAN'])
        emin = np.array(tab_e['E_MIN'])
        emax = np.array(tab_e['E_MAX'])
        npred = np.array(tab_s['NORM']*tab_e['REF_NPRED'])
        dfde = np.array(tab_s['NORM']*tab_e['REF_DFDE'])
        flux = np.array(tab_s['NORM']*tab_e['REF_FLUX'])
        eflux = np.array(tab_s['NORM']*tab_e['REF_EFLUX'])
        
        sd = SpecData(emin,emax,dfde,flux,eflux,npred)
    
        return CastroData(norm_vals,nll_vals,sd,norm_type)
        
    def spectrum_loglike(self,specType,params,scale=1E3):

        sfn = self.create_functor(specType,scale)[0]
        return self.__call__(sfn(params))      
        
    def test_spectra(self,spec_types=['PowerLaw','LogParabola','PLExpCutoff']):
        """
        """
        retDict = {}
        for specType in spec_types:            
            spec_func,init_pars,scaleEnergy = self.create_functor(specType)
            fit_result,fit_spec,fit_ts = self.fit_spectrum(spec_func,init_pars)
       
            specDict = {"Function":spec_func,
                        "Result":fit_result,
                        "Spectrum":fit_spec,
                        "ScaleEnergy":scaleEnergy,
                        "TS":fit_ts}

            retDict[specType] = specDict
            pass
        return retDict

    def create_functor(self,specType,scale=1E3):
        """Create a functor object that computes normalizations in a
        sequence of energy bins for a given spectral model.
        """

        emin = self._specData.emin
        emax = self._specData.emax

        if specType == 'PowerLaw':        
            initPars = np.array([5e-13,-2.0])
        elif specType == 'LogParabola': 
            initPars = np.array([5e-13,-2.0,0.0])
        elif specType == 'PLExpCutoff': 
            initPars = np.array([5e-13,-1.0,1E4])
        else:
            raise Exception('Unknown spectral type: %s'%specType)
            
        fn = SpectralFunction.create_functor(specType,
                                             self.norm_type,
                                             emin,
                                             emax,
                                             scale=scale)

        return (fn,initPars,scale)





class TSCube(object):
    """ 
    """
    def __init__(self,tsmap,normmap,tscube,normcube,
                 norm_vals,nll_vals,specData,norm_type):
        """C'tor

        Parameters
        ----------
        tsmap       : `~fermipy.skymap.Map`
           A Map object with the TestStatistic values in each pixel

        normmap     : `~fermipy.skymap.Map`
           A Map object with the normalization values in each pixel
           
        tscube      : `~fermipy.skymap.Map`
           A Map object with the TestStatistic values in each pixel & energy bin

        normcube    : `~fermipy.skymap.Map`
           A Map object with the normalization values in each pixel & energy bin
           
        norm_vals   : `~numpy.ndarray`        
           The normalization values ( nEBins X N array, where N is the
           number of sampled values for each bin )
           
        nll_vals    : `~numpy.ndarray`        
           The negative log-likelihood values ( nEBins X N array, where N is
           the number of sampled values for each bin )
           
        specData    : `~fermipy.sed.SpecData`
           The specData object
           
        norm_type : str
           String specifying the quantity used for the normalization
            * NORM : Normalization w.r.t. to test source
            * FLUX : Flux of the test source ( ph cm^-2 s^-1 )
            * EFLUX : Energy Flux of the test source ( MeV cm^-2 s^-1 )
            * NPRED : Number of predicted photons
            * DFDE : Differential flux of the test source ( ph cm^-2 s^-1 MeV^-1 )
            * E2DFDE : E^2 times Differential energy flux of the test source ( MeV cm^-2 s^-1 )
           
        """
        self._tsmap = tsmap
        self._normmap = normmap
        self._tscube = tscube
        self._normcube = normcube
        self._ts_cumul = tscube.sum_over_energy()
        self._specData = specData
        self._norm_vals = norm_vals
        self._nll_vals = nll_vals
        self._nE = self._specData.nE
        self._nN = 10
        self._norm_type = norm_type

    @property
    def tsmap(self):
        """ return the Map of the TestStatistic value """
        return self._tsmap
    
    @property
    def normmap(self):
        """ return the Map of the Best-fit normalization value """
        return self._normmap

    @property
    def tscube(self):
        """ return the Cube of the TestStatistic value per pixel / energy bin """
        return self._tscube

    @property
    def normcube(self):
        """ return the Cube of the normalization value per pixel / energy bin """
        return self._normcube    

    @property
    def ts_cumul(self):
        """ return the Map of the cumulative TestStatistic value per pixel (summed over energy bin) """
        return self._ts_cumul   

    @property
    def specData(self):
        """ Return the Spectral Data object """
        return self._specData  

    @property
    def nE(self):
        """ return the number of energy bins """
        return self._nE

    @property
    def nN(self):
        """ return the number of sample points in each energy bin """
        return self._nN

    @staticmethod 
    def create_from_fits(fitsfile,norm_type='FLUX'):
        """Build a TSCube object from a fits file created by gttscube
        Parameters
        ----------
        fitsfile : str
           Path to the tscube FITS file.
        norm_type : str 
           String specifying the quantity used for the normalization
        
        """
        tsmap,f = read_map_from_fits(fitsfile)
 
        tab_e = Table.read(fitsfile,'EBOUNDS')
        tab_s = Table.read(fitsfile,'SCANDATA')
        tab_f = Table.read(fitsfile,'FITDATA')

        emin = np.array(tab_e['E_MIN']/1E3)
        emax = np.array(tab_e['E_MAX']/1E3)
        nebins = len(tab_e)
        npred = tab_e['REF_NPRED']
        
        ndim = len(tsmap.counts.shape)

        if ndim == 2:
            cube_shape = (tsmap.counts.shape[0],
                          tsmap.counts.shape[1],nebins)
        elif ndim == 1:
            cube_shape = (tsmap.counts.shape[0],nebins)
        else:
            raise RuntimeError("Counts map has dimension %i"%(ndim))

        specData = SpecData(emin,emax,
                            np.array(tab_e['REF_DFDE']),
                            np.array(tab_e['REF_FLUX']),
                            np.array(tab_e['REF_EFLUX']),
                            npred)
        nll_vals =  -np.array(tab_s["DLOGLIKE_SCAN"])
        norm_vals = np.array(tab_s["NORM_SCAN"])
        
        wcs_3d = wcs_add_energy_axis(tsmap.wcs,emin)
        tscube = Map(np.rollaxis(tab_s["TS"].reshape(cube_shape),2,0),
                     wcs_3d)
        ncube = Map(np.rollaxis(tab_s["NORM"].reshape(cube_shape),2,0),
                    wcs_3d)
        nmap = Map(tab_f['FIT_NORM'].reshape(tsmap.counts.shape),
                   tsmap.wcs)
        
        ref_colname = 'REF_%s'%norm_type
        norm_vals *= tab_e[ref_colname][np.newaxis,:,np.newaxis]
        
        return TSCube(tsmap,nmap,tscube,ncube,norm_vals,nll_vals,specData,
                      norm_type)

    def castroData_from_ipix(self,ipix,colwise=False):
        """ Build a CastroData object for a particular pixel """
        # pix = utils.skydir_to_pix
        if colwise:
            ipix = self._tsmap.ipix_swap_axes(ipix,colwise)
        norm_d = self._norm_vals[ipix]
        nll_d = self._nll_vals[ipix]
        return CastroData(norm_d,nll_d,self._specData,self._norm_type)
    
    def castroData_from_pix_xy(self,xy,colwise=False):
        """ Build a CastroData object for a particular pixel """
        ipix = self._tsmap.xy_pix_to_ipix(xy,colwise)
        return self.castroData_from_ipix(ipix)

    def find_and_refine_peaks(self,threshold,min_separation=1.0,use_cumul=False):
        """
        """
        if use_cumul: 
            theMap = self._ts_cumul
        else:
            theMap = self._tsmap
            
        peaks = find_peaks(theMap,threshold,min_separation)
        for peak in peaks:
            #o =  utils.fit_parabola(theMap.counts,peak['iy'],peak['ix'],dpix=2)
            o, skydir = sourcefind.fit_error_ellipse(theMap,
                                                     (peak['ix'],peak['iy']),
                                                     dpix=2)
            peak['fit_loc'] = o
            peak['fit_skydir'] = skydir
            if o['fit_success']:            
                skydir = peak['fit_skydir']
            else:
                skydir = peak['skydir']
            pass
        return peaks

    def test_spectra_of_peak(self,peak,spec_types=["PowerLaw","LogParabola","PLExpCutoff"]):
        """
        """
        castro = self.castroData_from_pix_xy(xy=(peak['ix'],peak['iy']),colwise=False)
        test_dict = castro.test_spectra(spec_types)
        return (castro,test_dict)

    def find_sources(self,threshold,
                     min_separation=1.0,
                     use_cumul=False,
                     output_peaks=False,
                     output_castro=False,
                     output_specInfo=False,
                     output_src_dicts=False,
                     output_srcs=False):
        """
        """        
        srcs = []
        src_dicts = []
        castros = []
        specInfo = []
        names = []
        peaks = self.find_and_refine_peaks(threshold,min_separation,use_cumul=use_cumul)
        for i,peak in enumerate(peaks):
            (castro,test_dict) = self.test_spectra_of_peak(peak,["PowerLaw"])
            src_name = utils.create_source_name(peak['fit_skydir'])
            src_dict = build_source_dict(src_name,peak,test_dict,"PowerLaw")
            names.append(src_dict["name"])
            if output_castro:
                castros.append(castro)
            if output_specInfo:
                specInfo.append(test_dict)
            if output_src_dicts:
                src_dicts.append(src_dict)
            if output_srcs:
                src = roi_model.Source.create_from_dict(src_dict)
                srcs.append(src)            
            pass
        retDict = {"Names":names}
        if output_peaks:
            retDict["Peaks"]=peaks
        if output_castro:
            retDict["Castro"]=castros
        if output_specInfo:
            retDict["Spectral"]=specInfo
        if output_src_dicts:
            retDict["SrcDicts"]=src_dicts
        if output_srcs:
            retDict["Sources"]=srcs
        return retDict

def build_source_dict(src_name,peak_dict,spec_dict,spec_type):
    """
    """
    spec_results = spec_dict[spec_type]
    src_dir = peak_dict['fit_skydir']

    src_dict = dict(name=src_name,
                    Source_Name=src_name,
                    SpatialModel='PointSource',
                    SpectrumType=spec_type,
                    ts=spec_results["TS"][0],
                    ra=src_dir.icrs.ra.deg,               
                    dec=src_dir.icrs.dec.deg,
                    Prefactor=spec_results["Result"][0],
                    Index=-1.*spec_results["Result"][1],
                    Scale=spec_results["ScaleEnergy"])

    src_dict['pos_sigma'] = peak_dict['fit_loc']['sigma']
    src_dict['pos_sigma_semimajor'] = peak_dict['fit_loc']['sigma_semimajor']
    src_dict['pos_sigma_semiminor'] = peak_dict['fit_loc']['sigma_semiminor']
    src_dict['pos_r68'] = peak_dict['fit_loc']['r68']
    src_dict['pos_r95'] = peak_dict['fit_loc']['r95']
    src_dict['pos_r99'] = peak_dict['fit_loc']['r99']
    src_dict['pos_angle'] = np.degrees(peak_dict['fit_loc']['theta'])
    
    return src_dict




if __name__ == "__main__":


    from fermipy import roi_model
    import fermipy.utils as utils
    import xml.etree.cElementTree as ElementTree
    import sys

    if len(sys.argv) == 1:
        flux_type = "FLUX"
    else:
        flux_type = sys.argv[1]


    tscube = TSCube.create_from_fits("tscube_test.fits",flux_type)

    resultDict = tscube.find_sources(10.0,1.0,use_cumul=False,
                                     output_peaks=True,
                                     output_specInfo=True,
                                     output_srcs=True)

    figList = []
    peaks = resultDict["Peaks"]
    specInfos = resultDict["Spectral"]
    sources = resultDict["Sources"]
    
    root = ElementTree.Element('source_library')
    root.set('title', 'source_library')
      
    for src in sources:
        src.write_xml(root)

    output_file = open("sed_sources.xml", 'w!')
    output_file.write(utils.prettify_xml(root))

    """
    idx_off = -2

    for peak in peaks:
        castro,test_dict = tscube.test_spectra_of_peak(peak)

        result_pl = test_dict["PowerLaw"]["Result"]
        result_lp = test_dict["LogParabola"]["Result"]
        result_pc = test_dict["PLExpCutoff"]["Result"]
        ts_pl = test_dict["PowerLaw"]["TS"]
        ts_lp = test_dict["LogParabola"]["TS"]
        ts_pc = test_dict["PLExpCutoff"]["TS"]

        print ("Cumulative TS:        %.1f"%castro.ts_vals().sum())
        print ("TS for PL index free: %.1f (Index = %.2f)"%(ts_pl[0],idx_off-result_pl[1]))
        print ("TS for LogParabola:   %.1f (Index = %.2f, Beta = %.2f)"%(ts_lp[0],idx_off-result_lp[1],result_lp[2]))
        print ("TS for PLExpCutoff:   %.1f (Index = %.2f, E_c = %.2f)"%(ts_pc[0],idx_off-result_pc[1],result_pc[2]))

    """
        
