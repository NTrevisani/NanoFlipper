import ROOT
from ROOT import gROOT , gStyle
import os, sys
import time
from collections import OrderedDict

sys.path.append('%s/../analysis/utils' %os.getcwd() )  
from helper import *
#from workflow import *

ROOT.ROOT.EnableImplicitMT(12)

ROOT.TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

# hard-coded variables
def PrepareVariable( df_in , name , dataset_ , testname_ , isSF=0 ):
        
    h = OrderedDict() ; weight_ = 'weights'
    h[ name + '_mll' ]     = df_in.Histo1D( ( name + '_mll'      , '%s %s ; mll [GeV]     ; Events' %( testname_ , dataset_ ) , 30, 76.2, 106.2 ) , 'mll'      , weight_ )
    h[ name + '_lep1_eta'] = df_in.Histo1D( ( name + '_lep1_eta' , '%s %s ; lep1_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep1_eta' , weight_ )
    h[ name + '_lep2_eta'] = df_in.Histo1D( ( name + '_lep2_eta' , '%s %s ; lep2_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep2_eta' , weight_ )
    h[ name + '_lep1_pt']  = df_in.Histo1D( ( name + '_lep1_pt'  , '%s %s ; lep1_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , weight_ )
    h[ name + '_lep2_pt']  = df_in.Histo1D( ( name + '_lep2_pt'  , '%s %s ; lep2_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , weight_ )
    h[ name + '_totalW']   = df_in.Histo1D( ( name + '_totalW'   , '%s %s ; totalW ; Events' %( testname_ , dataset_ ) , 100 , 0. , 10.  )        , 'weights'  , weight_ )
    return h
pass

DIR = os.getcwd()

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
        "2018" : [ "28" , "17" ]   # 23+5 ; 12+5
    },
    'Trigger_sngEl' : {
        "2016" : [ "32" , "15" ] , # 27+5
        "2017" : [ "40" , "15" ] , # 35+5
        "2018" : [ "40" , "15" ]   # 35+5
    }
}

if __name__ == '__main__':

    ################# CONDITION
    alterMC=False
    #commontrig="Trigger_sngEl"
    commontrig="Trigger_dblEl"
    withSF=True
    commonMC="SFweight2l*XSWeight*METFilter_MC*GenLepMatch2l*ptllDYW*sf3"
    ################# CONDITION

    ntuple={
        'nanov5_2016' : {
            'DATA' : [ "SingleElectron.root" , "DoubleEG.root" ],
            'MC'   : [ "DYJetsToLL_M-50-LO_ext2.root" , "DYJetsToLL_M-50.root" ]
        },
        'nanov5_2017' : {
            'DATA' : [ "SingleElectron.root" , "DoubleEG.root" ],
            'MC'   : [ "DYJetsToLL_M-50-LO_ext1.root" , "DYJetsToLL_M-50_ext1.root" ]
        },
        'nanov5_2018' : {
            'DATA' : [ "EGamma.root" ],
            'MC'   : [ "DYJetsToLL_M-50-LO.root" , "DYJetsToLL_M-50_ext2.root" ]
        }
    }

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

    start_time = time.time()
    for idataset in [ "nanov5_2016" , "nanov5_2017" , "nanov5_2018" ] :
        
        year              = idataset.split('_')[-1]
        ntupleDIR         = "%s/../ntuple/results/%s"                   %( DIR , idataset )
        process_ntupleDIR = "%s/ntuple4Val/%s"                          %( DIR , idataset )
        flipfiles         = "%s/../analysis/data/chargeFlip_%s_SF.root" %( DIR , idataset )
        output= 'plots/%s' %( idataset )
        if not os.path.exists(process_ntupleDIR): os.system( 'mkdir -p %s' %process_ntupleDIR )
        
        # process SF
        for iroot in os.listdir(ntupleDIR) :
            if 'DY' in iroot :
                if alterMC and not 'LO' in iroot :
                    print("Processing NLO DY sf")
                    os.system( "root -l -q \'process_SF.C( \"%s/%s\" , \"%s/%s\" , \"%s\" )\' " %( ntupleDIR , iroot , process_ntupleDIR , iroot , flipfiles )  )
                elif not alterMC and 'LO' in iroot :
                    print("Processing LO DY sf")
                    os.system( "root -l -q \'process_SF.C( \"%s/%s\" , \"%s/%s\" , \"%s\" )\' " %( ntupleDIR , iroot , process_ntupleDIR , iroot , flipfiles )  )
            else:
                print("Its data, skip")
                os.system( "scp %s/%s %s/%s" %( ntupleDIR , iroot , process_ntupleDIR , iroot ) )
        
        MC   = map( lambda x : process_ntupleDIR+"/"+x , ntuple[idataset]['MC']   )
        DATA = map( lambda x : process_ntupleDIR+"/"+x , ntuple[idataset]['DATA'] )

        #filter DATA
        if idataset != "nanov5_2018" :
            if commontrig == "Trigger_sngEl" : DATA = [ i for i in DATA if "SingleElectron" in i ]
            if commontrig == "Trigger_dblEl" : DATA = [ i for i in DATA if "DoubleEG" in i ]
        #filter MC  
        if alterMC :
            MC = [ i for i in MC if "LO" not in i ]
        else :
            MC = [ i for i in MC if "LO" in i ]
        
        print( "MC   : ", MC )
        print( "DATA : ", DATA )
    
        DF= OrderedDict({
            'MC_%s' %year   : ROOT.ROOT.RDataFrame( "flipper" , MC   ) ,
            'DATA_%s' %year : ROOT.ROOT.RDataFrame( "flipper" , DATA )
        })

        #presel="lep1_pt > %s && lep2_pt > %s" %( triggers[commontrig][year][0] , triggers[commontrig][year][1] )
        presel="lep1_pt > 25 && lep2_pt > 20 && %s " %signness['ss']
        wp_ = "mvaBased_tthmva"
        print( "Preselection : %s" %presel )
        #ROOT.loadSF2D( "../analysis/data/chargeFlip_%s_SF.root" %idataset )
                
        #begins
        histo_pair = {}
        for idf in DF :
            # name      
            name = idf.split('_')[0]
            print(" name : ", name )
            
            # define weight
            weight = '%s*%s' %( cfg[year]['%s_w'%name] , cfg[year]['WPs'][wp_] if name == 'MC' else cfg[year]['WPs'][wp_].split('*LepSF')[0] )
            df = DF[idf].Define( 'weights' , weight )
            print( " Common weights : " , weight )

            # preselection
            df_tmp = df.Filter( presel , "Preselection : %s" %presel )
            # SS/OS region
            # SF (D/M) x MC_SS = DATA_SS
            #df_tmp = df.Filter( signness['ss'] , '%s selection' %signness['ss'] )
            
            if name == "MC" :
                histo_pair[name] = PrepareVariable( df_tmp , name , idataset , "Scale factor method" , 1 )
            else:
                histo_pair[name] = PrepareVariable( df_tmp , name , idataset , "Scale factor method" )
            ###################
            
        output += output + "/SF_application_before" if not withSF else "/SF_application_after"
	if not os.path.exists(output): os.system('mkdir -p %s' %output)
        for imc, idata in zip( histo_pair['MC'] , histo_pair['DATA'] ) :
            #print( "imc : ", imc , " ; idata : ", idata )
            #print( "imc : ", histo_pair['MC'][imc] , " ; idata : ", histo_pair['DATA'][idata] )
            saveHisto1DCompare( histo_pair['MC'][imc].GetPtr() , histo_pair['DATA'][idata].GetPtr() , output , imc.split('MC_')[-1] , 0, 4, False, True if 'pt' in imc else False )
            
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
