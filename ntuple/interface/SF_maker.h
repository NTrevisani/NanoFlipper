#ifndef SF_MAKER_H
#define SF_MAKER_H

#include "helper.h"
#include "config.h"

void makeSF_ele( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst ) {

  int ele_nbins_eta = 10;
  int ele_nbins_pt = 7;

  float ele_eta_bins[] {-2.5, -2., -1.566, -1.444,  -0.8, 0., 0.8, 1.444, 1.566, 2.0, 2.5};
  float ele_pt_bins[] {10., 15., 20., 35., 50., 90., 150., 500.};

  // Loop on run periods
  for( auto f : SF_files_map_in ){

    TH2D h_SF = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    TH2D h_SF_err = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    TH2D h_SF_sys = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);

    for(int iBinX = 1; iBinX<=h_SF.GetNbinsX(); iBinX++){
      for(int iBinY = 1; iBinY<=h_SF.GetNbinsY(); iBinY++){

	double eta = h_SF.GetXaxis()->GetBinCenter(iBinX);
	double pt = h_SF.GetYaxis()->GetBinCenter(iBinY);

	if(f.find(".txt") != std::string::npos){
	  //Parsing the .txt file
	  std::string line;
	  std::istringstream strm;
	  double num;
	  std::ifstream ifs(f);

	  double lines[70][12];

	  int i=0;
	  int j=0;
	  while(getline(ifs, line)){
	    j=0;
	    std::istringstream strm(line);
	    while(strm >> num){
	      lines[i][j] = num;
	      j++;
	    }
	    i++;
	  }
	  //Looking for correct eta, pt bin
	  for(unsigned int i=0;i<70;i++){

	    if(eta>=lines[i][0] && eta<=lines[i][1] && pt>=lines[i][2] && pt<=lines[i][3]){

	      double data = lines[i][4];
	      double mc = lines[i][6];

	      double sigma_d = lines[i][5];
	      double sigma_m = lines[i][7];

	      h_SF.SetBinContent(iBinX, iBinY, data/mc);
	      h_SF_err.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(sigma_d/mc, 2) + TMath::Power(data/mc/mc*sigma_m, 2) ));
	      h_SF_sys.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(lines[i][8], 2) + TMath::Power(lines[i][9], 2) + TMath::Power(lines[i][10], 2) + TMath::Power(lines[i][11], 2) ) / mc);
	      break;
	    }
	  }
	}
	else{
	  //Not needed for now as all electron SF files are .txt
	  continue;
	}
      }
    }

    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
    sf_syst.push_back(h_SF_sys);
  }
}

void makeSF_muon( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname ) {
  
  for( auto f : SF_files_map_in ){
    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    
    // C language allows the creation of arrays on the stack of variable length, but C ++ does not. In C ++ the size of the arrays allocated in the stack must be known at compile time.
    std::vector<double> mu_eta_bins(mu_nbins_eta+1), mu_pt_bins(mu_nbins_pt+1);

    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }
    
    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    
    for(int i=1; i<=mu_nbins_eta;i++){
            for(int j=1; j<=mu_nbins_pt;j++){
              h_SF.SetBinContent(i, j, htemp->GetBinContent(i, j));
              h_SF_err.SetBinContent(i, j, htemp->GetBinError(i, j));
	      h_SF_sys.SetBinContent(i, j, 1.); // FIXME this is here as a placeholder: old SF files only have total error, in the new ones it is split
            }
        }
    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
    sf_syst.push_back(h_SF_sys);
  }
}

void makeSF_muon_tthMVA( std::pair< std::list<std::string> , std::list<std::string> > SF_files_map_in , std::vector<TH2D> &sf_nom , std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname ) {

  // NOM
  for( auto f : SF_files_map_in.first ){

    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    std::vector<double> mu_eta_bins(mu_nbins_eta+1), mu_pt_bins(mu_nbins_pt+1);
    
    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }

    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());

    for(int i=1; i<=mu_nbins_eta;i++){
      for(int j=1; j<=mu_nbins_pt;j++){
	h_SF.SetBinContent(i, j, htemp->GetBinContent(i, j));
	h_SF_err.SetBinContent(i, j, htemp->GetBinError(i, j));
      }
    }

    sf_nom.push_back(h_SF);
    sf_stat.push_back(h_SF_err);
  }

  // SYS
  for( auto f : SF_files_map_in.second ){
    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    std::vector<double> mu_eta_bins(mu_nbins_eta+1), mu_pt_bins(mu_nbins_pt+1);
    
    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }

    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());

    for(int i=1; i<=mu_nbins_eta;i++){
      for(int j=1; j<=mu_nbins_pt;j++){
	h_SF_sys.SetBinContent(i, j, htemp->GetBinError(i, j));
      }
    }
    sf_syst.push_back(h_SF_sys);
  }
}

///
std::tuple<double, double, double> GetSF(int flavor, float eta, float pt, int run_period, config_t mycfg , std::string type){

  double eta_temp = eta;
  double pt_temp = pt;

  double SF, SF_err, SF_sys;

  if((flavor==11) && (type == "ttHMVA")){

    double eta_max = 2.49;
    double eta_min = -2.5;
    double pt_max = 499.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = mycfg.h_SF_ele_ttHMVA[run_period].GetBinContent(mycfg.h_SF_ele_ttHMVA[run_period].FindBin(eta_temp, pt_temp));
    SF_err = mycfg.h_SF_ele_ttHMVA_err[run_period].GetBinContent(mycfg.h_SF_ele_ttHMVA_err[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = mycfg.h_SF_ele_ttHMVA_sys[run_period].GetBinContent(mycfg.h_SF_ele_ttHMVA_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else if((flavor==11) && (type == "Id")){

    double eta_max = 2.49;
    double eta_min = -2.5;
    double pt_max = 499.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = mycfg.h_SF_ele[run_period].GetBinContent(mycfg.h_SF_ele[run_period].FindBin(eta_temp, pt_temp));
    SF_err = mycfg.h_SF_ele_err[run_period].GetBinContent(mycfg.h_SF_ele_err[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = mycfg.h_SF_ele_sys[run_period].GetBinContent(mycfg.h_SF_ele_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else if((flavor == 13) && (type == "Id")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = mycfg.h_SF_mu_Id[run_period].GetBinContent(mycfg.h_SF_mu_Id[run_period].FindBin(eta_temp, pt_temp));
    SF_err = mycfg.h_SF_mu_Id_err[run_period].GetBinContent(mycfg.h_SF_mu_Id_err[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = mycfg.h_SF_mu_Id_sys[run_period].GetBinContent(mycfg.h_SF_mu_Id_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else if((flavor == 13) && (type == "Iso")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = mycfg.h_SF_mu_Iso[run_period].GetBinContent(mycfg.h_SF_mu_Iso[run_period].FindBin(eta_temp, pt_temp));
    SF_err = mycfg.h_SF_mu_Iso_err[run_period].GetBinContent(mycfg.h_SF_mu_Iso_err[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = mycfg.h_SF_mu_Iso_sys[run_period].GetBinContent(mycfg.h_SF_mu_Iso_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else if((flavor == 13) && (type == "ttHMVA")){

    double eta_max = 2.39;
    double eta_min = -2.4;
    double pt_max = 199.;
    double pt_min = 10.;

    if(eta_temp < eta_min){eta_temp = eta_min;}
    if(eta_temp > eta_max){eta_temp = eta_max;}
    if(pt_temp < pt_min){pt_temp = pt_min;}
    if(pt_temp > pt_max){pt_temp = pt_max;}

    SF = mycfg.h_SF_mu_ttHMVA[run_period].GetBinContent(mycfg.h_SF_mu_ttHMVA[run_period].FindBin(eta_temp, pt_temp));
    SF_err = mycfg.h_SF_mu_ttHMVA_err[run_period].GetBinContent(mycfg.h_SF_mu_ttHMVA_err[run_period].FindBin(eta_temp, pt_temp));
    SF_sys = mycfg.h_SF_mu_ttHMVA_sys[run_period].GetBinContent(mycfg.h_SF_mu_ttHMVA_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else {std::cout << "Invalid call to compute_SF::GetSF" << std::endl;}

  //std::tuple<double, double, double> result = {SF, SF_err, SF_sys};

  return std::tuple<double,double,double>{ SF, SF_err, SF_sys };

}

template < typename T >
  auto hww_tthmva_sf( T &df, config_t &cfg){
  using namespace ROOT::VecOps;
  
  // lambda function
  auto hww_tthmva_sf_maker = [&cfg](
				    const int& run_period ,
				    const RVec<int>& pdgId ,
				    const RVec<float>& lepton_pt ,
				    const RVec<float>& lepton_eta ,
				    const RVec<float>& lepton_recoSF ,
				    const RVec<float>& lepton_recoSF_Up ,
				    const RVec<float>& lepton_recoSF_Down
				    )
    {
      std::vector<double> SF_vect {};
      std::vector<double> SF_err_vect {};
      std::vector<double> SF_up {};
      std::vector<double> SF_do {};
      
      const unsigned int nlep = cfg.nlep_SF; 
      int run_period__ = run_period;
      
      for ( unsigned int i=0 ; i < nlep ; i++ ){
	if(TMath::Abs(pdgId[i]) == 11){
	  std::list<std::string> SF_path = cfg.SF_files_map["electron"]["TightObjWP"][cfg.year]["wpSF"];
	  std::list<std::string> SF_path_ttHMVA = cfg.SF_files_map["electron"]["ttHMVA0p7"][cfg.year]["ttHMVA"];
	  std::tuple<double, double, double> res;
	  std::tuple<double, double, double> res_ttHMVA;
	  if( cfg.year.find("2017") != std::string::npos ){
	    int runp = run_period;                         
	    if (runp <= 2){                                
	      run_period__ = runp-1;
	    }                                              
	    else{                                          
	      run_period__ = runp-2;                       
	    }                                              
	    res = GetSF( 11 , lepton_eta[i] , lepton_pt[i], SF_path.size()==1 ? 0 : run_period__ , cfg , "Id"); 
	    res_ttHMVA = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path_ttHMVA.size()==1 ? 0 : run_period__ , cfg , "ttHMVA");
	  }                                                                                                                   
	  else{                                                                                                               
	    res = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path.size()==1 ? 0 : run_period__ - 1, cfg , "Id");               
	    res_ttHMVA = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path_ttHMVA.size()==1 ? 0 : run_period__ - 1, cfg , "ttHMVA");
	  }
	  // scale factor = HWW x ttHMVA
	  SF_vect.push_back(std::get<0>(res)*std::get<0>(res_ttHMVA));
	  SF_err_vect.push_back(TMath::Sqrt(TMath::Power(std::get<1>(res), 2) + TMath::Power(std::get<2>(res), 2)                
					    + TMath::Power(std::get<1>(res_ttHMVA), 2) + TMath::Power(std::get<2>(res_ttHMVA), 2) ));
	}
	else if(TMath::Abs(pdgId[i]) == 13){
	  std::list<std::string> SF_path_id = cfg.SF_files_map["muon"]["TightObjWP"][cfg.year]["idSF"];             
	  std::list<std::string> SF_path_iso = cfg.SF_files_map["muon"]["TightObjWP"][cfg.year]["isoSF"];
	  std::tuple<double, double, double> res_id = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_id.size()==1 ? 0 : run_period__ - 1, cfg , "Id");
	  std::tuple<double, double, double> res_iso = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_iso.size()==1 ? 0 : run_period__ - 1, cfg , "Iso");
	  std::tuple<double, double, double> res_ttHMVA = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_iso.size()==1 ? 0 : run_period__ - 1, cfg , "ttHMVA");
	  double SF_id = std::get<0>(res_id);                                                      
	  double SF_iso = std::get<0>(res_iso);                                                                                                                
	  double SF_ttHMVA = std::get<0>(res_ttHMVA);
	  // scale factor = HWW x ttHMVA
	  SF_vect.push_back( SF_id * SF_iso * SF_ttHMVA );
	  // SF_err_vect.push_back((SF_id * SF_iso) * TMath::Sqrt( TMath::Power(std::get<1>(res_id)/SF_id, 2) + TMath::Power(std::get<1>(res_iso)/SF_iso, 2) )); // Old formula for debugging                   
	  SF_err_vect.push_back(                                                                                                                               
				(SF_id * SF_iso * SF_ttHMVA) * TMath::Sqrt(                                                                                    
									   TMath::Power(std::get<1>(res_id)/SF_id, 2)                                          
									   + TMath::Power(std::get<1>(res_iso)/SF_iso, 2)                                      
									   + (TMath::Power(std::get<1>(res_ttHMVA), 2) + TMath::Power(std::get<2>(res_ttHMVA), 2))/SF_ttHMVA/SF_ttHMVA )
																			       );
	}
      } // end of loops
      
      double SF = 1.;
      
      // Calculate product of IsIso_SFs for all leptons in the event
      for(auto x : SF_vect) SF *= x;

      // Now for the variations, these also have to account for the recoSF
      for( unsigned int i=0 ; i< nlep ; i++ ){
	
	SF_up.push_back( ((SF_vect[i] * lepton_recoSF[i]) + TMath::Sqrt(TMath::Power(SF_err_vect[i], 2) + TMath::Power(lepton_recoSF_Up[i] - lepton_recoSF[i], 2) ))/(SF_vect[i] * lepton_recoSF[i]) );
	SF_do.push_back( ((SF_vect[i] * lepton_recoSF[i]) - TMath::Sqrt(TMath::Power(SF_err_vect[i], 2) + TMath::Power(lepton_recoSF_Down[i] - lepton_recoSF[i], 2) ))/(SF_vect[i] * lepton_recoSF[i]) );
      }
      // output {total_SF ; single_SF_up_0 ; single_SF_up_1 ; single_SF_down_0 ; single_SF_down_1 }
      return RVec<double> (
	{
	  SF,
	    SF_vect.size() > 0 ? SF_up[0] : 1. ,
	    SF_vect.size() > 1 ? SF_up[1] : 1. ,
	    SF_vect.size() > 0 ? SF_do[0] : 1. ,
	    SF_vect.size() > 1 ? SF_do[1] : 1.
	    }
	);
    };
  
  std::cout<<" --> default HWW WP : "<< cfg.HWW_WP[cfg.year] <<std::endl;
  
  df = df
    .Define( "HWW_WP_cut" , cfg.HWW_WP[cfg.year] )
    .Define( "LepCut2l__ele_mu_tthMVA" , "HWW_WP_cut*( (abs(Lepton_pdgId[0])==11 || Muon_mvaTTH[Lepton_muonIdx[0]]>0.8) && (abs(Lepton_pdgId[1])==11 || Muon_mvaTTH[Lepton_muonIdx[1]]>0.8) && (abs(Lepton_pdgId[0])==13 || Electron_mvaTTH[Lepton_electronIdx[0]]>0.70) && (abs(Lepton_pdgId[1])==13 || Electron_mvaTTH[Lepton_electronIdx[1]]>0.70))");

  // mc only
  if (cfg.isMC){
    df = df
      .Define( "ttHMVA" , hww_tthmva_sf_maker , { "run_period" , "Lepton_pdgId" , "Lepton_pt" , "Lepton_eta" , "Lepton_RecoSF" , "Lepton_RecoSF_Up" , "Lepton_RecoSF_Down" } )
      .Define( "ttHMVA_SF_2l" , "ttHMVA[0]" )
      .Define( "ttHMVA_SF_Up_0" , "ttHMVA[1]" )
      .Define( "ttHMVA_SF_Up_1" , "ttHMVA[2]" )
      .Define( "ttHMVA_SF_Down_0" , "ttHMVA[3]" )
      .Define( "ttHMVA_SF_Down_1" , "ttHMVA[4]" );

    // Up/Down variations for electrons, i.e. LepSF2l__ele_'+eleWP+'__Up/Down
    df = df
      .Define( "ttHMVA_2l_ele_SF_Up" , "(ttHMVA_SF_Up_0*(TMath::Abs(Lepton_pdgId[0]) == 11) + (TMath::Abs(Lepton_pdgId[0]) == 13)) * (ttHMVA_SF_Up_1*(TMath::Abs(Lepton_pdgId[1]) == 11) + (TMath::Abs(Lepton_pdgId[1]) == 13))" )
      .Define( "ttHMVA_2l_ele_SF_Down" , "(ttHMVA_SF_Down_0*(TMath::Abs(Lepton_pdgId[0]) == 11) + (TMath::Abs(Lepton_pdgId[0]) == 13)) * (ttHMVA_SF_Down_1*(TMath::Abs(Lepton_pdgId[1]) == 11) + (TMath::Abs(Lepton_pdgId[1]) == 13))" );
    
    // Up/Down variations for muons, i.e. LepSF2l__mu_'+muWP+'__Up/Down
    df = df
      .Define( "ttHMVA_2l_mu_SF_Up" , "(ttHMVA_SF_Up_0*(TMath::Abs(Lepton_pdgId[0]) == 13) + (TMath::Abs(Lepton_pdgId[0]) == 11)) * (ttHMVA_SF_Up_1*(TMath::Abs(Lepton_pdgId[1]) == 13) + (TMath::Abs(Lepton_pdgId[1]) == 11))" )
      .Define( "ttHMVA_2l_mu_SF_Down" , "(ttHMVA_SF_Down_0*(TMath::Abs(Lepton_pdgId[0]) == 13) + (TMath::Abs(Lepton_pdgId[0]) == 11)) * (ttHMVA_SF_Down_1*(TMath::Abs(Lepton_pdgId[1]) == 13) + (TMath::Abs(Lepton_pdgId[1]) == 11))" );
      }
  return df;
}

#endif
