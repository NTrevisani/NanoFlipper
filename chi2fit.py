from ROOT import TMinuit , Double , Long
import numpy as np
from array import array as arr
#import matplotlib.pyplot as plt
'''
def model( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) );
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) );
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) );
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) );
     elif i == 4:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) );
     elif i == 5:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) );
     elif i == 6:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) );
     elif i == 7:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) );
     elif i == 8:  value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) );
     elif i == 9:  value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) );
     elif i == 10: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) );
     elif i == 11: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) );
     elif i == 12: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) );
     elif i == 13: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) );
     elif i == 14: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) );
     elif i == 15: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) );

     return value
pass
'''


def model( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) );
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) );
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) );
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) );
     elif i == 4:  value = ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) / ( 1 - ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) );
     
     elif i == 5:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) );
     elif i == 6:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) );
     elif i == 7:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) );
     elif i == 8:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) );
     elif i == 9:  value = ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) / ( 1 - ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) );

     elif i == 10:  value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) );
     elif i == 11:  value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) );
     elif i == 12: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) );
     elif i == 13: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) );
     elif i == 14: value = ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) / ( 1 - ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) );

     elif i == 15: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) );
     elif i == 16: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) );
     elif i == 17: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) );
     elif i == 18: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) );
     elif i == 19: value = ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) / ( 1 - ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) );

     elif i == 20: value = ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) / ( 1 - ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) );
     elif i == 21: value = ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) / ( 1 - ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) );
     elif i == 22: value = ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) / ( 1 - ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) );
     elif i == 23: value = ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) / ( 1 - ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) );
     elif i == 24: value = ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) / ( 1 - ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) );

     return value
pass


def fcn( npar , deriv , f , par , iflag):

    """ meaning of parametrs:
    npar:  number of parameters
    deriv: aray of derivatives df/dp_i (x), optional
    f:     value of function to be minimised (typically chi2ornegLogL)
    par:  the array of parameters
    iflag: internal flag: 1 at first call, 3 at the last, 4 during minimisation
    """
    
    chisq=0.0
    for i in range(0, nBins):
        delta = (val[i] - model( i, par )/err[i])
        chisq += delta*delta

    f[0] = chisq

def fit(p,perr):

     global val, err, nBins
     val = p
     err = perr
     nBins=len(val)

     print nBins
     
     name=['q0','q1','q2','q3','q4']
     #name=['q0','q1','q2','q3']
     npar=len(name)
     # the initial values
     vstart = arr( 'd' , ( 0.1 , 0.1 , 0.1 , 0.1 , 0.1  ) )
     # the initial step size
     step = arr( 'd' , ( 0.001 , 0.001 , 0.001 , 0.001 , 0.001 ) )
     
     # --> set up MINUIT
     gMinuit = TMinuit ( npar ) # initialize TMinuit with maximum of npar parameters
     gMinuit.SetFCN( fcn ) # set function to minimize
     arglist = arr('d' , npar*[0.01]) # set error definition
     ierflg = Long(0)

     #arglist[0] = 1. # 1 sigma is Delta chi2 = 1
     arglist[0] = 2
     gMinuit.mnexcm("SET ERR", arglist, 1, ierflg)

     # --> set starting values and step size for parameters
     for i in range(0,npar):
          # Define the parameters for the fit
          gMinuit.mnparm( i, name[i] , vstart[i] , step[i] , 0, 1, ierflg )
     arglist [0] = 500 # Number of calls for FCN before giving up
     arglist [1] = 1 # Tolerance
     gMinuit.mnexcm("MIGRAD" , arglist , 2 , ierflg) # execute the minimisation

     # --> check TMinuit status
     amin , edm , errdef = Double (0.) , Double (0.) , Double (0.)
     nvpar , nparx , icstat = Long (0) , Long (0) , Long (0)
     gMinuit.mnstat (amin , edm , errdef , nvpar , nparx , icstat )
     
     # meaning of parameters:
     #   amin:   value of fcn distance at minimum (=chi^2)
     #   edm:    estimated distance to minimum
     #   errdef: delta_fcn used to define 1 sigam errors
     #   nvpar:  total number of parameters
     #   icstat: status of error matrix:
     #           3 = accurate
     #           2 = forced pos. def
     #           1 = approximative
     #           0 = not calculated
     #
     
     gMinuit.mnprin(3,amin) # print-out by Minuit
     # --> get results from MINUIT
     finalPar = []
     finalParErr = []
     p, pe = Double(0) , Double(0)
     for i in range(0,npar):
          gMinuit.GetParameter(i, p, pe) # retrieve parameters and errors
          finalPar.append(float(p))
          finalParErr.append(float(pe))
     # get covariance matrix
     buf = arr('d' , npar*npar*[0.])
     gMinuit.mnemat( buf , npar ) # retrieve error matrix
     emat = np.array( buf ).reshape( npar , npar )

     # --> provide formatted output of results
     print "\n"
     print "*==* MINUIT fit completed:"
     print'fcn@minimum = %.3g'%(amin)," error code =",ierflg," status =",icstat, " (if its 3, mean accurate)"
     print " Results: \t value error corr. mat."
     for i in range(0,npar):
          print'%s: \t%10.3e +/- %.1e'%(name[i] ,finalPar[i] ,finalParErr[i]) ,
          for j in range (0,i):
               print'%+.3g'%(emat[i][j]/np.sqrt(emat[i][i])/np.sqrt(emat[j][j])),
          print ' '
          print "\n"
     return [ finalPar , finalParErr ]
pass
     
          
