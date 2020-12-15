#ifndef SF_MAKER_H
#define SF_MAKER_H

#include "helper.h"
#include "config.h"

// make muon 
void makeSF_muon( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom , std::string histname ) { //, std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst , std::string histname ) {
  
  for( auto f : SF_files_map_in ){
    TFile rootfile(f.c_str());
    TH2D* htemp = (TH2D*)rootfile.Get(histname.c_str());

    int mu_nbins_eta = htemp->GetNbinsX(), mu_nbins_pt = htemp->GetNbinsY();
    
    // C language allows the creation of arrays on the stack of variable length, but C ++ does not. 
    //In C ++ the size of the arrays allocated in the stack must be known at compile time.
    std::vector<double> mu_eta_bins(mu_nbins_eta+1), mu_pt_bins(mu_nbins_pt+1);

    for(int k=0;k<=mu_nbins_eta;k++) { mu_eta_bins[k] = htemp->GetXaxis()->GetXbins()->At(k); }
    for(int k=0;k<=mu_nbins_pt;k++) { mu_pt_bins[k] = htemp->GetYaxis()->GetXbins()->At(k); }
    
    TH2D h_SF = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    //TH2D h_SF_err = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    //TH2D h_SF_sys = TH2D("", "", mu_nbins_eta, mu_eta_bins.data(), mu_nbins_pt, mu_pt_bins.data());
    
    for(int i=1; i<=mu_nbins_eta;i++){
            for(int j=1; j<=mu_nbins_pt;j++){
              h_SF.SetBinContent(i, j, htemp->GetBinContent(i, j));
              //h_SF_err.SetBinContent(i, j, htemp->GetBinError(i, j));
	      //h_SF_sys.SetBinContent(i, j, 1.); // FIXME this is here as a placeholder: old SF files only have total error, in the new ones it is split
            }
        }
    sf_nom.push_back(h_SF);
    //sf_stat.push_back(h_SF_err);
    //sf_syst.push_back(h_SF_sys);
  }
}

// make electrion
void makeSF_ele( std::list<std::string> SF_files_map_in , std::vector<TH2D> &sf_nom  ) { //, std::vector<TH2D> &sf_stat , std::vector<TH2D> &sf_syst ) {

  int ele_nbins_eta = 10;
  int ele_nbins_pt = 7;

  float ele_eta_bins[] {-2.5, -2., -1.566, -1.444,  -0.8, 0., 0.8, 1.444, 1.566, 2.0, 2.5};
  float ele_pt_bins[] {10., 15., 20., 35., 50., 90., 150., 500.};

  // Loop on run periods
  for( auto f : SF_files_map_in ){

    TH2D h_SF = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    //TH2D h_SF_err = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);
    //TH2D h_SF_sys = TH2D("", "", ele_nbins_eta, ele_eta_bins, ele_nbins_pt, ele_pt_bins);

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

	      //double sigma_d = lines[i][5];
	      //double sigma_m = lines[i][7];

	      h_SF.SetBinContent(iBinX, iBinY, data/mc);
	      //h_SF_err.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(sigma_d/mc, 2) + TMath::Power(data/mc/mc*sigma_m, 2) ));
	      //h_SF_sys.SetBinContent(iBinX, iBinY, TMath::Sqrt( TMath::Power(lines[i][8], 2) + TMath::Power(lines[i][9], 2) + TMath::Power(lines[i][10], 2) + TMath::Power(lines[i][11], 2) ) / mc);
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
    //sf_stat.push_back(h_SF_err);
    //sf_syst.push_back(h_SF_sys);
  }
}

///
//std::tuple<double, double, double> GetSF(int flavor, float eta, float pt, int run_period, config_t mycfg , std::string type){
double GetSF(int flavor, float eta, float pt, int run_period, config_t mycfg , std::string type){

  double eta_temp = eta;
  double pt_temp = pt;

  double SF = 1. ; //, SF_err, SF_sys;

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
    //SF_err = mycfg.h_SF_ele_ttHMVA_err[run_period].GetBinContent(mycfg.h_SF_ele_ttHMVA_err[run_period].FindBin(eta_temp, pt_temp));
    //SF_sys = mycfg.h_SF_ele_ttHMVA_sys[run_period].GetBinContent(mycfg.h_SF_ele_ttHMVA_sys[run_period].FindBin(eta_temp, pt_temp));

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
    //SF_err = mycfg.h_SF_ele_err[run_period].GetBinContent(mycfg.h_SF_ele_err[run_period].FindBin(eta_temp, pt_temp));
    //SF_sys = mycfg.h_SF_ele_sys[run_period].GetBinContent(mycfg.h_SF_ele_sys[run_period].FindBin(eta_temp, pt_temp));

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
    //SF_err = mycfg.h_SF_mu_Id_err[run_period].GetBinContent(mycfg.h_SF_mu_Id_err[run_period].FindBin(eta_temp, pt_temp));
    //SF_sys = mycfg.h_SF_mu_Id_sys[run_period].GetBinContent(mycfg.h_SF_mu_Id_sys[run_period].FindBin(eta_temp, pt_temp));

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
    //SF_err = mycfg.h_SF_mu_Iso_err[run_period].GetBinContent(mycfg.h_SF_mu_Iso_err[run_period].FindBin(eta_temp, pt_temp));
    //SF_sys = mycfg.h_SF_mu_Iso_sys[run_period].GetBinContent(mycfg.h_SF_mu_Iso_sys[run_period].FindBin(eta_temp, pt_temp));

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
    //SF_err = mycfg.h_SF_mu_ttHMVA_err[run_period].GetBinContent(mycfg.h_SF_mu_ttHMVA_err[run_period].FindBin(eta_temp, pt_temp));
    //SF_sys = mycfg.h_SF_mu_ttHMVA_sys[run_period].GetBinContent(mycfg.h_SF_mu_ttHMVA_sys[run_period].FindBin(eta_temp, pt_temp));

  }
  else {std::cout << "Invalid call to compute_SF::GetSF" << std::endl;}

  //std::tuple<double, double, double> result = {SF, SF_err, SF_sys};

  //return std::tuple<double,double,double>{ SF, SF_err, SF_sys };
  return SF;

}

template < typename T >
  auto hww_tthmva_sf( T &df, config_t &cfg ){
  using namespace ROOT::VecOps;
  // lambda function
  auto hww_tthmva_sf_maker = [&cfg](
				    const int& run_period ,
				    const RVec<int>& pdgId ,
				    const RVec<float>& lepton_pt ,
				    const RVec<float>& lepton_eta ,
				    const RVec<int>& lepton_electronIdx ,
				    const RVec<int>& lepton_muonIdx ,
				    const RVec<float>& electron_mvaTTH ,
				    const RVec<float>& muon_mvaTTH
				    )
    {
      const unsigned int nlep = cfg.nlep_SF;
      std::vector<double> SF_vect( nlep , 1. );
      std::vector<int> Cut_vect( nlep , 1 );
      for ( unsigned int i=0 ; i < nlep ; i++ ){
	
	if (TMath::Abs(pdgId[i]) == 11){
	  if (cfg.isMC){
	    std::list<std::string> SF_path = cfg.SF_files_map["electron"]["TightObjWP"][cfg.year]["idSF"];
	    std::list<std::string> SF_path_ttHMVA = cfg.SF_files_map["electron"]["ttHMVA0p7"][cfg.year]["ttHMVA"];

	    double res        = GetSF( 11, lepton_eta[i], lepton_pt[i], SF_path.size()==1 ? 0 : run_period - 1, cfg , "Id");
	    double res_ttHMVA = GetSF( 11, lepton_eta[i], lepton_pt[i], SF_path_ttHMVA.size()==1 ? 0 : run_period - 1, cfg , "ttHMVA");

	    // scale factor = HWW x ttHMVA
	    SF_vect[i] = res * res_ttHMVA ;
	  }
	  // passing cut?
	  Cut_vect[i] = ( electron_mvaTTH[lepton_electronIdx[i]] > 0.7 ) ? 1 : 0;
	}
	else if(TMath::Abs(pdgId[i]) == 13){
	  if (cfg.isMC){
	    std::list<std::string> SF_path_id = cfg.SF_files_map["muon"]["TightObjWP"][cfg.year]["idSF"];
	    std::list<std::string> SF_path_iso = cfg.SF_files_map["muon"]["TightObjWP"][cfg.year]["isoSF"];
	    
	    double res_id = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_id.size()==1 ? 0 : run_period - 1, cfg , "Id");
	    double res_iso = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_iso.size()==1 ? 0 : run_period - 1, cfg , "Iso");
	    double res_ttHMVA = GetSF(13, lepton_eta[i], lepton_pt[i], SF_path_iso.size()==1 ? 0 : run_period - 1, cfg , "ttHMVA");
	    
	    // scale factor = HWW_Id x HWW_Iso x ttHMVA
	    SF_vect[i] = res_id * res_iso * res_ttHMVA ;
	  }
	  // passing cut ?
	  Cut_vect[i] = ( muon_mvaTTH[lepton_muonIdx[i]] > 0.8 ) ? 1 : 0;
        }
      } // end of loops
      
      double SF = 1.;
      int Cut = 1;
      
      for(auto x : Cut_vect) Cut *= x;
      // Calculate product of IsIso_SFs for all leptons in the event
      for(auto x : SF_vect) SF *= x;
      
      return std::make_pair( Cut , SF );
    };
  
  std::cout<<" --> default HWW WP : "<< cfg.HWW_WP[cfg.year] <<std::endl;
  
  df = df
    .Define( "hww_tthmva_sf_maker" , hww_tthmva_sf_maker , 
	     { "run_period" , "Lepton_pdgId" , "Lepton_pt" , "Lepton_eta" , "Lepton_electronIdx" , "Lepton_muonIdx" , "Electron_mvaTTH" , "Muon_mvaTTH" } )
    .Define( "HWW_WP_cut" , cfg.HWW_WP[cfg.year] )
    .Define( "LepCut3l__ele_mu_HWW_ttHMVA" , "HWW_WP_cut*(hww_tthmva_sf_maker.first)" )
    .Define( "LepSF3l__ele_mu_HWW_ttHMVA" , "hww_tthmva_sf_maker.second" )
    ;
  return df;
}

#endif
