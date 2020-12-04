#ifndef CONFIG_H
#define CONFIG_H


typedef std::map<std::string, std::map<std::string, std::map<std::string, std::map<std::string, std::list<std::string>>>>> nested_dict;
typedef std::map<std::string,std::string> WP_dict;

/*
 * configuration for ntuple
 */
struct config_t {
  // basic
  bool isMC=false;
  std::string year;
  std::string lumi;
  std::string base;
  nested_dict SF_files_map;
  const unsigned int nlep_SF=2;

  WP_dict HWW_WP= {
    { "2016" , "LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x" } ,
    { "2017" , "LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW" } ,
    { "2018" , "LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW" }
  };

  std::vector<TH2D> h_SF_ele {};
  std::vector<TH2D> h_SF_ele_err {};
  std::vector<TH2D> h_SF_ele_sys {};
  std::vector<TH2D> h_SF_ele_ttHMVA {};
  std::vector<TH2D> h_SF_ele_ttHMVA_err {};
  std::vector<TH2D> h_SF_ele_ttHMVA_sys {};
  
  std::vector<TH2D> h_SF_mu_Id {};
  std::vector<TH2D> h_SF_mu_Id_err {};
  std::vector<TH2D> h_SF_mu_Id_sys {};
  std::vector<TH2D> h_SF_mu_Iso {};
  std::vector<TH2D> h_SF_mu_Iso_err {};
  std::vector<TH2D> h_SF_mu_Iso_sys {};
  std::vector<TH2D> h_SF_mu_ttHMVA {};
  std::vector<TH2D> h_SF_mu_ttHMVA_err {};
  std::vector<TH2D> h_SF_mu_ttHMVA_sys {};
  
  size_t listSize;

  std::map< const std::string , const std::vector<std::string> > outBranch ={
    {
      "mc_2016",{
        "run",
        "luminosityBlock",
        "event",
        "PrefireWeight",
        "SFweight2l",
        "LepSF2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
        "METFilter_MC",
        "XSWeight",
        "LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
        "GenLepMatch2l",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "gen_promptmatch",
        "ptllDYW" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA" ,
	//"LepSF2l_ttHMVA"
	"LepWPCut" ,
	"ttHMVA_SF_2l",
	"ttHMVA_2l_ele_SF_Up",
	"ttHMVA_2l_ele_SF_Down",
	"ttHMVA_2l_mu_SF_Up",
	"ttHMVA_2l_mu_SF_Down"
      }
    },

    {
      "mc_2017",{
	"run",
	"luminosityBlock",
	"event",
	"PrefireWeight",
	"SFweight2l",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"METFilter_MC",
	"XSWeight",
	"GenLepMatch2l",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"gen_promptmatch",
	"ptllDYW" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA" ,
	//"LepSF2l_ttHMVA"
	"LepWPCut" ,
	"ttHMVA_SF_2l" ,
	"ttHMVA_2l_ele_SF_Up",
        "ttHMVA_2l_ele_SF_Down",
        "ttHMVA_2l_mu_SF_Up",
        "ttHMVA_2l_mu_SF_Down"              
      }
    },

    {
      "mc_2018",{
	"run",
	"luminosityBlock",
	"event",
	"SFweight2l",
	"LepSF2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"METFilter_MC",
	"XSWeight",
	"GenLepMatch2l",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"gen_promptmatch",
	"ptllDYW" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA" ,
	//"LepSF2l_ttHMVA"
	"LepWPCut" ,
	"ttHMVA_SF_2l" ,
	"ttHMVA_2l_ele_SF_Up" ,
        "ttHMVA_2l_ele_SF_Down" ,
        "ttHMVA_2l_mu_SF_Up" ,
        "ttHMVA_2l_mu_SF_Down"              
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
	"LepCut2l__ele_mva_90p_Iso2016__mu_cut_Tight80x",
	"METFilter_DATA",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA"
	"LepWPCut"
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
	"METFilter_DATA",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA"
	"LepWPCut"
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
	"METFilter_DATA",
	"LepCut2l__ele_mvaFall17V1Iso_WP90__mu_cut_Tight_HWWW",
	"lep1_pt",
	"lep1_eta",
	"lep1_pdgId",
	"lep2_pt",
	"lep2_eta",
	"lep2_pdgId",
	"mll",
	"trigger" ,
	"nLepton" ,
	//"LepCut2l_ttHMVA"
	"LepWPCut"
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
	"fakeW2l_ele_mva_90p_Iso2016_tthmva_70_mu_cut_Tight80x_tthmva_80",
        "METFilter_FAKE",
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"nLepton"
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
        "METFilter_FAKE",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW" ,
	"fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80" ,
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"nLepton"
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
        "METFilter_FAKE",
        "fakeW2l_ele_mvaFall17V1Iso_WP90_mu_cut_Tight_HWWW",
	"fakeW2l_ele_mvaFall17V1Iso_WP90_tthmva_70_mu_cut_Tight_HWWW_tthmva_80" ,
        "lep1_pt",
        "lep1_eta",
        "lep1_pdgId",
        "lep2_pt",
        "lep2_eta",
        "lep2_pdgId",
        "mll",
        "trigger" ,
	"nLepton"
      }
    }
    
  };
  
  //DY correction
  //std::map< const std::string , const std::string> ptllDYW_NLO = {
  //  {"2016","(0.876979+gen_ptll*(4.11598e-03)-(2.35520e-05)*gen_ptll*gen_ptll)*(1.10211 * (0.958512 - 0.131835*TMath::Erf((gen_ptll-14.1972)/10.1525)))*(gen_ptll<140)+0.891188*(gen_ptll>=140)"},
  //  {"2017","(((0.623108 + 0.0722934*gen_ptll - 0.00364918*gen_ptll*gen_ptll + 6.97227e-05*gen_ptll*gen_ptll*gen_ptll - 4.52903e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll<45)*(gen_ptll>0) + 1*(gen_ptll>=45))*(abs(gen_mll-90)<3) + (abs(gen_mll-90)>3))"},
  //  {"2018","(0.87*(gen_ptll<10)+(0.379119+0.099744*gen_ptll-0.00487351*gen_ptll*gen_ptll+9.19509e-05*(gen_ptll*gen_ptll*gen_ptll)-6.0212e-07*(gen_ptll*gen_ptll*gen_ptll*gen_ptll))*(gen_ptll>=10 && gen_ptll<45)+(9.12137e-01+1.11957e-04*gen_ptll-3.15325e-06*gen_ptll*gen_ptll-4.29708e-09*gen_ptll*gen_ptll*gen_ptll+3.35791e-11*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>=45 && gen_ptll<200) + 1*(gen_ptll>200))"}
  //};

  std::map< const std::string , const std::string> ptllDYW_LO = {
    {"2016","(gen_ptll>=0.0)*((8.61313e-01+gen_ptll*4.46807e-03-1.52324e-05*gen_ptll*gen_ptll)*(1.08683 * (0.95 - 0.0657370*TMath::Erf((gen_ptll-11.)/5.51582)))*(gen_ptll<140)+1.141996*(gen_ptll>=140))"},
    {"2017","((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))"},
    {"2018","((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))"}
  };
  
  //trigger configuration
  std::map< const std::string , const std::string > trigger = {
    {"MuonEG","Trigger_ElMu"},
    {"DoubleMuon","!Trigger_ElMu && Trigger_dblMu"},
    {"SingleMuon","!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu"},
    {"DoubleEG","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl"}, // none existent for 2018
    {"SingleElectron","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl"},
    {"EGamma","!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)"} // only 2018
  };  
  
};

#endif
