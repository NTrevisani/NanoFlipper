import os, sys
from math import sqrt
from ROOT import TMinuit , TFile , TCanvas , TH2D, gROOT, gStyle
import ROOT
import numpy as np
from array import array as arr
from collections import OrderedDict
from  ctypes import c_double, c_int
from mkHist import ptbin, eta_bin
import random

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
#gStyle.SetPaintTextFormat("4.2f")
gStyle.SetPalette(ROOT.kArmy)
#gStyle.SetPalette(ROOT.kAquamarine)
gStyle.SetPadRightMargin(0.2)
gStyle.SetPadBottomMargin(0.13)
gStyle.SetPadLeftMargin(0.1)

eta_bin_array = arr('f', eta_bin )

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

def fcn( npar , deriv , f , par , iflag):

    chisq=0.0
    for i in range(0, nBins):
        delta = ( model( i, par ) - val[i] ) / err[i]
        chisq += delta*delta

    #f[0] = chisq
    f.value = chisq
    pass

def fit( p , perr ):

     global val, err, nBins
     val = p
     err = perr
     nBins=len(val)

     name=['q0','q1','q2','q3','q4']
     npar=len(name)
     # the initial values
     vstart = arr( 'd' , npar*[0.1] )
     # the initial step size
     step = arr( 'd' , npar*[0.000001] )

     # --> set up MINUIT
     gMinuit = TMinuit ( npar ) # initialize TMinuit with maximum of npar parameters
     gMinuit.SetFCN( fcn ) # set function to minimize
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

def mkSf(ptbin):
     fitted_prob = OrderedDict()
     h4val=OrderedDict()
     out=OrderedDict()
     for ifile in os.listdir('plots/'):
          h_ratio={}
          year=ifile.split('_')[-1]
          h_data = TFile.Open("plots/%s/Chflipfit/%s_mll/ratio_DATASUB_%s_%s_mll.root" %(ifile,ptbin,year,ptbin) ,"READ")
          h_mc   = TFile.Open("plots/%s/Chflipfit/%s_mll/ratio_DY_%s_%s_mll.root" %(ifile,ptbin,year,ptbin) ,"READ")
          # fit
          fitted_prob[year]={}
          h4val[year]={}
          for ids in [ 'DATA' , 'MC' ]:
              h4val[year][ids] = flatten2D( h_data.Get('h2_DATASUB') if ids=='DATA' else h_mc.Get('h2_DY') )
              fitted_prob[year][ids] = fit( arr( 'f' , h4val[year][ids][0] ) , arr( 'f' , h4val[year][ids][1] ) ) # fit( value, error )
          out[year] = map( lambda x , y : [ x[0]/y[0] , sqrt( (x[1]*x[1])/(x[0]*x[0]) + (y[1]*y[1])/(y[0]*y[0]) ) ]  , fitted_prob[year]['DATA'] , fitted_prob[year]['MC'] )

     return [ fitted_prob , h4val , out ]

def mk2DHisto(bins_in , name , bins_error_in=None , ztitle="charge flip probability"):

    h_ratio_create=TH2D( name , '%s ; lepton 1 Eta ; lepton 2 Eta' %name , len(eta_bin)-1 , eta_bin_array , len(eta_bin)-1 , eta_bin_array )
    counter=0
    for i in range(0,len(eta_bin)-1):
        for j in range(0,len(eta_bin)-1):
            h_ratio_create.SetBinContent( i+1 , j+1 , bins_in[counter])
            if bins_error_in is not None: h_ratio_create.SetBinError( i+1 , j+1 , bins_error_in[counter])
            counter+=1
    h_ratio_create.GetZaxis().SetTitle(ztitle)
    h_ratio_create.SetMarkerSize(1.5)
    return h_ratio_create

def mkValidation(flipPro,h_val,ptbin):
    # flipPro : dict[year][ids][ [val,err] , [], ...  ]
    # h_val : faltten 2D bins , ranging to 25
    for ifile in os.listdir('plots/'):
        output='plots/%s/postfit_validation/%s' %(ifile,ptbin)
        if not os.path.exists(output): os.system('mkdir -p %s' %output)

        c = TCanvas( 'c' , 'ratio_postfit_validation' , 1200 , 800 )
        c.Divide(2,2)
        year=ifile.split('_')[-1]
        for ids in ['DATA','MC']:
            dim = len(h_val[year][ids][0]) # infers dimension
            flipper = map(lambda x: x[0], flipPro[year][ids]) # extract the fitted value (mischarge probability)

            bins_postfit = map( lambda x: model(x,flipper) , list(range(0,dim)) ) # reproduce the ratio
            bins_prefit = h_val[year][ids][0]
            bins_diff = map(lambda x : (abs(bins_prefit[x] - bins_postfit[x])/bins_prefit[x])*100. , list(range(0,dim)) )

            c.cd(1) ; h_prefit  = mk2DHisto( bins_prefit , 'h_ratio_prefit_%s' %ids ) ; h_prefit.Draw("Colz TEXT45")
            c.cd(2) ; h_postfit = mk2DHisto( bins_postfit , 'h_ratio_postfit_%s' %ids ) ; h_postfit.Draw("Colz TEXT45")
            c.cd(3) ; h_diff    = mk2DHisto( bins_diff , 'h_ratio_diff_%s' %ids , None , 'rel. Difference in percent' ) ; h_diff.Draw("Colz TEXT45")
            c.Update()
            c.Print( "%s/val_ratio_postprefit_%s.png" %(output,ids) )
    pass

# input the five dummy parameters

def mkToy(dim):
    #toy
    print "Running on Toy"
    zA = arr( 'f' , [ random.uniform(0,0.01) for i in range(dim) ] ) ; errorzA = arr( 'f' , [ 0.0025 for i in range(dim) ] )
    zB = arr( 'f' , [ random.uniform(0,0.01) for i in range(dim) ] ) ; errorzB = arr( 'f' , [ 0.0025 for i in range(dim) ] )

    c = TCanvas( 'c' , 'ratio_fit_toy' , 1200 , 800 )
    c.Divide(2,2)

    c.cd(1) ; h_A_prefit_toy = mk2DHisto( zA , 'h_ratio_prefit_toy_A' , errorzA , 'toy A N_{ss}/N_{os}' ) ; h_A_prefit_toy.Draw("Colz TEXTE")
    c.cd(2) ; h_B_prefit_toy = mk2DHisto( zB , 'h_ratio_prefit_toy_B' , errorzB , 'toy B N_{ss}/N_{os}' ) ; h_B_prefit_toy.Draw("Colz TEXTE")
    fit_A_param = map( lambda x : x[0] , fit( zA , errorzA ) ) ; fit_A_toy = map( lambda x: model(x,fit_A_param) , list(range(0,dim)) )
    fit_B_param = map( lambda x : x[0] , fit( zB , errorzB ) ) ; fit_B_toy = map( lambda x: model(x,fit_B_param) , list(range(0,dim)) )
    c.cd(3) ; h_A_postfit_toy = mk2DHisto( fit_A_toy , 'h_ratio_postfit_toy_A' , None , 'toy A N_{ss}/N_{os}' ) ; h_A_postfit_toy.Draw("Colz TEXTE")
    c.cd(4) ; h_B_postfit_toy = mk2DHisto( fit_B_toy , 'h_ratio_postfit_toy_B' , None , 'toy A N_{ss}/N_{os}' ) ; h_B_postfit_toy.Draw("Colz TEXTE")
    c.Update()
    c.Print( "toy.png" )
    pass

if __name__ == "__main__":

     if not os.path.exists( 'plots/' ):
          print("Error, path folder does not exist")
          sys.exit()

     ptbin="lowpt2"
     ########################################################################
     mkToy( (len(eta_bin)-1)*(len(eta_bin)-1) )
     ########################################################################
     fitted = mkSf( ptbin )
     mischarge = fitted[0] ; histo_val = fitted[1] ; epsilon = fitted[2]

     for year in epsilon:
          print " ===> scale factor DATA/MC for ", year
          for num , iparam in enumerate(epsilon[year]):
               print "q%s SF : epsilon = %.6f +/- %.6f ; relative error : %.2f %%" %( num , iparam[0] , iparam[1] , (iparam[1]/iparam[0])*100 )
          print ""
     ##########################################################################
     mkValidation( mischarge , histo_val , ptbin )
