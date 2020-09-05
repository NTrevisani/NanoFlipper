#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"

#include "Math/Vector4D.h"
#include "TStopwatch.h"

#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>
#include <cmath>

/*
 * preselection (skim) on the lepton
 */

template <typename T>
auto pt_Sel(T &df) {
  return df.Filter("Sum(abs(Lepton_pdgId)==11) >=2 ","Two or more electrons")
           .Filter("( (nLepton==2 && Lepton_pt[0] > 25 && Lepton_pt[1] > 20 ) || (nLepton>2 && Lepton_pt[0] > 25 && Lepton_pt[1] > 20 && Lepton_pt[2] < 10 ) )","Pt selection");
}

template <typename T>
auto Zmass_Sel(T &df) {
  return df.Filter("abs(mll-91.2) < 15","Z mass window selection");
}

/*
 * Declare variables for analysis
 */

template <typename T>
auto DeclareVariables(T &df) {

  return df.Define("ele_pt1","(Lepton_electronIdx[0]!=-1)*Lepton_pt[0]")
           .Define("ele_pt2","(Lepton_electronIdx[1]!=-1)*Lepton_pt[1]")
           .Define("ele_eta1","(Lepton_electronIdx[1]!=-1)*Lepton_eta[0]")
           .Define("ele_eta2","(Lepton_electronIdx[1]!=-1)*Lepton_eta[1]")
           .Define("absele_eta1","(Lepton_electronIdx[1]!=-1)*abs(Lepton_eta[0])")
           .Define("absele_eta2","(Lepton_electronIdx[1]!=-1)*abs(Lepton_eta[1])")
           .Define("ispt2low1","(Lepton_electronIdx[1]!=-1)*( Lepton_pt[1] > 20 && Lepton_pt[1] < 35 )")
           .Define("ispt2low2","(Lepton_electronIdx[1]!=-1)*( Lepton_pt[1] > 35 && Lepton_pt[1] < 50 )")
           .Define("ispt2low3","(Lepton_electronIdx[1]!=-1)*( Lepton_pt[1] > 50 && Lepton_pt[1] < 200 )")
           .Define("isOS","( (Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) || (Lepton_pdgId[0]*Lepton_pdgId[1]==11*-11) )")
           .Define("isSS","(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)");
}

/*
 * Add event weights
 */

template <typename T>
auto AddEventWeight(T &df, const std::string& path, const std::string& sample, const std::string& lumi, const std::string& weight1, const std::string& weight2) {
  std::string weights;
  if (sample.find("Double") != std::string::npos) {
    if (path.find("fake") != std::string::npos ){
      weights = "METFilter_DATA*fakeW2l_"+weight1+"*("+weight2+")";
    }
    else{
      weights = "METFilter_DATA*LepCut2l__"+weight1+"*("+weight2+")";
    }
  }
  else {
    weights = lumi+"*XSWeight*SFweight2l*LepSF2l__"+weight1+"*LepCut2l__"+weight1+"*PrefireWeight*GenLepMatch2l*METFilter_MC*("+weight2+")";
  }
  std::cout<<" weights interpreted : "<<weights<<std::endl;
  return df.Define( "weight", weights );
}

/*
 * Declare all variables which will end up in the final reduced dataset
 */
const std::vector<std::string> finalVariables = {
  "ele_pt1" , "ele_pt2" , "ele_eta1" , "ele_eta2" , "absele_eta1" , "absele_eta2" , "mll" , "weight" , "ispt2low1" , "ispt2low2" , "ispt2low3" , "isOS" , "isSS"
};

/*
 * Main function, skimming step of analysis
 * The function loops over the input samples,
 * and write them to new files
 */
int main(int argc, char **argv) {
  
  ROOT::EnableImplicitMT(10);
  
  if(argc != 7) {
        std::cout << "Use executable with following arguments: ./skim input output integrated_luminosity weight1 weight2" << std::endl;
        return -1;
    }
    std::string input = argv[1];
    std::cout << ">>> Process input: " << input << std::endl;

    const std::string path = argv[1];
    const std::string sample = argv[3];
    std::cout << "Looking at : " << path+"*"+sample+"*.root" << std::endl;

    const auto lumi = argv[4];
    std::cout << "Integrated luminosity: " << lumi << std::endl;

    const std::string weight1 = argv[5];
    const std::string weight2 = argv[6];
    std::cout << "weight1 : " << weight1 << std::endl;
    std::cout << "weight2 : " << weight2 << std::endl;

    TStopwatch time;
    time.Start();

    ROOT::RDataFrame df("Events", path+"*"+sample+"*.root" );
    //const auto numEvents = *df.Count();
    //std::cout << "Number of events: " << numEvents << std::endl;

    auto df1 = pt_Sel(df);
    auto df2 = Zmass_Sel(df1);
    
    // should be applied last step
    auto df3 = DeclareVariables(df2);
    auto df4 = AddEventWeight(df3 , path, sample , lumi , weight1 , weight2 );

    auto dfFinal = df4;
    auto report = dfFinal.Report();
    const std::string output = argv[2];
    std::cout << "Output name: " << output << std::endl;
    dfFinal.Snapshot("Events", output, finalVariables);
    time.Stop();

    report->Print();
    time.Print();
}
