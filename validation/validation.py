import ROOT
from ROOT import gROOT , gStyle
import os, sys
import time
from collections import OrderedDict

sys.path.append('%s/../analysis/utils' %os.getcwd() )  
from helper import *
from workflow import *

ROOT.ROOT.EnableImplicitMT(12)

ROOT.TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

# hard-coded variables
def PrepareVariable( df_in , name , dataset_ , testname_ , isSF=0 ):
    # compute with SF
    if isSF == 1 :
        df_in = df_in.Define( 'SF' , 'getSF( lep1_pt , lep1_eta , lep2_pt , lep2_eta , lep1_pdgId , lep2_pdgId )' ).Define( 'totalW' , 'SF*weights' )
    # compute with charge flip mc
    elif isSF == 2 :
        df_in = df_in.Define( 'f_mc' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , 0 )' ).Define( 'totalW' , 'f_mc*weights' )
    # compute with charge flip data
    elif isSF == 3 :
        df_in = df_in.Define( 'f_data' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , 1 )' ).Define( 'totalW' , 'f_data*weights' )
    else:
        if name != "DATA" : sys.exit()
        df_in = df_in.Define( 'totalW' , 'weights' )
        
    h = OrderedDict() ; weight_ = 'totalW'
    h[ name + '_mll' ]     = df_in.Histo1D( ( name + '_mll'      , '%s %s ; mll [GeV]     ; Events' %( testname_ , dataset_ ) , 30, 76.2, 106.2 ) , 'mll'      , weight_ )
    h[ name + '_lep1_eta'] = df_in.Histo1D( ( name + '_lep1_eta' , '%s %s ; lep1_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep1_eta' , weight_ )
    h[ name + '_lep2_eta'] = df_in.Histo1D( ( name + '_lep2_eta' , '%s %s ; lep2_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep2_eta' , weight_ )
    h[ name + '_lep1_pt']  = df_in.Histo1D( ( name + '_lep1_pt'  , '%s %s ; lep1_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , weight_ )
    h[ name + '_lep2_pt']  = df_in.Histo1D( ( name + '_lep2_pt'  , '%s %s ; lep2_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , weight_ )
    h[ name + '_SF']       = df_in.Histo1D( ( name + '_SF'       , '%s %s ; SF ; Events' %( testname_ , dataset_ ) , 100 , 0. , 10.  )            , 'SF'  , weight_ )
    h[ name + '_totalW']   = df_in.Histo1D( ( name + '_totalW'   , '%s %s ; totalW ; Events' %( testname_ , dataset_ ) , 100 , 0. , 10.  )        , 'totalW'  , weight_ )
    return h
pass

DIR = os.getcwd()

ntuple={
    'nanov5_2016' : {
        'DATA' : [ "SingleElectron.root" ],
        'MC'   : [ "DYJetsToLL_M-50-LO_ext2.root" ]
    },
    'nanov5_2017' : {
        'DATA' : [ "SingleElectron.root" ],
        'MC'   : [ "DYJetsToLL_M-50-LO_ext1.root" ]
    },
    'nanov5_2018' : {
        'DATA' : [ "EGamma.root" ],
        'MC'   : [ "DYJetsToLL_M-50-LO.root" ]
    }
}

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

cfg = OrderedDict({
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
            'mvaBased_tthmva'      : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_ttHMVA*LepSF2l__ele_mu_HWW_ttHMVA',
            'fake_mvaBased'        : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
            'fake_mvaBased_tthmva' : 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
        }
    },
    '2018' : {
        'MC_w'                     : '59.74*%s' %commonMC ,
        'DATA_w'                   : 'METFilter_DATA*%s' %commontrig ,
        'WPs' : {
            'mvaBased'             : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW'      ,
            'mvaBased_tthmva'      : 'LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mu_HWW_ttHMVA*LepSF2l__ele_mu_HWW_ttHMVA' ,
            'fake_mvaBased'        : 'fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW',
            'fake_mvaBased_tthmva' : 'fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80'
        }
    }
})

if __name__ == '__main__':

    start_time = time.time()
    for idataset in [ "nanov5_2016" , "nanov5_2017" , "nanov5_2018" ] :
        
        year = idataset.split('_')[-1]
        ntupleDIR= "%s/../ntuple/results/%s" %( DIR , idataset )

        output= 'plots/%s' %( idataset )
        
        MC   = map( lambda x : ntupleDIR+"/"+x , ntuple[idataset]['MC']   )
        DATA = map( lambda x : ntupleDIR+"/"+x , ntuple[idataset]['DATA'] )
        
        print( "MC   : ", MC )
        print( "DATA : ", DATA )
    
        DF= OrderedDict({
            'MC_%s' %year   : ROOT.ROOT.RDataFrame( "flipper" , MC   ) ,
            'DATA_%s' %year : ROOT.ROOT.RDataFrame( "flipper" , DATA )
        })

        presel="lep1_pt > %s && lep2_pt > %s" %( triggers[commontrig][year][0] , triggers[commontrig][year][1] )
        wp_ = "mvaBased_tthmva"
        ROOT.loadSF2D( "../analysis/data/chargeFlip_%s_SF.root" %idataset )
                
        #begins
        histo_pair = {}
        for idf in DF :
            # name                                                                                                                                                                                              
            name = idf.split('_')[0]
            print(" name : ", name )
            # define weight                                                                                                                                                                                     
            df = DF[idf].Define( 'weights' , '%s*%s' %( cfg[year]['%s_w'%name] , cfg[year]['WPs'][wp_] if name == 'MC' else cfg[year]['WPs'][wp_].split('*LepSF')[0] ) )
            print( " Common weights : %s*%s" %( cfg[year]['%s_w'%name] , cfg[year]['WPs'][wp_] if name == 'MC' else cfg[year]['WPs'][wp_].split('*LepSF')[0] ) )

            # preselection                                                                                                                                                                                      
            df = df.Filter( presel , "Preselection : %s" %presel )
            # SS/OS region
            # SF (D/M) x MC_SS = DATA_SS
            df_tmp = df.Filter( signness['ss'] , '%s selection' %signness['ss'] )
            
            if name == "MC" :
                histo_pair[name] = PrepareVariable( df_tmp , name , idataset , "Scale factor method" , 1 )
            else:
                histo_pair[name] = PrepareVariable( df_tmp , name , idataset , "Scale factor method" )
            ###################
        output += output + "/SF_application"
        if not os.path.exists(output): os.system('mkdir -p %s' %output)
        for imc, idata in zip( histo_pair['MC'] , histo_pair['DATA'] ) :
            #print( "imc : ", imc , " ; idata : ", idata )
            #print( "imc : ", histo_pair['MC'][imc] , " ; idata : ", histo_pair['DATA'][idata] )
            saveHisto1DCompare( histo_pair['MC'][imc].GetPtr() , histo_pair['DATA'][idata].GetPtr() , output , imc.split('MC_')[-1] , 0, 4, False, True if 'pt' in imc else False )
            
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
