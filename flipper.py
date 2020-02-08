from helper import *
import ROOT
from ROOT import gROOT, gStyle
import sys, os
import numpy as np
from chi2fit import *
from math import sqrt

######################
# what does it do?
# 1.) plot 1D kinematics between DATA/MC
# 2.) plot 1D N_SS/N_OS on kinematics
# 3.) plot 2D N_SS/N_OS on eta1; eta2 , pt??
# 4.) extract N_SS/N_OS
# 5.) fit

ROOT.TH1.SetDefaultSumw2()
#gROOT.SetBatch(True)
#gStyle.SetOptStat(0)
#gStyle.SetPaintTextFormat(".5f")

dir='plots/'

files=[
    #dir+'nanov5_2016/nanov5_2016.root',
    dir+'nanov5_2017/nanov5_2017.root',
    #dir+'nanov5_2018/nanov5_2018.root'
]

epsilon={}
epsilon_err={}

for ifile in files:
    token=ifile.split('/')[-1].split('.root')[0]
    epsilon[token] = {}
    epsilon_err[token] = {}
    f = TFile.Open(ifile,"READ")
    #name of tree (key)
    samples=[ key.GetName() for key in f.GetListOfKeys() ]
    #collect variable
    variables = list(dict.fromkeys(map(lambda x : x.split('_')[-1], samples)))

    #built add histogram
    #convert list of key into key-pair dictionary
    histlist = dict( zip( map(lambda x : x, samples) , map(lambda x : f.Get(x), samples) ) ) ###
    haddlist={}
    
    for key,ihist in histlist.iteritems():
        for ivar in variables:
            #Hadd according to process
            if 'DY' in key and ivar in key:
                #print 'DY here: ', key
                if 'DY_%s_%s'%(key.split('_')[-2],key.split('_')[-1]) not in haddlist: haddlist['DY_%s_%s'%(key.split('_')[-2],key.split('_')[-1])]= ihist.Clone('DY_%s_%s'%(key.split('_')[-2],key.split('_')[-1]))
                else: haddlist['DY_%s_%s'%(key.split('_')[-2],key.split('_')[-1])].Add(ihist)
            if key.split('_')[-3]=='fake' and ivar in key:
                #print 'Fake here: ', key
                print 'FAKE_%s_%s'%(key.split('_')[-2],key.split('_')[-1])
                if 'FAKE_%s_%s'%(key.split('_')[-2],key.split('_')[-1]) not in haddlist: haddlist['FAKE_%s_%s'%(key.split('_')[-2],key.split('_')[-1])]= ihist.Clone('FAKE_%s_%s'%(key.split('_')[-2],key.split('_')[-1]))
                else: haddlist['FAKE_%s_%s'%(key.split('_')[-2],key.split('_')[-1])].Add(ihist)
            elif ( key.split('_')[-3]=='DoubleEG' or key.split('_')[-3]=='SingleElectron' or key.split('_')[-3]=='EGamma') and ivar in key:
            #    #print 'DATA here: ', key
                if 'DATA_%s_%s'%(key.split('_')[-2],key.split('_')[-1]) not in haddlist: haddlist['DATA_%s_%s'%(key.split('_')[-2],key.split('_')[-1])]= ihist.Clone('DATA_%s_%s'%(key.split('_')[-2],key.split('_')[-1]))
                else: haddlist['DATA_%s_%s'%(key.split('_')[-2],key.split('_')[-1])].Add(ihist)
    
    #plot 1D kinematics between DATA/MC
    for ireg in [ 'OSnum' , 'SSnum' ]: #NO NEED REGION
        fl1 = filter(lambda x: ireg in x, haddlist)
        for jvar in variables:
            fl2 = filter(lambda x: jvar in x,fl1)
            if jvar=='2d': continue
            SaveHisto1D( dict( zip( map(lambda x : x, fl2) , map(lambda x : haddlist[x], fl2) ) ) , ireg , jvar, f , token , 0, 4, False , True if jvar in [ 'lep1pt','lep2pt' ] else False)
    '''
    #plot ratio SS/OS on 1D kinematics
    for isample in ['DATA','DY']:
        fl1 = filter(lambda x: isample in x, haddlist)
        for ivar in variables:
            if ivar=='mll': continue
            fl2 = filter(lambda x: ivar in x, fl1)
            hSS = map(lambda x: haddlist[x] , filter(lambda x: 'SSnum' in x,fl2))
            hOS = map(lambda x: haddlist[x] , filter(lambda x: 'OSnum' in x,fl2))
            SaveRatio(hSS[0],hOS[0],token,isample,ivar)
    
    #extract ratio from each bins and do fit
    fitvar={};
    for c,isample in enumerate(['DATA','DY']):
        fitvar[isample] = {}
        if os.path.isfile('plots/%s/Object_studies/Ratio_%s_%s_2d.root' %(token, token, isample)):
            ro = TFile.Open('plots/%s/Object_studies/Ratio_%s_%s_2d.root' %(token, token, isample),'READ')
            hratio = ro.Get('hratio_2d')
            bins=[]; err=[]; counter=0
            # bin squeence define as from bottom to top, transversing from left to right
            for ixbin in range(1,hratio.GetNbinsX()+1):
                for iybin in range(1,hratio.GetNbinsY()+1):
                    print('%s_Z[%s] = %s; %s_Z_err[%s] = %s;' %( isample , counter , hratio.GetBinContent(ixbin,iybin) , isample , counter , hratio.GetBinError(ixbin,iybin) ) )
                    bins.append(hratio.GetBinContent(ixbin,iybin))
                    err.append(hratio.GetBinError(ixbin,iybin))
                    counter+=1
            #
            fitted = fit( arr('f',bins) , arr('f',err) )
            fitvar[isample]['fit'] = fitted[0]
            fitvar[isample]['err'] = fitted[1]

    #number of param
    epsilon[token] = [ float(i) / float(j) for i, j in zip(fitvar['DATA']['fit'], fitvar['DY']['fit'])]
    rel_err={}
    for iproc in [ 'DATA' , 'DY' ]: rel_err[iproc] = [  (float(i) / float(j))*(float(i) / float(j)) for i, j in zip(fitvar[iproc]['err'], fitvar[iproc]['fit'])]
    rel_sqrt = [ sqrt(float(i) + float(j)) for i, j in zip(rel_err['DATA'], rel_err['DY']) ]
    epsilon_err[token] = [ float(i) * float(j) for i, j in zip(epsilon[token], rel_sqrt) ]

    for key, iep in epsilon.iteritems():
        print "\n"
        for num, iparam in enumerate(iep):
            print key, ' : epsilon = ', iparam , ' +/- ', epsilon_err[key][num]
        print "\n"
    '''
