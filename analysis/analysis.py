import ROOT
from ROOT import gROOT , gStyle
import os, sys
import time
from collections import OrderedDict

sys.path.append('%s/utils' %os.getcwd() )

ROOT.ROOT.EnableImplicitMT(12)

ROOT.TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

DIR = os.getcwd()

from optparse import OptionParser
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
parser.add_option("-n","--ntuplefolder", action="store", type="string", dest="ntuplefolder", default="%s/../ntuple/results" %DIR )
(options, args) = parser.parse_args()
ntuplefolder = options.ntuplefolder
dataset= options.dataset
year = dataset.split('_')[-1]
ntupleDIR= "%s/%s" %( ntuplefolder , dataset )

variables=[ 'lep1_pt' , 'lep1_eta' , 'lep2_pt' , 'lep2_eta' , 'lep3_pt' , 'lep3_eta' , 'mll' , 'Mll' , '2d' ]

signness= OrderedDict({
    'os' : 'lep1_pdgId*lep2_pdgId == -11*11',
    'ss' : 'lep1_pdgId*lep2_pdgId == 11*11'
})

# SingleElectron
# 2016 : HLT Ele27 WPTight Gsf v* || HLT Ele25 eta2p1 WPTight Gsf v*
# 2017 : HLT Ele35 WPTight Gsf v*
# 2018 : EGamma : HLT Ele32 WPTight Gsf v* || HLT Ele35 WPTight Gsf v* || HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*

# DoubleEG
# 2016 : HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL DZ v*
# 2017 : HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*
# 2018 : EGamma : HLT Ele32 WPTight Gsf v* || HLT Ele35 WPTight Gsf v* || HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*

triggers = {
    'Trigger_dblEl' : {
        "2016" : [ "28" , "17" ] , # 23+5 ; 12+5
        "2017" : [ "28" , "17" ] , # 23+5 ; 12+5
        "2018" : [ "40" , "17" ]   # 32+5 ; 12+5
    },
    'Trigger_sngEl' : {
        "2016" : [ "32" , "15" ] , # 27+5
        "2017" : [ "40" , "15" ] , # 35+5
        "2018" : [ "40" , "15" ]   # 35+5
    }
}

commontrig="Trigger_sngEl"
commonMC="SFweight2l*XSWeight*METFilter_MC*GenLepMatch2l*ptllDYW"

dataset_cfg = OrderedDict({
    '2016' : {
        'MC_w'                     : '35.92*%s' %commonMC ,
        'DATA_w'                   : 'METFilter_DATA*%s' %commontrig ,
        'WPs'                      : {
            'mvaBased'             : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x'       ,
            'mvaBased_tthmva'      : 'LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x*LepCut2l__ele_mu_HWW_ttHMVA*LepSF2l__ele_mu_HWW_ttHMVA',
            'fake_mvaBased'        : 'fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x' ,
            'fake_mvaBased_tthmva' : 'fakeW2l_ele_mva_90p_Iso2016_tthmva_70_mu_cut_Tight80x_tthmva_80'
        }
    },
    '2017' : {
        'MC_w'                     : '41.53*%s' %commonMC ,
        'DATA_w'                   : 'METFilter_DATA*%s' %commontrig ,
        'WPs'                      : {
            'mvaBased'             : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
            'mvaBased_tthmva'      : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_tthMVA*HWW_ttHMVA_SF_2l',
            'fake_mvaBased'        : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
            'fake_mvaBased_tthmva' : 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
        }
    },
    '2018' : {
        'MC_w'                     : '59.74*%s' %commonMC ,
        'DATA_w'                   : 'METFilter_DATA*%s' %commontrig ,
        'WPs' : {
            'mvaBased'             : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
            'mvaBased_tthmva'      : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_tthMVA*HWW_ttHMVA_SF_2l' ,
            'fake_mvaBased'        : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
            'fake_mvaBased_tthmva' : 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
        }
    }
})

ptbin = OrderedDict()
ptbin['lowpt']    = 'lep1_pt >= %s && lep1_pt < 200 && lep2_pt > %s && lep2_pt <= 20' %( triggers[commontrig][year][0] , triggers[commontrig][year][1]  )
ptbin['highpt']   = 'lep1_pt >= %s && lep1_pt < 200 && lep2_pt > 20 && lep2_pt < 200' %( triggers[commontrig][year][0] )

etabin = [ 0. , 1.4 , 2.5 ]
#etabin = [ -2.5 , -1.4 , 0. , 1.4 , 2.5 ]

from utils.helper import *
from utils.mkroot import *
from utils.mkplot import *
from utils.mkzfit import *
from utils.mkflipsf import *

if __name__ == '__main__':

    start_time = time.time()
    year = dataset.split('_')[-1]
    MC = [ "DYJetsToLL_M-50-LO_ext2.root" ]
    DATA = [ "SingleElectron.root" ] #"DoubleEG.root" ]
    
    MC   = map( lambda x : ntupleDIR+"/"+x , MC     )
    DATA = map( lambda x : ntupleDIR+"/"+x , DATA  )

    print( "MC   : ", MC )
    print( "DATA : ", DATA )

    # DF loaded here
    DF= OrderedDict({
        'MC_%s' %year   : ROOT.ROOT.RDataFrame( "flipper" , MC   ) ,
        'DATA_%s' %year : ROOT.ROOT.RDataFrame( "flipper" , DATA )
    })
    
    presel="lep1_pt > %s && lep2_pt > %s" %( triggers[commontrig][year][0] , triggers[commontrig][year][1] )
    #presel="1==1"

    info = [ dataset_cfg[year] , presel , signness , ptbin , etabin , variables ]
    
    for idataset in [ "nanov5_2016" , "nanov5_2017" , "nanov5_2018" ] :
        if idataset != "nanov5_2016" : continue
        mkroot( idataset , DF , info , "mvaBased_tthmva" );
        mkplot( idataset , info )
        mkzfit( idataset , info )
    mkflipsf( info )

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
