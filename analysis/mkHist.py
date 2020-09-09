from ROOT import gROOT, TChain, TH2D, TCanvas, gStyle, TH1, TMath
from ROOT import TEfficiency, TCanvas, TFile
import ROOT
import os, sys
import numpy as np
from ROOT import array
import time
from collections import OrderedDict

from utils.helper import *

ROOT.ROOT.EnableImplicitMT(12)

ROOT.TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

from optparse import OptionParser
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
(options, args) = parser.parse_args()

DIR = os.getcwd()
dataset= options.dataset
variables=['lep1_pt','lep1_eta','lep2_pt','lep2_eta','mll'] #2d
ntupleDIR= DIR+"/../ntuple/results/"+dataset

start_time = time.time()

#DF= OrderedDict({
#    'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
#    'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/SingleElectron.root' , ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
#    'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_SingleElectron.root' , ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
#})

DF= OrderedDict({
    'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
    'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
    'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
})

signness= OrderedDict({
    'os' : 'lep1_pdgId*lep2_pdgId == -11*11',
    'ss' : 'lep1_pdgId*lep2_pdgId == 11*11'
})

#jie
#ptbin= OrderedDict({
#    'trigpt' : 'lep1_pt > 23 &&  lep2_pt > 23',
#    'highpt' : 'lep1_pt > 25 &&  lep2_pt > 25',
#    'lowpt2' : 'lep1_pt > 25 && lep2_pt > 35',
#    'lowpt1' : 'lep1_pt > 25 &&  lep2_pt <= 35 && lep2_pt > 25',
#    'lowpt0' : 'lep1_pt > 25 &&  lep2_pt <= 25 && lep2_pt > 12'
#})


ptbin= OrderedDict({
    'trigpt' : 'lep1_pt > XXX && lep2_pt > 23',
    'highpt' : 'lep1_pt > XXX && lep2_pt > 35',
    'lowpt2' : 'lep1_pt > XXX && lep2_pt > 25',
    'lowpt1' : 'lep1_pt > XXX && lep2_pt > 25 && lep2_pt <= 35',
    'lowpt0' : 'lep1_pt > XXX && lep2_pt > 12 && lep2_pt <= 25'
})

trig_pt=28
#if '2016' in dataset:
#    trig_pt=32
#elif '2017' in dataset:
#    trig_pt=40
#elif '2018' in dataset:
#    trig_pt=37

ptbin = OrderedDict( zip ( map(lambda x : x, ptbin)  , map(lambda x : ptbin[x].replace( 'XXX' ,'%s' %trig_pt).replace( 'YYY' , '%s' %(trig_pt+5) ) , ptbin )) )

# lepton wp couples with sf
WPs= OrderedDict({
    '2016' : {
        'cutBased'   : 'LepCut2l__ele_cut_WP_Tight80X__mu_cut_Tight80x*LepSF2l__ele_cut_WP_Tight80X__mu_cut_Tight80x'       ,
        'cutBasedSS' : 'LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*LepSF2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x' ,
        'mvaBased'   : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x'       ,
        'mvaBasedSS' : 'LepCut2l__ele_mva_90p_Iso2016_SS__mu_cut_Tight80x*LepSF2l__ele_mva_90p_Iso2016_SS__mu_cut_Tight80x' ,
    },
    '2017' : {
        'mvaBased'   : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBasedSS' : 'LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW',
    },
    '2018' : {
        'mvaBased'   : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBasedSS' : 'LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW',
    }
})

#eta_bin = [ 0. , 1.0 , 1.5 , 2.5 ]
eta_bin = [ 0. , 0.5  , 1.0  , 1.5  , 2.0 , 2.5 ]
etagrid=np.zeros((len(eta_bin)-1,len(eta_bin)-1),dtype=np.object)
for i in range(len(etagrid)):
    for j in range(len(etagrid[i])):
        etagrid[i][j]='abs(lep1_eta)>='+str(eta_bin[i])+' && abs(lep1_eta)<'+str(eta_bin[i+1])+' && abs(lep2_eta)>='+str(eta_bin[j])+' && abs(lep2_eta)<'+str(eta_bin[j+1])

df2histo= OrderedDict()
bins=np.array(eta_bin)

def makeEtaGrid(indf,iterdf,prefix):
    for i in range(len(etagrid)):
        for j in range(len(etagrid[i])):
            prefix_tmp=prefix+"_etabin"+str(i)+"_etabin"+str(j)+"_mll"
            dftmp=iterdf.Filter(etagrid[i][j])
            indf[prefix_tmp]=dftmp.Histo1D( ( prefix_tmp , "%s ; mll [GeV] ; Events" %prefix_tmp , 30, 76.2, 106.2 ), "mll","weights")
    pass

def mkplot():

    rf = ROOT.TFile.Open('hist_%s.root'%(dataset),"RECREATE")

    for idf in DF:
        # weight
        weight='1==1'
        if 'DY' in idf:
            # SFweight2l = puWeight*TriggerEffWeight_2l*Lepton_RecoSF[0]*Lepton_RecoSF[1]*EMTFbug_veto
            # XSWeight = baseW*genWeight
            # METFilter_Common = vent.Flag_goodVertices*\
            #         event.Flag_globalSuperTightHalo2016Filter*\
            #         event.Flag_HBHENoiseFilter*\
            #         event.Flag_HBHENoiseIsoFilter*\
            #         event.Flag_EcalDeadCellTriggerPrimitiveFilter*\
            #         event.Flag_BadPFMuonFilter\
            # GenLepMatch2l = event.Lepton_genmatched[0]*\
            #                 event.Lepton_genmatched[1] \

            common="ptllDYW*SFweight2l*XSWeight*METFilter_MC*genmatch" #GenLepMatch2l
            if '2016' in idf:
                weight="35.92*%s*%s" %(common,WPs['2016']['mvaBased'])
            elif '2017' in idf:
                weight="41.53*%s*%s" %(common,WPs['2017']['mvaBased'])
            elif '2018' in idf:
                weight="59.74*%s*%s" %(common,WPs['2018']['mvaBased'])
        elif 'DATA' in idf:
            common="METFilter_DATA*Trigger_dblEl" #"trigger"
            if '2016' in idf:
                weight="%s*%s" %(common,WPs['2016']['mvaBased'].split('*')[0])
            elif '2017' in idf:
                weight="%s*%s" %(common,WPs['2017']['mvaBased'].split('*')[0])
            elif '2018' in idf:
                weight="%s*%s" %(common,WPs['2018']['mvaBased'].split('*')[0])
        elif 'FAKE' in idf:
            common="METFilter_FAKE*Trigger_dblEl" #trigger"
            if '2016' in idf:
                weight="%s*%s" %(common,WPs['2016']['mvaBased'].split('*')[0].replace('LepCut2l_','fakeW2l').replace('__','_'))
            elif '2017' in idf:
                weight="%s*%s" %(common,WPs['2017']['mvaBased'].split('*')[0].replace('LepCut2l_','fakeW2l').replace('__','_'))
            elif '2018' in idf:
                weight="%s*%s" %(common,WPs['2018']['mvaBased'].split('*')[0].replace('LepCut2l_','fakeW2l').replace('__','_'))
        DYregion = DF[idf].Define('weights',weight) #.Define('abslep1eta','abs(lep1_eta)').Define('abslep2eta','abs(lep2_eta)')

        #SS/OS
        for ireg in signness:
            tmp_df_1 = DYregion.Filter( signness[ireg] , '%s selection' %ireg )
            for iptbin in ptbin:
                tmp_df_2 = tmp_df_1.Filter( ptbin[iptbin] , '%s selection' %iptbin )
                for ivar in variables:
                    if 'eta' in ivar:
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) , '%s_%s_%s_%s ; %s; Events' %(idf,ireg,iptbin,ivar,ivar) , 10 , -2.5 , 2.5 ) , ivar , 'weights' )
                    elif 'pt' in ivar:
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) , '%s_%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,iptbin,ivar,ivar) , 40 , 0. , 200. ) , ivar , 'weights' )
                #################################################################################################################
                    elif ivar=='mll':
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar), '%s_%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,iptbin,ivar,ivar) , 30, 76.2, 106.2 ) , ivar , 'weights' )
                        ## mll in different etabins
                        makeEtaGrid(df2histo,tmp_df_2,'%s_%s_%s'%(idf,iptbin,ireg))
                #################################################################################################################
                    #elif ivar=='2d':
                    #    df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)] = tmp_df_2.Histo2D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) ,' %s_%s_%s_%s ; Lepton eta 1 ; Lepton eta 2 ; Events.' %(idf,ireg,iptbin,ivar), len(bins)-1 , np.asarray(bins,'d') , len(bins)-1 , np.asarray(bins,'d') ) , 'abslep1eta' , 'abslep2eta' , 'weights' )

    map(lambda x: df2histo[x].Write() , df2histo)
    rf.Close()
    pass

def mkvalidation(rf,dataset):
    f = ROOT.TFile.Open(rf,"READ")
    output='plots/%s/validPlot' %dataset
    if not os.path.exists(output): os.system('mkdir -p %s' %output)

    # convert list of branch into key-branch dictionary
    histkeys=[ key.GetName() for key in f.GetListOfKeys() ]
    histlist = OrderedDict( zip( map(lambda x : x, histkeys) , map(lambda x : f.Get(x), histkeys) ) )

    #####################
    # what does it do?
    # 1.) plot 1D kinematics DATA/MC
    # 2.) plot 1D N_SS/N_OS on kinematics?
    # trigpt default
    ptregion='lowpt2' #'trigpt'
    oskeys = filter(lambda x : 'etabin' not in x and ptregion in x and 'os' in x , histkeys)
    sskeys = filter(lambda x : 'etabin' not in x and ptregion in x and 'ss' in x , histkeys)

    #plot 1D STACK kinematics between DATA/MC
    for ireg in [ sskeys , oskeys ]:
        for jvar in variables:
            if jvar=='2d': continue
            regvar = filter( lambda x: jvar in x , ireg )
            insitu = OrderedDict( zip( map(lambda x : x , regvar) , map(lambda x : histlist[x], regvar) ) )
            SaveHisto1D( insitu , regvar[0].strip('%s_' %regvar[0].split('_')[0]) , output , 0, 4, False , True if jvar in [ 'lep1_pt' , 'lep2_pt' ] else False)

    #plot 1D kinematics of SS/OS both for MC and Data
    for idata in [ 'DY' , 'DATA' , 'FAKE' ]:
        map( lambda x, y : SaveRatio( histlist[x] , histlist[y] , idata , x.split('_ss_')[-1] , output ) , sskeys , oskeys  )
    pass

if __name__ == '__main__':

    mkplot()
    mkvalidation('hist_%s.root'%(dataset),dataset)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
