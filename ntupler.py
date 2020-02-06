from ROOT import gROOT, TChain, TH2D, TCanvas, gStyle, TH1, TMath
from ROOT import TEfficiency, TCanvas, TFile
import ROOT
import os, sys
import numpy as np
from ROOT import array
import time

from datasets import Dataset

#bins=np.array([ 0. , 0.5 , 1. , 1.5 , 2.5])
bins=np.array([ 0. , 0.5 , 1. , 1.5 , 2.0 , 2.5])

nthread=9;
ROOT.ROOT.EnableImplicitMT(nthread)

#VAR='abs(Lepton_eta[0]):abs(Lepton_eta[1])'

TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

############# BTAG
#ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

#calib = ROOT.BTagCalibration("csv", "")
#reader = ROOT.BTagCalibrationReader(0, "central")  # 0 is for loose op
#reader.load(calib, 0, "comb")  # 0 is for b flavour, "comb" is the measurement type

# in your event loop
#reader.eval(0, 1.2, 30.)  # jet flavor, absolute eta, pt
###################

btag=False
yr=[]
variables=['lep1eta','lep2eta','lep1pt','lep2pt','mll','2d']
regions=['region','SSnum','OSnum']

start_time = time.time()

for i in Dataset:
    if len(yr)!=0:
        if yr[0] not in i:
            continue

    #Haverster
    DY={}; DATA={}; HIST={};
    for ireg in regions:
        for ivar in variables:
            DY['%s_%s'%(ireg,ivar)]=[]
            DATA['%s_%s'%(ireg,ivar)]=[]

    print("")
    print(i)
    print("")
    if not os.path.exists('plots'): os.mkdir('plots')
    if not os.path.exists('plots/%s'%i): os.mkdir('plots/%s'%i)
    rf = ROOT.TFile.Open('plots/%s/%s.root'%(i,i),"RECREATE")

    mcDir= Dataset[i]['MC']
    dataDir= Dataset[i]['DATA']
    mcKey= [ f for f in Dataset[i]['mcW'] if f!='common' ]
    dataKey= [ f for f in Dataset[i]['Trig'] ]

    mcCommon=Dataset[i]['mcW']['common']
    dataCommon=Dataset[i]['dataW']

    ###
    Nom = 'Lepton_pt[0]>20 && Lepton_pt[1]>20 && Lepton_pt[0]<200 && Lepton_pt[1]<200'
    #Zdenom = 'nLepton>=2 && abs(mll-91.2) < 15 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pt[2]<10'
    Zdenom = 'abs(mll-91.2) < 15 && ( (nLepton==2 && Lepton_pt[0]>25 && Lepton_pt[1]>20) || (nLepton==3 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pt[2]<10) )'
    SS_num = '( ( Lepton_pdgId[0]==11 && Lepton_pdgId[1]==11 ) || ( Lepton_pdgId[0]==-11 && Lepton_pdgId[1]==-11 ) )'
    OS_num = '( ( Lepton_pdgId[0]==-11 && Lepton_pdgId[1]==11 ) || ( Lepton_pdgId[0]==11 && Lepton_pdgId[1]==-11 ) )'

    histo={}
    print mcKey
    for inum,j in enumerate(mcKey+dataKey):
        print '%s : %s/*%s*.root'%(j,mcDir if 'DY' in j else dataDir,j)
        DF = ROOT.ROOT.RDataFrame("Events", '%s/*%s*.root'%(mcDir if 'DY' in j else dataDir,j) )

        ## apply nominal condition
        histodf={}
        #Define Denom, array type variable needed defined new column
        DYregion = DF.Filter('%s && %s' %(Zdenom,Nom), 'DY process selection for %s' %j)

        #Define plotting variable
        DYregion = DYregion\
                .Define('Lep1eta','abs(Lepton_eta[0])')\
                .Define('Lep2eta','abs(Lepton_eta[1])')\
                .Define('lep1eta','Lepton_eta[0]')\
                .Define('lep2eta','Lepton_eta[1]')\
                .Define('lep1pt','abs(Lepton_pt[0])')\
                .Define('lep2pt','abs(Lepton_pt[1])')\
                .Define('evWeight', '%s*%s'  %(mcCommon,Dataset[i]['mcW'][j]) if 'DY' in j else '%s*%s' %(dataCommon,Dataset[i]['Trig'][j]) )

        #Define Selection
        histodf['%s_%s_region' %(i,j)] = DYregion.Filter('1==1','No cut, DrellYan region')
        histodf['%s_%s_SSnum' %(i,j)] = DYregion.Filter('%s && %s' %(SS_num,Nom), 'SS selection for %s' %j)
        histodf['%s_%s_OSnum' %(i,j)] = DYregion.Filter('%s && %s' %(OS_num,Nom), 'OS selection for %s' %j)

        #Variable
        for ivar in variables:
            for idf in histodf:
                if 'eta' in ivar:
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events/1 GeV' %(idf,ivar,ivar) , 60 , -3. , 3. ) , ivar , 'evWeight' )
                elif 'pt' in ivar:
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events/5 GeV' %(idf,ivar,ivar) , 40 , 0. , 200. ) , ivar , 'evWeight' )
                elif ivar=='mll':
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events/5 GeV' %(idf,ivar,ivar) , 80 , 70. , 110. ) , ivar , 'evWeight' )
                elif ivar=='2d':
                    histo['%s_2d'%idf] = histodf[idf].Histo2D( ( '%s_2d'%idf ,' %s ; Lepton_eta 0 ; Lepton_eta 1 ; Events.' %idf, len(bins)-1 , np.asarray(bins,'d') ,\
                                                               len(bins)-1 , np.asarray(bins,'d') ) , 'Lep1eta' , 'Lep2eta' , 'evWeight' )
    
    map(lambda x: histo[x].Write() , histo)

    rf.Close();

######################################################################

print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
