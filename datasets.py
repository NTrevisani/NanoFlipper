Dataset={}
DIR="/media/shoh/02A1ACF427292FC0/nanov5"

###### 2016 #######
Dataset['nanov5_2016'] ={
    'DATA' : '%s/2016/Run2016_102X_nAODv4_Full2016v5/DATAl1loose2016v5__l2loose__l2tightOR2016v5' %DIR,
    'MC'   : '%s/2016/Summer16_102X_nAODv4_Full2016v5/MCl1loose2016v5__MCCorr2016v5__l2loose__l2tightOR2016v5' %DIR,
    'Trig' : {
        'DoubleEG' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl',
        'SingleElectron' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl'
    },
    'dataW': 'METFilter_DATA*LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x',
    'mcW'  : {
        'common' : '35.867*XSWeight*SFweight2l*LepSF2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*PrefireWeight*GenLepMatch2l*METFilter_MC',
        'DYJetsToLL_M-10to50-LO' : '(8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140)',
        #'DYJetsToLL_M-50-LO_ext1' : '(8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140)',
        #'DYJetsToLL_M-50-LO_ext2' :  '(8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140)',
        'DYJetsToLL_M-50_ext2' : '(0.876979+gen_ptll*(4.11598e-03)-(2.35520e-05)*gen_ptll*gen_ptll)*(1.10211 * (0.958512 - 0.131835*TMath::Erf((gen_ptll-14.1972)/10.1525)))*(gen_ptll<140)+0.891188*(gen_ptll>=140)'
        
    },
    'btagcsv' : 'data/btagSF/DeepCSV_2016LegacySF_V1.csv',
}

####### 2017 #########
Dataset['nanov5_2017'] ={
    'DATA' : '%s/2017/Run2017_102X_nAODv4_Full2017v5/DATAl1loose2017v5__l2loose__l2tightOR2017v5' %DIR,
    'MC'   : '%s/2017/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__l2loose__l2tightOR2017v5' %DIR,
    'Trig' : {
        'DoubleEG'       : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl',
        'SingleElectron' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl',
    },
    'dataW' : 'METFilter_DATA*LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW',
    'mcW'  : {
        'common' : '41.53*XSWeight*SFweight2l*LepSF2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW*LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW*PrefireWeight*GenLepMatch2l*METFilter_MC',
        'DYJetsToLL_M-10to50-LO' : '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))',
        #'DYJetsToLL_M-50' : '(((0.623108 + 0.0722934*gen_ptll - 0.00364918*gen_ptll*gen_ptll + 6.97227e-05*gen_ptll*gen_ptll*gen_ptll - 4.52903e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll<45)*(gen_ptll>0) + 1*(gen_ptll>=45))*(abs(gen_mll-90)<3) + (abs(gen_mll-90)>3))',
        'DYJetsToLL_M-50-LO_ext1' : '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))'
    },
    'btagcsv' : 'data/btagSF/DeepCSV_94XSF_V2_B_F.csv',
}

###### 2018 ###########
Dataset['nanov5_2018'] ={
    'DATA' : '%s/2018/Run2018_102X_nAODv5_Full2018v5/DATAl1loose2018v5__l2loose__l2tightOR2018v5' %DIR,
    'MC'   : '%s/2018/Autumn18_102X_nAODv5_Full2018v5/MCl1loose2018v5__MCCorr2018v5__l2loose__l2tightOR2018v5' %DIR,
    'Trig' : {
        'EGamma'         : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)',
    },
    'dataW' : 'METFilter_DATA*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW',
    'mcW'  : {
        'common' : '59.74*XSWeight*SFweight2l*LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*GenLepMatch2l*METFilter_MC',
        'DYJetsToLL_M-10to50-LO' : '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))',
        'DYJetsToLL_M-50_ext' : '(0.87*(gen_ptll<10)+(0.379119+0.099744*gen_ptll-0.00487351*(gen_ptll*gen_ptll)+9.19509e-05*(gen_ptll*gen_ptll*gen_ptll)-6.0212e-07*(gen_ptll*gen_ptll*gen_ptll*gen_ptll))*(gen_ptll>=10 && gen_ptll<45)+(9.12137e-01+1.11957e-04*gen_ptll-3.15325e-06*(gen_ptll*gen_ptll)-4.29708e-09*(gen_ptll*gen_ptll*gen_ptll)+3.35791e-11*(gen_ptll*gen_ptll*gen_ptll*gen_ptll))*(gen_ptll>=45 && gen_ptll<200) + 1*(gen_ptll>200))'
    },
    'btagcsv' : 'data/btagSF/DeepCSV_102XSF_V1.csv',
}
