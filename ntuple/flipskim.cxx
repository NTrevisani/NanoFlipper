#include "interface/helper.h"
#include "interface/config.h"
#include "interface/SF_maker.h"
#include "interface/selection.h"

int main(int argc, char **argv) {

  ROOT::EnableImplicitMT(12);

  if(argc != 5) {
    std::cout << "Use executable with following arguments: ./flipskim name input output year" << std::endl;
    return -1;
  }

  const std::string name   = argv[1];
  const std::string input  = argv[2];
  const std::string output = argv[3];
  const std::string year   = argv[4];

  // init cfg
  config_t mycfg;
  mycfg.year = year;
  mycfg.isMC = (input.find("DYJetsToLL") != std::string::npos) ? true : false;
  mycfg.base = std::getenv("PWD");

  std::cout << ">>> Process is mc: " << mycfg.isMC << std::endl;
  std::cout << ">>> Process input: " << input << std::endl;
  std::cout << ">>> Process output: " << output << std::endl;
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
    makeSF_ele( mycfg.SF_files_map["electron"]["ttHMVA0p7"][year]["ttHMVA"] , mycfg.h_SF_ele_ttHMVA );
  }

  ROOT::RDataFrame df( "Events", infiles);
  auto df1 = selection( df , input );
  auto df2 = df1
    .Filter("abs(Mll-91.2)<15" , "DY region : ( abs(mll-91.2)<15 )")
    .Define("lep1_pt"    , "Lepton_pt[0]")
    .Define("lep1_eta"   , "Lepton_eta[0]")
    .Define("lep1_pdgId" , "Lepton_pdgId[0]")
    .Define("lep2_pt"    , "Lepton_pt[1]")
    .Define("lep2_eta"   , "Lepton_eta[1]")
    .Define("lep2_pdgId" , "Lepton_pdgId[1]")
    .Define("lep3_pt"    , "Lepton_pt[2]")
    .Define("lep3_eta"   , "Lepton_eta[2]")
    .Define("lep3_pdgId" , "Lepton_pdgId[2]")
    ;
  
  // make lepton SF
  auto outdf = hww_tthmva_sf( df2 , mycfg );
  
  // staging out
  std::vector<std::string> outbranch;
  if ( name.find("Fake_") != std::string::npos ) {
    outbranch = mycfg.outBranch[ "fake_" + year ];
  }
  else{
    outbranch = mycfg.outBranch[ (mycfg.isMC) ? "mc_" + year : "data_" + year ];
  }
  
  if (mycfg.isMC){
    // gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
    outdf = outdf
      .Define("gen_promptmatch" , "Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]")
      .Define("ptllDYW"    , (name.find("LO") != std::string::npos) ? mycfg.ptllDYW_LO[year] : mycfg.ptllDYW_NLO[year] );
    // push back sf lep
    outbranch.push_back( mycfg.HWW_WP[year] );
    outbranch.push_back( mycfg.HWW_WP_SF[year] );
  }
  else{
    std::string tname = name;
    std::string s = "Fake_";
    std::string::size_type iss = tname.find(s);
    if (iss != std::string::npos)
      tname.erase(iss, s.length());
    std::cout<<"tname : "<< tname <<std::endl;
    outdf = outdf.Define( "trig_sngEl_dblEl" , mycfg.triggers[tname] );
  }
  
  outdf.Snapshot( "flipper", output, outbranch );
  
  ROOT::RDF::SaveGraph( outdf ,"graph_flip_"+name+".dot");
  
  auto report = outdf.Report();
  report->Print();
  
  time.Stop();
  time.Print();
}
