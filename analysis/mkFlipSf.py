import os, sys
from math import sqrt
from ROOT import TMinuit , TFile
import numpy as np
from array import array as arr
from collections import OrderedDict
from  ctypes import c_double, c_int

# 5x5 eta bin scheme
def model( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) )
     elif i == 4:  value = ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) / ( 1 - ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) )

     elif i == 5:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 6:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 7:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )
     elif i == 8:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) )
     elif i == 9:  value = ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) / ( 1 - ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) )

     elif i == 10: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 11: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 12: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )
     elif i == 13: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) )
     elif i == 14: value = ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) / ( 1 - ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) )

     elif i == 15: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) )
     elif i == 16: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) )
     elif i == 17: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) )
     elif i == 18: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) )
     elif i == 19: value = ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) / ( 1 - ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) )

     elif i == 20: value = ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) / ( 1 - ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) )
     elif i == 21: value = ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) / ( 1 - ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) )
     elif i == 22: value = ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) / ( 1 - ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) )
     elif i == 23: value = ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) / ( 1 - ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) )
     elif i == 24: value = ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) / ( 1 - ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) )

     return value
pass

""" meaning of parametrs:
npar:  number of parameters
deriv: aray of derivatives df/dp_i (x), optional
f:     value of function to be minimised (typically chi2ornegLogL)
par:  the array of parameters
iflag: internal flag: 1 at first call, 3 at the last, 4 during minimisation
"""

def chisq( npar , deriv , f , par , iflag):

    chisq=0.0
    for i in range(0, nBins):
        delta = ( model( i, par ) - val[i] ) / err[i]
        chisq += delta*delta

    #f[0] = chisq
    f.value = chisq
    pass

def leastsq( npar , deriv , f , par , iflag):

    leastsq=0.0
    for i in range(0, nBins):
        delta = ( model( i, par ) - val[i] ) / err[i]
        leastsq += delta*delta

    #f[0] = chisq                                                                                                                        
    f.value = leastsq
    pass


def fit( p , perr ):

     global val, err, nBins
     val = p
     err = perr
     nBins=len(val)

     print nBins

     name=['q0','q1','q2','q3','q4']
     npar=len(name)
     # the initial values
     vstart = arr( 'd' , npar*[0.1] )
     # the initial step size
     step = arr( 'd' , npar*[0.000001] )

     # --> set up MINUIT
     gMinuit = TMinuit ( npar ) # initialize TMinuit with maximum of npar parameters
     gMinuit.SetFCN( chisq ) # set function to minimize
     arglist = arr( 'd' , npar*[0.01] ) # set error definition
     ierflg = c_int(0)

     arglist[0] = 1. # 1 sigma is Delta chi2 = 1
     gMinuit.mnexcm("SET ERR", arglist, 1, ierflg )

     # --> set starting values and step size for parameters
     # Define the parameters for the fit
     for i in range(0,npar): gMinuit.mnparm( i, name[i] , vstart[i] , step[i] , 0, 0, ierflg )
     # now ready for minimization step
     arglist [0] = 500 # Number of calls for FCN before giving up
     arglist [1] = 1. # Tolerance
     gMinuit.mnexcm("MIGRAD" , arglist , 2 , ierflg) # execute the minimisation

     # --> check TMinuit status
     amin , edm , errdef = c_double(0.) , c_double(0.) , c_double(0.)
     nvpar , nparx , icstat = c_int(0) , c_int(0) , c_int(0)
     gMinuit.mnstat (amin , edm , errdef , nvpar , nparx , icstat )
     gMinuit.mnprin(3,amin) # print-out by Minuit

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

     # --> get results from MINUIT
     finalPar = []
     finalParErr = []
     p, pe = c_double(0.) , c_double(0.)
     for i in range(0,npar):
          gMinuit.GetParameter(i, p, pe) # retrieve parameters and errors
          finalPar.append( float(p.value) )
          finalParErr.append( float(pe.value) )
     # get covariance matrix
     buf = arr('d' , npar*npar*[0.])
     gMinuit.mnemat( buf , npar ) # retrieve error matrix
     emat = np.array( buf ).reshape( npar , npar )

     # --> provide formatted output of results
     print "\n"
     print "*==* MINUIT fit completed:"
     print'fcn@minimum = %.3g'%( amin.value ) , " error code =" , ierflg.value , " status =" , icstat.value , " (if its 3, mean accurate)"
     print " Results: \t value error corr. mat."
     for i in range(0,npar):
          print'%s: \t%10.3e +/- %.1e'%( name[i] , finalPar[i] , finalParErr[i] ) ,
          for j in range (0,i): print'%+.3g'%( emat[i][j]/np.sqrt(emat[i][i])/np.sqrt(emat[j][j]) ),
          print "\n"

     return [ [i,j]  for i,j in zip(finalPar , finalParErr) ]

def flatten2D(h2d):
    bins=[]; errs=[]
    for i in range( 1 , h2d.GetNbinsX() + 1 ):
        for j in range( 1 , h2d.GetNbinsY() + 1 ):
            bins.append( h2d.GetBinContent(i,j) )
            errs.append( h2d.GetBinError(i,j) )
    return [ bins , errs ]


if __name__ == "__main__":

     ptbin="lowpt2"

     if not os.path.exists( 'plots/' ):
          print("Error, path folder does not exist")
          sys.exit()

     epsilon=OrderedDict()
     for ifile in os.listdir('plots/'):
          h_ratio={}
          year=ifile.split('_')[-1]
          print year
          h_data = TFile.Open("plots/nanov5_%s/Chflipfit/%s_mll/ratio_DATASUB_%s_%s_mll.root" %(year,ptbin,year,ptbin) ,"READ")
          h_mc   = TFile.Open("plots/nanov5_%s/Chflipfit/%s_mll/ratio_DY_%s_%s_mll.root" %(year,ptbin,year,ptbin) ,"READ")
          h_ratio['DATA'] = flatten2D(h_data.Get('h2_DATASUB'))
          h_ratio['MC'] = flatten2D(h_mc.Get('h2_DY'))
          # fit
          fitted=OrderedDict()
          for ids in [ 'DATA' , 'MC' ]: fitted[ids] = fit( arr( 'f' , h_ratio[ids][0] ) , arr( 'f' , h_ratio[ids][1] ) )
          epsilon[year] = map( lambda x , y : [ x[0]/y[0] , sqrt( (x[1]*x[1])/(x[0]*x[0]) + (y[1]*y[1])/(y[0]*y[0]) ) ]  , fitted['DATA'] , fitted['MC'] )
     
     for year in epsilon:
         print " ===> ", year
         for num , iparam in enumerate(epsilon[year]):
             print 'q' , num , ' : epsilon = ', iparam[0] , ' +/- ', iparam[1]
         print ""
