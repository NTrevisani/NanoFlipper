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

nthread=12;
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
yr=['2017']
variables=['lep1eta','lep2eta','lep1pt','lep2pt','mll','2d']
regions=['region','SSnum','OSnum']

start_time = time.time()

for i in Dataset:
    if len(yr)!=0:
        if yr[0] not in i:
            continue

    #Haverster
    DY={}; DATA={}; FAKE={}; HIST={};
    for ireg in regions:
        for ivar in variables:
            DY['%s_%s'%(ireg,ivar)]=[]
            DATA['%s_%s'%(ireg,ivar)]=[]
            FAKE['%s_%s'%(ireg,ivar)]=[]

    print("")
    print(i)
    print("")

    mcDir= Dataset[i]['MC']
    dataDir= Dataset[i]['DATA']
    fakeDir= Dataset[i]['FAKE']
    mcKey= [ f for f in Dataset[i]['mcW'] if f!='common' ]
    dataKey= [ f for f in Dataset[i]['Trig'] ]
    
    mcCommon=Dataset[i]['mcW']['common']
    dataCommon=Dataset[i]['dataW']
    fakeCommon=Dataset[i]['fakeW']

    ###
    Nom = 'lep1pt>20 && lep2pt>20 && lep1pt<200 && lep2pt<200'
    #Zdenom = 'nLepton>=2 && abs(mll-91.2) < 15 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pt[2]<10'
    #Zdenom = 'abs(mll-91.2) < 15 && ( (nLepton==2 && Lepton_pt[0]>25 && Lepton_pt[1]>20) || (nLepton>=3 && Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pt[2]<10) )'
    #Zdenom = 'abs(mll-91.2) < 15 && Alt$(Lepton_pt[0],0)>25 && Alt$(Lepton_pt[1],0)>20 && Alt$(Lepton_pt[2],0)<10'
    SS_num = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)'
    OS_num = '( (Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) || (Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11) )'

    if not os.path.exists('plots'): os.mkdir('plots')
    if not os.path.exists('plots/%s'%i): os.mkdir('plots/%s'%i)
    rf = ROOT.TFile.Open('plots/%s/%s.root'%(i,i),"RECREATE")

    histo={}
    print mcKey
    for inum,j in enumerate(mcKey+dataKey):
        source=''
        if 'DY' in j:
            source=mcDir
        elif '_fake' in j:
            source=fakeDir
        else:
            source=dataDir
        #print '%s : %s/*%s*.root'%(j,source, j.split('_')[0] if 'fake' in j else j )
        DF = ROOT.ROOT.RDataFrame("Events", '%s/*%s*.root'%(source, j.split('_')[0] if 'fake' in j else j ) )

        ## apply nominal condition
        histodf={}
        #Define Denom, array type variable needed defined new column
        #DYregion = DF.Filter('%s && %s' %(Zdenom,Nom), 'DY process selection for %s' %j)

        #Define plotting variable
        DYregion = DF\
                .Define('lep1eta','Lepton_eta[0]')\
                .Define('lep2eta','Lepton_eta[1]')\
                .Define('abslep1eta','abs(Lepton_eta[0])')\
                .Define('abslep2eta','abs(Lepton_eta[1])')\
                .Define('lep1pt','Lepton_pt[0]')\
                .Define('lep2pt','Lepton_pt[1]')\
                .Define('lep3pt','Lepton_pt[2]')
                #.Define('evWeight', '%s*%s'  %(mcCommon,Dataset[i]['mcW'][j]) if 'DY' in j else '%s*%s' %(dataCommon,Dataset[i]['Trig'][j.split('_')[0]]) )

        #Define Weights
        if 'DY' in j:
            DYregion = DYregion.Define('evWeight', '%s*%s' %(mcCommon,Dataset[i]['mcW'][j]) )
            print '%s : %s/*%s*.root'%(j,source, j.split('_')[0] if 'fake' in j else j )
            #print 'weight: %s*%s' %(mcCommon,Dataset[i]['mcW'][j])
        elif 'fake' in j:
            DYregion = DYregion.Define('evWeight', '%s*%s' %(fakeCommon,Dataset[i]['Trig'][j]) )
            print '%s : %s/*%s*.root'%(j,source, j.split('_')[0] if 'fake' in j else j )
            #print 'weight: %s*%s' %(fakeCommon,Dataset[i]['Trig'][j])
        else:
            DYregion = DYregion.Define('evWeight', '%s*%s' %(dataCommon,Dataset[i]['Trig'][j]) )
            print '%s : %s/*%s*.root'%(j,source, j.split('_')[0] if 'fake' in j else j )
            #print 'weight: %s*%s' %(dataCommon,Dataset[i]['Trig'][j])

        #Filter
        DYregion = DYregion.Filter(Nom,"Lepton pT cuts")
        DYregion = DYregion.Filter('abs(mll-91.2) < 15 && ( (nLepton==2 && lep1pt>25 && lep2pt>20) || (nLepton==3 && lep1pt>25 && lep2pt>20 && lep3pt<10) )','lepton cut')
        #Define Selection
        histodf['%s_%s_region' %(i,j)] = DYregion.Filter('1==1','No cut, DrellYan region')
        histodf['%s_%s_SSnum' %(i,j)] = DYregion.Filter( SS_num , 'SS selection for %s' %j)
        histodf['%s_%s_OSnum' %(i,j)] = DYregion.Filter( OS_num , 'OS selection for %s' %j)


        #Variable
        for ivar in variables:
            for idf in histodf:
                if 'eta' in ivar:
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events' %(idf,ivar,ivar) , 10 , -2.5 , 2.5 ) , ivar , 'evWeight' )
                elif 'pt' in ivar:
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events' %(idf,ivar,ivar) , 20 , 0. , 200. ) , ivar , 'evWeight' )
                elif ivar=='mll':
                    histo['%s_%s'%(idf,ivar)]  = histodf[idf].Histo1D( ( '%s_%s' %(idf,ivar) , '%s_%s ; %s [GeV]; Events' %(idf,ivar,ivar) , 80 , 70. , 110. ) , ivar , 'evWeight' )
                elif ivar=='2d':
                    histo['%s_2d'%idf] = histodf[idf].Histo2D( ( '%s_2d'%idf ,' %s ; Lepton_eta 0 ; Lepton_eta 1 ; Events.' %idf, len(bins)-1 , np.asarray(bins,'d') ,\
                                                               len(bins)-1 , np.asarray(bins,'d') ) , 'abslep1eta' , 'abslep1eta' , 'evWeight' )
    
    map(lambda x: histo[x].Write() , histo)

    rf.Close();

######################################################################

print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
