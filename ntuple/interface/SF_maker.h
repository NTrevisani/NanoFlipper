#ifndef SF_MAKER_H
#define SF_MAKER_H

#include "helper.h"
#include "config.h"

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
  else {std::cout << "Invalid call to compute_SF::GetSF" << std::endl;}

  //std::tuple<double, double, double> result = {SF, SF_err, SF_sys};

  //return std::tuple<double,double,double>{ SF, SF_err, SF_sys };
  return SF;

}

template < typename T >
  auto hww_tthmva_sf( T &df, config_t &cfg){
  using namespace ROOT::VecOps;
  
  // lambda function
  auto hww_tthmva_sf_maker = [&cfg](
				    const int& run_period ,
				    const RVec<int>& pdgId ,
				    const RVec<float>& lepton_pt ,
				    const RVec<float>& lepton_eta
				    )
    {
      std::vector<double> SF_vect {};
      //std::vector<double> SF_err_vect {};
      //std::vector<double> SF_up {};
      //std::vector<double> SF_do {};
      
      const unsigned int nlep = cfg.nlep_SF; 
      //int run_period__ = run_period;
      
      for ( unsigned int i=0 ; i < nlep ; i++ ){
	if(TMath::Abs(pdgId[i]) == 11){
	  //std::list<std::string> SF_path = cfg.SF_files_map["electron"]["TightObjWP"][cfg.year]["wpSF"];
	  std::list<std::string> SF_path_ttHMVA = cfg.SF_files_map["electron"]["ttHMVA0p7"][cfg.year]["ttHMVA"];
	  //std::tuple<double, double, double> res;
	  //std::tuple<double, double, double> res_ttHMVA;
	  //double res;
	  double res_ttHMVA;
	  if( cfg.year.find("2017") != std::string::npos ){
	    int run_period__;
	    if ( run_period <= 2){                                
	      run_period__ = run_period - 1;
	    }                                              
	    else{                                          
	      run_period__ = run_period - 2;               
	    }                                              
	    //res = GetSF( 11 , lepton_eta[i] , lepton_pt[i], SF_path.size()==1 ? 0 : run_period__ , cfg , "Id"); 
	    res_ttHMVA = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path_ttHMVA.size()==1 ? 0 : run_period__ , cfg , "ttHMVA");
	  }                                                                                                                   
	  else{                                                                                                               
	    //res = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path.size()==1 ? 0 : run_period__ - 1, cfg , "Id");               
	    res_ttHMVA = GetSF(11, lepton_eta[i], lepton_pt[i], SF_path_ttHMVA.size()==1 ? 0 : run_period - 1, cfg , "ttHMVA");
	  }
	  // scale factor = HWW x ttHMVA
	  SF_vect.push_back( res_ttHMVA );
	  //SF_vect.push_back( res * res_ttHMVA );
	  //SF_vect.push_back(std::get<0>(res)*std::get<0>(res_ttHMVA));
	  //SF_err_vect.push_back(TMath::Sqrt(TMath::Power(std::get<1>(res), 2) + TMath::Power(std::get<2>(res), 2)                
	  //+ TMath::Power(std::get<1>(res_ttHMVA), 2) + TMath::Power(std::get<2>(res_ttHMVA), 2) ));
	}
	else if(TMath::Abs(pdgId[i]) == 13){
	  std::cout<<"Impossible, we only look at e-e phase space"<<std::endl;
	  exit(0);
	}
      } // end of loops
      
      double SF = 1.;
      
      // Calculate product of IsIso_SFs for all leptons in the event
      for(auto x : SF_vect) SF *= x;
      
      return SF;
    };
  
  std::cout<<" --> default HWW WP : "<< cfg.HWW_WP[cfg.year] <<std::endl;
  
  df = df
    .Define( "HWW_WP_cut" , cfg.HWW_WP[cfg.year] )
    .Define( "LepCut2l__ele_mu_HWW_tthMVA" , "HWW_WP_cut*( ( abs(Lepton_pdgId[0])==11 || Muon_mvaTTH[Lepton_muonIdx[0]]>0.8 ) && ( abs(Lepton_pdgId[1])==11 || Muon_mvaTTH[Lepton_muonIdx[1]]>0.8 ) && ( abs(Lepton_pdgId[0])==13 || Electron_mvaTTH[Lepton_electronIdx[0]]>0.70) && ( abs(Lepton_pdgId[1])==13 || Electron_mvaTTH[Lepton_electronIdx[1]]>0.70) )");
  // mc only
  if (cfg.isMC) df = df.Define( "LepSF2l__ele_mu_HWW_ttHMVA" , hww_tthmva_sf_maker , { "run_period" , "Lepton_pdgId" , "Lepton_pt" , "Lepton_eta" } );
  
  return df;
}

#endif
