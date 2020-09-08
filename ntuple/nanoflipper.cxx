#include "interface/helper.h"
#include "interface/config.h"

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
  
  ROOT::RDataFrame df("Events", infiles);
  auto outdf=df.Filter("nLepton==2 || (nLepton>2 && Lepton_pt[2]<10)","nlepton cut")
    .Filter("Lepton_pt[0]>25 && Lepton_pt[1]>12","lepton pt cut")
    .Filter("abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11","ee channel")
    .Filter("abs(mll-91.2)<15","mll cut")
    .Define("lep1_pt"    , "Lepton_pt[0]")
    .Define("lep1_eta"   , "Lepton_eta[0]")
    .Define("lep1_pdgId" , "Lepton_pdgId[0]")
    .Define("lep2_pt"    , "Lepton_pt[1]")
    .Define("lep2_eta"   , "Lepton_eta[1]")
    .Define("lep2_pdgId" , "Lepton_pdgId[1]")
    ;
  
  if (mycfg.isMC){
    outdf = outdf.Define("genmatch" , "Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]")
      .Define("ptllDYW"    , mycfg.ptllDYW_LO[year]);
  }
  else{
    std::string tname = name;
    std::string s = "Fake_";
    std::string::size_type iss = tname.find(s);
    if (iss != std::string::npos)
      tname.erase(iss, s.length());
    //
    outdf = outdf.Define("trigger"    , mycfg.trigger[tname] );
  }
  
  //ROOT::RDF::SaveGraph(df,"graph_"+sample+".dot");
  if (name.find("Fake_") != std::string::npos){
    std::cout<<"Processing fake output"<<std::endl;
    outdf.Snapshot( "flipper", output, mycfg.outBranch[ "fake_"+year ] );
  }
  else{
    outdf.Snapshot( "flipper", output, mycfg.outBranch[ (mycfg.isMC) ? "mc_"+year : "data_"+year ] );
  }
  auto report = outdf.Report();
  report->Print();
  time.Stop();
  time.Print();
}
