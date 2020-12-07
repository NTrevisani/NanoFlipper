import os, sys
from math import sqrt
from ROOT import TMinuit , TFile , TCanvas , TH2D, gROOT, gStyle
import ROOT
import numpy as np
from array import array as arr
from collections import OrderedDict
from  ctypes import c_double, c_int
from mkHist import ptbin, eta_bin
import random, csv

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
#eta_bin = [ 0. , 0.5  , 1.0  , 1.5  , 2.0 , 2.5 ]
def model_5x5( i , par ):

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

# 4x4 eta bin scheme
#eta_bin = [ 0. , 1.0  , 1.5 , 2.0 , 2.5 ]
def model_4x4( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )
     elif i == 3:  value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) )

     elif i == 4:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 5:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 6:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )
     elif i == 7:  value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) )

     elif i == 8: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 9: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 10: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )
     elif i == 11: value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) )

     elif i == 12: value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) )
     elif i == 13: value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) )
     elif i == 14: value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) )
     elif i == 15: value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) )

     return value
pass

def model_3x3( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )
     elif i == 2:  value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) )

     elif i == 3:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 4:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )
     elif i == 5:  value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) )

     elif i == 6: value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) )
     elif i == 7: value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) )
     elif i == 8: value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) )

     return value
pass

def model_2x2( i , par ):

     if   i == 0:  value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) )
     elif i == 1:  value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) )

     elif i == 2:  value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) )
     elif i == 3:  value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) )

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

    #model = model_5x5;
    #model = model_4x4;
    #model = model_3x3;
    model = model_2x2;

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

     #name=['q0','q1','q2','q3','q4']
     #name=['q0','q1','q2','q3']
     #name=['q0','q1','q2']
     name = [ 'q0' , 'q1' ]

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

def outFormat(ifile_,eta_bin_,pt_bin_,fitted_prob_,out_,useCsv=True):

    pt_lo = float(ptbin[pt_bin_].split(" && ")[-2].split(' ')[-1])
    pt_hi = float(ptbin[pt_bin_].split(" && ")[-1].split(' ')[-1])
    print pt_bin_

    outfile = open( "data/chargeFlip_%s_%s_SF.txt" %( ifile_ , pt_bin_ ) if not useCsv else 'data/chargeFlip_%s_%s_SF.csv' %( ifile_ , pt_bin_ ) , "w" )

    row_list=[]

    for i, ieta in enumerate(eta_bin):
        row=""
        if i==(len(eta_bin)-1): continue
        row='{:.1f} , {:.1f} , '.format( ieta , eta_bin[i+1] )
        row+='{:.1f} , {:.1f} , {:.3e} , {:.3e} , {:.3e} , {:.3e} , {:.3e} , {:.3e}'\
                .format( pt_lo , pt_hi , fitted_prob_['DATA'][i][0] , fitted_prob_['DATA'][i][1] , fitted_prob_['MC'][i][0] , fitted_prob_['MC'][i][1] , out_[i][0] , out_[i][1] )
        row_list.append( row if not useCsv else [row] )
    #print row_list
    #sys.exit()
    # preprocess
    fout=[]
    for i, line in enumerate(row_list):
        header = ['etaDown','etaUp','ptDown','ptUp','DATA','DATAerr','MC','MCerr','SF','SFerr' ]
        if i==0: fout.append( ' , '.join(header) if not useCsv else header )
        fout.append( line if not useCsv else line[0].replace(' ','').split(',') )

    with outfile as out_handler:
        if not useCsv:
            print "Writing to txt format"
            for listitem in fout:
                out_handler.write( '%s\n' %listitem )
        else:
            print "Wiriting to CSV format"
            writer = csv.writer( out_handler )
            writer.writerows( fout )
    pass

def mk2Dfromcsv( ifile_ , pt_bin_ ):

    ptlist=[]
    for idict in pt_bin_:
        pt_lo = float(pt_bin_[idict].split(" && ")[-2].split(' ')[-1])
        pt_hi = float(pt_bin_[idict].split(" && ")[-1].split(' ')[-1])
        ptlist.append(pt_lo);
        ptlist.append(pt_hi);

    ptlist =  sorted(list(dict.fromkeys(ptlist)))

    #pt_lo = float(ptbin[pt_bin_].split(" && ")[-2].split(' ')[-1])
    #pt_hi = float(ptbin[pt_bin_].split(" && ")[-1].split(' ')[-1])

    # initialize csv
    dcsv=OrderedDict()
    c=0
    for i, ikey in enumerate(pt_bin_.keys()):
        with open( "data/chargeFlip_%s_%s_SF.csv" %( ifile_ , ikey ) , 'r' ) as f:
            for x , line in enumerate(csv.DictReader(f)):
                dcsv[c] = line
                c+=1
    # initialize mischarge probability h2d
    sf_hist= OrderedDict()
    for ihist in [ 'data' , 'data_sys' , 'mc' , 'mc_sys' , 'sf' , 'sf_sys' ]:
        sf_hist[ihist] = TH2D( ihist , 'charge flipping rate %s ; eta bin ; pt bin' %ihist , len(eta_bin)-1 , arr( 'f' , eta_bin ) , len(ptlist)-1 , arr( 'f' , ptlist ) )

    h_dummy = sf_hist['data']
    for ibinX in range(1,h_dummy.GetNbinsX()+1):
        eta = h_dummy.GetXaxis().GetBinCenter(ibinX)
        for ibinY in range(1,h_dummy.GetNbinsY()+1):
            pt =  h_dummy.GetYaxis().GetBinCenter(ibinY)

            # looking for correct eta , pt bin
            for num , ibn in dcsv.items():
                if eta >= float(ibn['etaDown']) and eta < float(ibn['etaUp']) and pt >= float(ibn['ptDown']) and pt < float(ibn['ptUp']):

                    data_flip = float(ibn['DATA']) ; data_flip_sys = float(ibn['DATAerr'])
                    mc_flip = float(ibn['MC']) ; mc_flip_sys = float(ibn['MCerr'])
                    sf_flip = float(ibn['SF']) ; sf_flip_sys = float(ibn['SFerr'])

                    sf_hist['data'].SetBinContent( ibinX , ibinY , data_flip )
                    sf_hist['data_sys'].SetBinContent( ibinX , ibinY , data_flip_sys )
                    sf_hist['mc'].SetBinContent( ibinX , ibinY , mc_flip )
                    sf_hist['mc_sys'].SetBinContent( ibinX , ibinY , mc_flip_sys )
                    sf_hist['sf'].SetBinContent( ibinX , ibinY , sf_flip )
                    sf_hist['sf_sys'].SetBinContent( ibinX , ibinY , sf_flip_sys )

                    #break;
    # save it
    h_fileout = TFile.Open( "data/chargeFlip_%s_SF.root" %( ifile_ ) , "RECREATE" )
    map(lambda x: sf_hist[x].Write() , sf_hist)
    h_fileout.Close()
    pass

    # verify.
    #for ihistkey in sf_hist:
    #    c = TCanvas() ; c.cd()
    #    sf_hist[ihistkey].Draw("ColzText")
    #    c.Print('%s/h_flipping_%s_2D.png' %( output_ , ihistkey ) )
    #return sf_hist

def mkSf( ifile_ , ptbin_ , outcsv_=True):
     fitted_prob = OrderedDict()
     h4val=OrderedDict()
     out=OrderedDict()
     h_ratio={}

     year=ifile_.split('_')[-1]
     h_data = TFile.Open("plots/%s/Chflipfit/%s_mll/ratio_DATASUB_%s_%s_mll.root" %(ifile_,ptbin_,year,ptbin_) ,"READ")
     h_mc   = TFile.Open("plots/%s/Chflipfit/%s_mll/ratio_DY_%s_%s_mll.root" %(ifile_,ptbin_,year,ptbin_) ,"READ")

     print year
     print ptbin_
     # here
     # fit
     fitted_prob[year]={}
     h4val[year]={}
     for ids in [ 'DATA' , 'MC' ]:
          print ids
          h4val[year][ids] = flatten2D( h_data.Get('h2_DATASUB') if ids=='DATA' else h_mc.Get('h2_DY') )
          fitted_prob[year][ids] = fit( arr( 'f' , h4val[year][ids][0] ) , arr( 'f' , h4val[year][ids][1] ) ) # fit( value, error )
     out[year] = map( lambda x , y : [ x[0]/y[0] , sqrt( (x[1]*x[1])/(x[0]*x[0]) + (y[1]*y[1])/(y[0]*y[0]) ) ]  , fitted_prob[year]['DATA'] , fitted_prob[year]['MC'] )

     # save sf csv
     outFormat( ifile , eta_bin , ptbin_ , fitted_prob[year] , out[year] , outcsv_ ) ## HERE
     #mk2Dfromcsv( ifile , ptbin_ )

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

def mkValidation(ifile_,flipPro,h_val,ptbin_):
     # flipPro : dict[year][ids][ [val,err] , [], ...  ]
     # h_val : faltten 2D bins , ranging to 25
     output='plots/%s/postfit_validation/%s' %(ifile_,ptbin_)
     if not os.path.exists(output): os.system('mkdir -p %s' %output)

     c = TCanvas( 'c' , 'ratio_postfit_validation' , 1200 , 800 )
     c.Divide(2,2)
     year=ifile_.split('_')[-1]
     for ids in ['DATA','MC']:
          dim = len(h_val[year][ids][0]) # infers dimension
          flipper = map(lambda x: x[0], flipPro[year][ids]) # extract the fitted value (mischarge probability)

          bins_postfit = map( lambda x: model_2x2(x,flipper) , list(range(0,dim)) ) # reproduce the ratio
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
    fit_A_param = map( lambda x : x[0] , fit( zA , errorzA ) ) ; fit_A_toy = map( lambda x: model_2x2(x,fit_A_param) , list(range(0,dim)) )
    fit_B_param = map( lambda x : x[0] , fit( zB , errorzB ) ) ; fit_B_toy = map( lambda x: model_2x2(x,fit_B_param) , list(range(0,dim)) )
    c.cd(3) ; h_A_postfit_toy = mk2DHisto( fit_A_toy , 'h_ratio_postfit_toy_A' , None , 'toy A N_{ss}/N_{os}' ) ; h_A_postfit_toy.Draw("Colz TEXTE")
    c.cd(4) ; h_B_postfit_toy = mk2DHisto( fit_B_toy , 'h_ratio_postfit_toy_B' , None , 'toy A N_{ss}/N_{os}' ) ; h_B_postfit_toy.Draw("Colz TEXTE")
    c.Update()
    c.Print( "toy.png" )
    pass

if __name__ == "__main__":

     if not os.path.exists( 'plots/' ):
          print("Error, path folder does not exist")
          sys.exit()

     #ptbin="lowpt2"

     # toy
     #mkToy( (len(eta_bin)-1)*(len(eta_bin)-1) )

     for iptbin in ptbin:
          # fit, validate
          summary = open( "data/fit_summary_%s.txt" %iptbin , "w" )
          fpout=[] ;
          for ifile in os.listdir('plots/'):
               fitted = mkSf( ifile , iptbin , True ) # output sf file in csv
               mischarge = fitted[0] ; histo_val = fitted[1] ; epsilon = fitted[2]

               for year in epsilon:
                    fpout.append(" ===> scale factor DATA/MC for %s" %year)
                    for num, isf in enumerate(epsilon[year]):
                         fpout.append('q{} data : {:.3e} +/- {:.3e} ; mc : {:.3e} +/- {:.3e} ; SF : {:.3e} +/- {:.3e} ( rel.error : {:.2f} % )'\
                                      .format( num , mischarge[year]['DATA'][num][0] , mischarge[year]['DATA'][num][1] , mischarge[year]['MC'][num][0] , mischarge[year]['MC'][num][1] , isf[0] , isf[1] , (isf[1]/isf[0])*100 ) )
               #print ""
               # on the fly diagnostics
               mkValidation( ifile , mischarge , histo_val , iptbin )

          ### diagnositics
          with summary as out_handling:
               for listitem in fpout:
                    out_handling.write( '%s\n' %listitem )
          os.system( 'cat data/fit_summary_%s.txt' %iptbin )

     # make histogram from CSV
     for ifile in [ 'nanov5_2016' , 'nanov5_2017' , 'nanov5_2018' ] :
         mk2Dfromcsv( ifile , ptbin )


     pass
