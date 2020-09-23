#ifndef CONFIG_H
#define CONFIG_H

/*
 * configuration for ntuple
 */
struct config_t {
  // basic
  bool isMC=false;
  std::string year;
  std::string lumi;

  std::map< const std::string , const std::vector<std::string> > outBranch ={
    {
      "mc_2016",{
        "run",
        "luminosityBlock",
        "event",
        "PrefireWeight",
        "LepCut2l__ele_cut_WP_Tight80X__mu_cut_Tight80x",
        "LepSF2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x",
        "SFweight2l","LepSF2l__ele_cut_WP_Tight80X_SS__Up",
        "LepSF2l__ele_cut_WP_Tight80X__Do",
        "LepSF2l__ele_cut_WP_Tight80X__mu_cut_Tight80x",
        "LepSF2l__ele_mva_90p_Iso2016__Up",
        "LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
        "LepSF2l__ele_cut_WP_Tight80X__Up",
        "METFilter_MC",
        "LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x",
        "XSWeight",
        "LepSF2l__mu_cut_Tight80x__Do",
        "LepSF2l__mu_cut_Tight80x__Up",
        "LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
        "LepSF2l__ele_mva_90p_Iso2016__Do",
        "LepSF2l__ele_cut_WP_Tight80X_SS__Do",
        "GenLepMatch2l",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "genmatch",
        "ptllDYW" ,
	"isZpole"
      }
    },

    {
      "mc_2017",{
	"run",
	"luminosityBlock",
	"event",
	"PrefireWeight",
	"LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__mu_cut_Tight_HWWW__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__Do",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__Do",
	"SFweight2l",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__mu_cut_Tight_HWWW__Do",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__Up",
	"METFilter_MC",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__Do",
	"XSWeight",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__Do",
	"LepCut2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__Up",
	"GenLepMatch2l",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"genmatch",
	"ptllDYW" ,
	"isZpole"
       }
    },

    {
      "mc_2018",{
	"run",
	"luminosityBlock",
	"event",
	"LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__mu_cut_Tight_HWWW__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__Do",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__Do",
	"SFweight2l",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__mu_cut_Tight_HWWW__Do",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__Up",
	"METFilter_MC",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__Up",
	"LepSF2l__ele_mvaFall17V2Iso_WP90_SS__Do",
	"XSWeight",
	"LepSF2l__ele_mvaFall17V1Iso_WP90_SS__Do",
	"LepCut2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__Up",
	"GenLepMatch2l",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"genmatch",
	"ptllDYW" ,
	"isZpole"
      }
    },
    
    {
      "data_2016",{
	"run",
	"luminosityBlock",
	"event",
	"Trigger_sngEl",
	"Trigger_sngMu",
	"Trigger_dblEl",
	"Trigger_dblMu",
	"Trigger_ElMu",
	"LepCut2l__ele_cut_WP_Tight80X__mu_cut_Tight80x",
	"LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x",
	"LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
	"METFilter_DATA",
	"LepCut2l__ele_mva_90p_Iso2016_SS__mu_cut_Tight80x",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"isZpole"
      }
    },
    
    {
      "data_2017",{
	"run",
	"luminosityBlock",
	"event",
	"Trigger_sngEl",
	"Trigger_sngMu",
	"Trigger_dblEl",
	"Trigger_dblMu",
	"Trigger_ElMu",
	"LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"METFilter_DATA",
	"LepCut2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"isZpole"
      }
    },
    
    {
      "data_2018",{
	"run",
	"luminosityBlock",
	"event",
	"Trigger_sngEl",
	"Trigger_sngMu",
	"Trigger_dblEl",
	"Trigger_dblMu",
	"Trigger_ElMu",
	"LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW",
	"METFilter_DATA",
	"LepCut2l__ele_mvaFall17V2Iso_WP90_SS__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"isZpole"
      }
    },
    
    {
      "fake_2016",{
        "run",
        "luminosityBlock",
        "event",
        "Trigger_sngEl",
        "Trigger_sngMu",
        "Trigger_dblEl",
        "Trigger_dblMu",
        "Trigger_ElMu",
        "fakeW2l_ele_mva_90p_Iso2016_mu_cut_Tight80x",
        "METFilter_FAKE",
        "fakeW2l_ele_mva_90p_Iso2016_SS_mu_cut_Tight80x",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"isZpole"
      }
    },
    
    {
      "fake_2017",{
        "run",
        "luminosityBlock",
        "event",
        "Trigger_sngEl",
        "Trigger_sngMu",
        "Trigger_dblEl",
        "Trigger_dblMu",
        "Trigger_ElMu",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_SS_mu_cut_Tight_HWWW",
        "METFilter_FAKE",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"isZpole"
      }
    },

    {
      "fake_2018",{
        "run",
        "luminosityBlock",
        "event",
        "Trigger_sngEl",
        "Trigger_sngMu",
        "Trigger_dblEl",
        "Trigger_dblMu",
        "Trigger_ElMu",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_SS_mu_cut_Tight_HWWW",
        "METFilter_FAKE",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"isZpole"
      }
    }
    
  };
  
  //DY correction
  std::map< const std::string , const std::string> ptllDYW_NLO = {
    {"2016","(0.876979+gen_ptll*(4.11598e-03)-(2.35520e-05)*gen_ptll*gen_ptll)*(1.10211 * (0.958512 - 0.131835*TMath::Erf((gen_ptll-14.1972)/10.1525)))*(gen_ptll<140)+0.891188*(gen_ptll>=140)"},
    {"2017","(((0.623108 + 0.0722934*gen_ptll - 0.00364918*gen_ptll*gen_ptll + 6.97227e-05*gen_ptll*gen_ptll*gen_ptll - 4.52903e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll<45)*(gen_ptll>0) + 1*(gen_ptll>=45))*(abs(gen_mll-90)<3) + (abs(gen_mll-90)>3))"},
    {"2018","(0.87*(gen_ptll<10)+(0.379119+0.099744*gen_ptll-0.00487351*gen_ptll*gen_ptll+9.19509e-05*(gen_ptll*gen_ptll*gen_ptll)-6.0212e-07*(gen_ptll*gen_ptll*gen_ptll*gen_ptll))*(gen_ptll>=10 && gen_ptll<45)+(9.12137e-01+1.11957e-04*gen_ptll-3.15325e-06*gen_ptll*gen_ptll-4.29708e-09*gen_ptll*gen_ptll*gen_ptll+3.35791e-11*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>=45 && gen_ptll<200) + 1*(gen_ptll>200))"}
  };

  std::map< const std::string , const std::string> ptllDYW_LO = {
    {"2016","(gen_ptll>=0.0)*((8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140))"},
    {"2017","((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))"},
    {"2018","((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))"}
  };

//trigger configuration
  std::map< const std::string , const std::string > trigger = {
    //{"MuonEG","Trigger_ElMu"},
    //{"DoubleMuon","!Trigger_ElMu && Trigger_dblMu"},
    //{"SingleMuon","!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu"},
    {"DoubleEG","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl"}, // none existent for 2018
    {"SingleElectron","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl"},
    {"EGamma","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)"} // only 2018
  };
};

#endif
