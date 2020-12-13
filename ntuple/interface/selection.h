#ifndef SELECTION_H
#define SELECTION_H

#include "helper.h"
#include "config.h"

template < typename T >
auto selection( T &df, const std::string &input_ ){
  
  auto add_p4 = [](float pt, float eta, float phi)
    {
      return ROOT::Math::PtEtaPhiMVector(pt, eta, phi, 0.);
    };
  
  auto pair = [](ROOT::Math::PtEtaPhiMVector& p4_1, ROOT::Math::PtEtaPhiMVector& p4_2)
    {
      return std::vector<float>( { float((p4_1+p4_2).Pt()) , float((p4_1+p4_2).Eta()) , float((p4_1+p4_2).Phi()) , float((p4_1+p4_2).M()) } );
    };
  
  if ( input_.find("SingleMuon") != std::string::npos ){
    auto df1 = df
      .Filter("nLepton==3 || ( nLepton>=4 && Lepton_pt[3]<10 )","Muon tagged di-electron")
      .Filter("Lepton_pt[0]>15 && Lepton_pt[1]>15","Lepton pt cut : (Lepton_pt[0]>15 && Lepton_pt[1]>15)")
      .Filter("abs(Lepton_pdgId[0])==13","leading muon tagging : ( abs(Lepton_pdgId[0])==13 )")
      .Filter("abs(Lepton_pdgId[1]*Lepton_pdgId[2])==11*11","e-e channel : ( abs(Lepton_pdgId[1]*Lepton_pdgId[2])==11*11 )");
    auto df2 = df1
      .Define( "lep1pt" , "Lepton_pt[1]" ).Define( "lep1eta" , "Lepton_eta[1]" ).Define( "lep1phi" , "Lepton_phi[1]" )
      .Define( "lep2pt" , "Lepton_pt[2]" ).Define( "lep2eta" , "Lepton_eta[2]" ).Define( "lep2phi" , "Lepton_phi[2]" )
      .Define( "addp4_1" , add_p4 , { "lep1pt" , "lep1eta" , "lep1phi" } )
      .Define( "addp4_2" , add_p4 , { "lep2pt" , "lep2eta" , "lep2phi" } )
      .Define( "pair" , pair , { "addp4_1" , "addp4_2" } )
      .Define( "Mll" , "pair[3]" );
    return df2;
  }
  else{
    auto df1 = df
      .Filter("nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 )","Nlepton cut : ( nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 ) )")
      .Filter("Lepton_pt[0]>15 && Lepton_pt[1]>15","Lepton pt cut : (Lepton_pt[0]>15 && Lepton_pt[1]>15)")
      .Filter("abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11","e-e channel : ( abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11 )");
    auto df2 = df1      
      .Define( "lep1pt" , "Lepton_pt[0]" ).Define( "lep1eta" , "Lepton_eta[0]" ).Define( "lep1phi" , "Lepton_phi[0]" )
      .Define( "lep2pt" , "Lepton_pt[1]" ).Define( "lep2eta" , "Lepton_eta[1]" ).Define( "lep2phi" , "Lepton_phi[1]" )
      .Define( "addp4_1" , add_p4 , { "lep1pt" , "lep1eta" , "lep1phi" } )
      .Define( "addp4_2" , add_p4 , { "lep2pt" , "lep2eta" , "lep2phi" } )
      .Define( "pair" , pair , { "addp4_1" , "addp4_2" } )
      .Define( "Mll" , "pair[3]" );
    return df2;
  }
  
}

#endif
