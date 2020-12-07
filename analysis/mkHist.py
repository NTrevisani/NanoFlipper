import ROOT
from ROOT import gROOT , gStyle
import os, sys
import time
from collections import OrderedDict

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

ntupleDIR= DIR+"/../ntuple/results/"+ dataset

signness= OrderedDict({
    'os' : 'lep1_pdgId*lep2_pdgId == -11*11',
    'ss' : 'lep1_pdgId*lep2_pdgId == 11*11'
})

# lepton wp couples with sf
WPs = OrderedDict({
    '2016' : {
        'mvaBased'            : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x'       ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepCut2l__ele_mu_HWW_tthMVA*HWW_ttHMVA_SF_2l',
        'fake_mvaBased'       : 'fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x' ,
        'fake_mvaBased_tthmva': 'fakeW2l_ele_mva_90p_Iso2016_tthmva_70_mu_cut_Tight80x_tthmva_80'
    },
    '2017' : {
        'mvaBased'            : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_tthMVA*HWW_ttHMVA_SF_2l',
        'fake_mvaBased'       : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
        'fake_mvaBased_tthmva': 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
    },
    '2018' : {
        'mvaBased'            : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
        'mvaBased_tthmva'     : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_tthMVA*HWW_ttHMVA_SF_2l' ,
        'fake_mvaBased'       :	'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
        'fake_mvaBased_tthmva':	'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
    }
})

#fix
ptbin= OrderedDict({
    'lowpt'  : 'lep1_pt >= 25 && lep1_pt < 200 && lep2_pt > 15 && lep2_pt <= 20',
    'highpt' : 'lep1_pt >= 25 && lep1_pt < 200 && lep2_pt > 20 && lep2_pt < 200',
    })

print(ptbin)

eta_bin = [ 0. , 1.444 , 2.5 ]

from utils.helper import *
from utils.mkroot import *
from utils.mkplot import *

if __name__ == '__main__':
    
    start_time = time.time()
    
    # DF loaded here
    DF= OrderedDict({
        'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
        'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
        'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
    })

    
    presel="nLepton==2"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL DZ v*
    if dataset == "nanov5_2016" :
        presel+=" && lep1_pt>28 && lep2_pt>15"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*
    elif dataset == "nanov5_2017" :
        presel+=" && lep1_pt>35 && lep2_pt>15"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*
    elif dataset == "nanov5_2018" :
        presel+=" && lep1_pt>35 && lep2_pt>15"

    mkroot( dataset , DF , eta_bin , presel , "mvaBased_tthmva" ); # mk
    #mkroot( dataset , DF , eta_bin , presel , "mvaBased" );
    mkplot( dataset , False ) # no fake
    mkplot( dataset , True ) # with fake

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
