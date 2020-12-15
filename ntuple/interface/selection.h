#ifndef SELECTION_H
#define SELECTION_H

#include "helper.h"
#include "config.h"

template < typename T>
auto twoLep_selection( T &df ){
  
  auto df1 = df
    .Filter("nLepton==2 || ( nLepton>3 && Lepton_pt[2]<10 )","Nlepton cut : ( nLepton==2 || ( nLepton>=3 && Lepton_pt[2]<10 ) )")
    .Filter("Lepton_pt[0]>15 && Lepton_pt[1]>15","Lepton pt cut : (Lepton_pt[0]>15 && Lepton_pt[1]>15)")
    .Filter("abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11","e-e channel : ( abs(Lepton_pdgId[0]*Lepton_pdgId[1])==11*11 )")
    ;
  auto df2 = df1
    .Define("lep1_pt"    , "Lepton_pt[0]")
    .Define("lep1_eta"   , "Lepton_eta[0]")
    .Define("lep1_phi"   , "Lepton_phi[0]")
    .Define("lep1_pdgId" , "Lepton_pdgId[0]")
    .Define("lep2_pt"    , "Lepton_pt[1]")
    .Define("lep2_eta"   , "Lepton_eta[1]")
    .Define("lep2_phi"   , "Lepton_phi[1]")
    .Define("lep2_pdgId" , "Lepton_pdgId[1]")
    .Define("lep3_pt"    , "Lepton_pt[2]")
    .Define("lep3_eta"   , "Lepton_eta[2]")
    .Define("lep3_phi"   , "Lepton_phi[2]")
    .Define("lep3_pdgId" , "Lepton_pdgId[2]")
    .Define( "addp4_1" , Helper::add_p4 , { "lep1_pt" , "lep1_eta" , "lep1_phi" } )
    .Define( "addp4_2" , Helper::add_p4 , { "lep2_pt" , "lep2_eta" , "lep2_phi" } )
    .Define( "pair" , Helper::pair , { "addp4_1" , "addp4_2" } )
    .Define( "Mll" , "pair[3]" )
    ;
  return df2;
}

template < typename T >
auto threeLep_selection( T &df ){
  
  auto df1 = df
    .Filter("nLepton==3 || ( nLepton>3 && Lepton_pt[3]<10 )","three leptons final state")
    .Filter("Lepton_pt[0]>15 && Lepton_pt[1]>5","Lepton pt cut : (Lepton_pt[0]>15 && Lepton_pt[1]>5)")
    .Filter("abs(Lepton_pdgId[0])==13","one leading pt muon")
    .Filter("abs(Lepton_pdgId[1]*Lepton_pdgId[2])==11*11" , "two sub-leading pt electrons")
    ;
  
  auto df2 = df1
    .Define("lep1_pt"    , "Lepton_pt[0]")
    .Define("lep1_eta"   , "Lepton_eta[0]")
    .Define("lep1_phi"   , "Lepton_phi[0]")
    .Define("lep1_pdgId" , "Lepton_pdgId[0]")
    .Define("lep2_pt"    , "Lepton_pt[1]")
    .Define("lep2_eta"   , "Lepton_eta[1]")
    .Define("lep2_phi"   , "Lepton_phi[1]")
    .Define("lep2_pdgId" , "Lepton_pdgId[1]")
    .Define("lep3_pt"    , "Lepton_pt[2]")
    .Define("lep3_eta"   , "Lepton_eta[2]")
    .Define("lep3_phi"   , "Lepton_phi[2]")
    .Define("lep3_pdgId" , "Lepton_pdgId[2]")
    .Define( "addp4_1" , Helper::add_p4 , { "lep2_pt" , "lep2_eta" , "lep2_phi" } )
    .Define( "addp4_2" , Helper::add_p4 , { "lep3_pt" , "lep3_eta" , "lep3_phi" } )
    .Define( "pair" , Helper::pair , { "addp4_1" , "addp4_2" } )
    .Define( "Mll" , "pair[3]" );
  return df2;
}

#endif
