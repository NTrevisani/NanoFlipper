#include "interface/helper.h"
#include "interface/config.h"
#include "interface/SF_maker.h"

int main(int argc, char **argv) {

  ROOT::EnableImplicitMT(12);

  if(argc != 6) {
    std::cout << "Use executable with following arguments: ./nanotnp name input output integrated_luminosity year" << std::endl;
    return -1;
  }

  const std::string name   = argv[1];
  const std::string input  = argv[2];
  const std::string output = argv[3];
  const std::string lumi   = argv[4];
  const std::string year   = argv[5];

  // init cfg
  config_t mycfg;
  mycfg.lumi = lumi;
  mycfg.year = year;
  mycfg.isMC = (input.find("DYJetsToLL") != std::string::npos) ? true : false;
  mycfg.base = std::getenv("PWD");

  std::cout << ">>> Process is mc: " << mycfg.isMC << std::endl;
  std::cout << ">>> Process input: " << input << std::endl;
  std::cout << ">>> Process output: " << output << std::endl;
  std::cout << ">>> Integrated luminosity: " << mycfg.lumi << std::endl;
  std::cout << ">>> Year: " << mycfg.year << std::endl;

  // Initialize time
  TStopwatch time;
  time.Start();

  // filelist
  std::vector<std::string> infiles;
  std::ifstream file(input);
  std::string str;
  while (std::getline(file, str)) { infiles.push_back(str); }
  
  if (mycfg.isMC) {
    // set path
    Helper::leptonID(mycfg);
    // electron
    makeSF_ele( mycfg.SF_files_map["electron"]["TightObjWP"][year]["wpSF"]  , mycfg.h_SF_ele , mycfg.h_SF_ele_err , mycfg.h_SF_ele_sys );
    makeSF_ele( mycfg.SF_files_map["electron"]["ttHMVA0p7"][year]["ttHMVA"] , mycfg.h_SF_ele_ttHMVA , mycfg.h_SF_ele_ttHMVA_err , mycfg.h_SF_ele_ttHMVA_sys );
    // muon
    makeSF_muon( mycfg.SF_files_map["muon"]["TightObjWP"][year]["idSF"]  , mycfg.h_SF_mu_Id , mycfg.h_SF_mu_Id_err , mycfg.h_SF_mu_Id_sys , "Muon_idSF2D" ); //  IdSF
    makeSF_muon( mycfg.SF_files_map["muon"]["TightObjWP"][year]["isoSF"]  , mycfg.h_SF_mu_Iso , mycfg.h_SF_mu_Iso_err , mycfg.h_SF_mu_Iso_sys , "Muon_isoSF2D" ); // IsoSF 
    std::pair< std::list<std::string> , std::list<std::string> > listPair = std::make_pair(
											   mycfg.SF_files_map["muon"]["ttHMVA0p8"][year]["ttHMVA"] ,
											   mycfg.SF_files_map["muon"]["ttHMVA0p8"][year]["ttHMVA_SYS"]
											   );
    makeSF_muon_tthMVA( listPair  , mycfg.h_SF_mu_ttHMVA , mycfg.h_SF_mu_ttHMVA_err , mycfg.h_SF_mu_ttHMVA_sys , "ttHMVA0p8_TightHWWCut" );
  }
  //mycfg.listSize = SF_files_map["electron"]["TightObjWP"][year]["ttHMVA"].size();

  ROOT::RDataFrame df("Events", infiles);
  auto pre_outdf = df
    .Filter("nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 )","Nlepton cut : ( nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 ) )")
    .Filter("Lepton_pt[0]>23 && Lepton_pt[1]>12","Lepton pt cut : (Lepton_pt[0]>23 && Lepton_pt[1]>12)")
    .Filter("abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11","e-e channel : ( abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11 )")
    .Filter("abs(mll-91.2)<15" , "DY region : ( abs(mll-91.2)<15 )")
    .Define("lep1_pt"    , "Lepton_pt[0]")
    .Define("lep1_eta"   , "Lepton_eta[0]")
    .Define("lep1_pdgId" , "Lepton_pdgId[0]")
    .Define("lep2_pt"    , "Lepton_pt[1]")
    .Define("lep2_eta"   , "Lepton_eta[1]")
    .Define("lep2_pdgId" , "Lepton_pdgId[1]");

  // make lepton SF
  auto outdf = hww_tthmva_sf( pre_outdf , mycfg ); 

  if (mycfg.isMC){
    // gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
    outdf = outdf
      .Define("gen_promptmatch" , "Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]")
      .Define("ptllDYW"    , mycfg.ptllDYW_LO[year]);
  }
  else{
    std::string tname = name;
    std::string s = "Fake_";
    std::string::size_type iss = tname.find(s);
    if (iss != std::string::npos)
      tname.erase(iss, s.length());
    outdf = outdf.Define( "trigger" , mycfg.trigger[tname] );
  }

  if (name.find("Fake_") != std::string::npos){
    std::cout<<"Processing fake output"<<std::endl;
    outdf.Snapshot( "flipper", output, mycfg.outBranch[ "fake_"+year ] );
  }
  else{
    outdf.Snapshot( "flipper", output, mycfg.outBranch[ (mycfg.isMC) ? "mc_"+year : "data_"+year ] );
  }
  ROOT::RDF::SaveGraph( outdf ,"graph_flip.dot");                                                                                                                                                         
  auto report = outdf.Report();
  report->Print();
  
  time.Stop();
  time.Print();
}
