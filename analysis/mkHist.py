from ROOT import gROOT, TH2D, TCanvas, gStyle, TH1, TMath
from ROOT import TEfficiency, TCanvas, TFile
import ROOT
import os, sys
import numpy as np
from ROOT import array
import time
from collections import OrderedDict
from array import array as arr

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
variables=['lep1_pt','lep1_eta','lep2_pt','lep2_eta','mll','2d']
ntupleDIR= DIR+"/../ntuple/results/"+dataset

start_time = time.time()

signness= OrderedDict({
    'os' : 'lep1_pdgId*lep2_pdgId == -11*11',
    'ss' : 'lep1_pdgId*lep2_pdgId == 11*11'
})

# lepton wp couples with sf
WPs= OrderedDict({
    '2016' : {
        'mvaBased'            : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x'       ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepCut2l_ttHMVA*LepSF2l_ttHMVA',
        'fake_mvaBased'       : 'fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x' ,
        'fake_mvaBased_tthmva': 'fakeW2l_ele_mva_90p_Iso2016_tthmva_70_mu_cut_Tight80x_tthmva_80'
    },
    '2017' : {
        'mvaBased'            : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l_ttHMVA*LepSF2l_ttHMVA',
        'fake_mvaBased'       : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
        'fake_mvaBased_tthmva': 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
    },
    '2018' : {
        'mvaBased'            : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l_ttHMVA*LepSF2l_ttHMVA' ,
        'fake_mvaBased'       :	'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
        'fake_mvaBased_tthmva':	'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
    }
})

#fix
ptbin= OrderedDict({
    'lowpt'  : 'lep1_pt >= 30 && lep1_pt < 200 && lep2_pt >= 13 && lep2_pt < 30',
    'highpt' : 'lep1_pt >= 30 && lep1_pt < 200 && lep2_pt >= 30 && lep2_pt < 200',
    })

# bin1 has negative value on DY
# eta_bin = [ 0. , 1.0 , 1.5 , 2.5 ]
#ptbin= OrderedDict({
#    'bin1'  : 'lep1_pt >= 25 && lep1_pt < 45 && lep2_pt >= 13 && lep2_pt < 45',
#    'bin2'  : 'lep1_pt >= 45 && lep1_pt < 200 && lep2_pt >= 13 && lep2_pt < 45',
#    'bin3'  : 'lep1_pt >= 45 && lep1_pt < 200 && lep2_pt >= 45 && lep2_pt < 200',
#})

print ptbin

#eta_bin = [ 0. , 1.0 , 1.5 , 2.5 ]
#eta_bin = [ 0. , 0.5  , 1.0  , 1.5  , 2.0 , 2.5 ]
eta_bin = [ 0. , 1.0  , 1.5  , 2.0 , 2.5 ]

etagrid=np.zeros((len(eta_bin)-1,len(eta_bin)-1),dtype=np.object)
for i in range(len(etagrid)):
    for j in range(len(etagrid[i])):
        etagrid[i][j]='abs(lep1_eta)>='+str(eta_bin[i])+' && abs(lep1_eta)<'+str(eta_bin[i+1])+' && abs(lep2_eta)>='+str(eta_bin[j])+' && abs(lep2_eta)<'+str(eta_bin[j+1])

bins=np.array(eta_bin)

def makeEtaGrid(indf,iterdf,prefix):
    for i in range(len(etagrid)):
        for j in range(len(etagrid[i])):
            prefix_tmp=prefix+"_etabin"+str(i)+"_etabin"+str(j)+"_mll"
            dftmp=iterdf.Filter(etagrid[i][j])
            indf[prefix_tmp]=dftmp.Histo1D( ( prefix_tmp , "%s ; mll [GeV] ; Events" %prefix_tmp , 30, 76.2, 106.2 ), "mll","weights")
    pass

def addWeights( df_in , name ):

    dfout = df_in[name]

    weight='1==1'

    wp = 'mvaBased_tthmva';

    if 'DY' in name:
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

        common="ptllDYW*SFweight2l*XSWeight*METFilter_MC*GenLepMatch2l" #*genmatch" #GenLepMatch2l
        if '2016' in name:
            weight="35.92*%s*%s" %( common , WPs['2016'][wp] )
        elif '2017' in name:
            weight="41.53*%s*%s" %(common,WPs['2017'][wp])
        elif '2018' in name:
            weight="59.74*%s*%s" %(common,WPs['2018'][wp])
    elif 'DATA' in name:
        common="METFilter_DATA*Trigger_dblEl"
        if '2016' in name:
            weight="%s*%s" %( common , WPs['2016'][wp].replace( WPs['2016'][wp].split('*')[-1], "(1==1)" ) )
        elif '2017' in name:
            weight="%s*%s" %(common ,  WPs['2017'][wp].replace( WPs['2017'][wp].split('*')[-1], "(1==1)" ) )
        elif '2018' in name:
            weight="%s*%s" %(common ,  WPs['2018'][wp].replace( WPs['2018'][wp].split('*')[-1], "(1==1)" ) )
    elif 'FAKE' in name:
        common="METFilter_FAKE*Trigger_dblEl"
        if '2016' in name:
            weight="%s*%s" %( common , WPs['2016']['fake_'+wp] )
        elif '2017' in name:
            weight="%s*%s" %( common , WPs['2017']['fake_'+wp] )
        elif '2018' in name:
            weight="%s*%s" %( common , WPs['2018']['fake_'+wp] )

    return dfout.Define('weights',weight).Define('abslep1eta','abs(lep1_eta)').Define('abslep2eta','abs(lep2_eta)')

def mkplot( dataset_ , DFS ):

    rf = ROOT.TFile.Open('hist_%s.root'%(dataset_),"RECREATE")

    # this is for validation
    dfval={}
    df2histo= OrderedDict()

    for idf in DFS:
        DYregion = addWeights( DFS , idf )
        # trigger threshold
        #DYregion = DYregion.Filter("lep1_pt > 25","Trigger Threshold")

        #SS/OS
        for ireg in signness:
            tmp_df_1 = DYregion.Filter( signness[ireg] , '%s selection' %ireg )
            for ivar in variables:
                if 'eta' in ivar:
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar) , '%s_%s_%s ; %s; Events' %(idf,ireg,ivar,ivar) , 10 , -2.5 , 2.5 ) , ivar , 'weights' )
                elif 'pt' in ivar:
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar) , '%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,ivar,ivar) , 40 , 0. , 200. ) , ivar , 'weights' )
                #################################################################################################################
                elif ivar=='2d':
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)] = tmp_df_1.Histo2D( ( '%s_%s_%s'%(idf,ireg,ivar) ,' %s_%s_%s ; Lepton eta 1 ; Lepton eta 2 ; Events.' %(idf,ireg,ivar), len(bins)-1 , np.asarray(bins,'d') , len(bins)-1 , np.asarray(bins,'d') ) , 'abslep1eta' , 'abslep2eta' , 'weights' )
                elif ivar=='mll':
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar), '%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,ivar,ivar) , 30, 76.2, 106.2 ) , ivar , 'weights' )
                    ## mll in different etabins and ptbins
                    for iptbin in ptbin:
                        tmp_df_2 = tmp_df_1.Filter( ptbin[iptbin] , '%s selection' %iptbin )
		        makeEtaGrid( df2histo , tmp_df_2 , 'analysis_%s_%s_%s'%(idf,iptbin,ireg) )

    map(lambda x: df2histo[x].Write() , df2histo)
    rf.Close()

    pass

def mkval_prefit( rf , plotFake ):

    f = ROOT.TFile.Open(rf,"READ")
    output= 'plots/%s/mkHist_validation/noFake' %( dataset ) if not plotFake else 'plots/%s/mkHist_validation/withFake' %( dataset )
    if not os.path.exists(output): os.system('mkdir -p %s' %output)

    # convert list of branch into key-branch dictionary
    histkeys=[ key.GetName() for key in f.GetListOfKeys() ]
    histlist = OrderedDict( zip( map(lambda x : x, histkeys) , map(lambda x : f.Get(x), histkeys) ) )

    #####################

    oskeys = filter(lambda x : 'etabin' not in x and 'os' in x , histkeys)
    sskeys = filter(lambda x : 'etabin' not in x and 'ss' in x , histkeys)
    if not plotFake:
        oskeys = filter(lambda x : 'FAKE' not in x , oskeys)
        sskeys = filter(lambda x : 'FAKE' not in x , sskeys)

    #plot 1D STACK kinematics between DATA/MC
    for ireg in [ sskeys , oskeys ]:
        for jvar in variables:
            if jvar=='2d': continue
            regvar = filter( lambda x: jvar in x , ireg )
            insitu = OrderedDict( zip( map(lambda x : x , regvar) , map(lambda x : histlist[x], regvar) ) )
            SaveHisto1D( insitu , regvar[0].strip('%s_' %regvar[0].split('_')[0]) , output , 0, 4, False , True if jvar in [ 'lep1_pt' , 'lep2_pt' ] else False , False )

    #plot 1D kinematics of SS/OS both for MC and Data
    for sskey, oskey in zip ( sskeys , oskeys ):
        #print 'sskey : ', sskey , ' ; oskey : ', oskey
        h_sskey = histlist[sskey] ; h_oskey = histlist[oskey]
        SaveRatio( h_sskey , h_oskey , sskey , output )
    pass

if __name__ == '__main__':

    #ptbin__use =

    # use both dataset
    # DF loaded here
    #DF= OrderedDict({
    #    'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
    #    'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/SingleElectron.root' , ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
    #    'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_SingleElectron.root' , ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
    #})

    # use doubleEle
    DF= OrderedDict({
        'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
        'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
        'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
    })

    # use singleElectron
    #DF= OrderedDict({
        #'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
        #'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/SingleElectron.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
        #'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_SingleElectron.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
        #})

    mkplot( dataset , DF ); # mk
    mkval_prefit( 'hist_%s.root'%(dataset) , False ) #toggle Fake
    mkval_prefit( 'hist_%s.root'%(dataset) , True ) #toggle Fake

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
