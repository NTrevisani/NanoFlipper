#ifndef HELPER_H
#define HELPER_H
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDFHelpers.hxx"
#include "ROOT/RVec.hxx"

#include "Math/Vector4D.h"
#include "TStopwatch.h"

#include <iostream>
#include <sstream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <cmath>
#include <map>

#include "utility" // std::pair
#include <algorithm> // for std::find
#include <iterator> // for std::begin, std::end

#include "TRandom3.h"
#include "TLorentzVector.h"

#include "config.h"

namespace Helper {
  template <typename T>
    void leptonID(T &mycfg){ 
    // HWW electron SF
    mycfg.SF_files_map["electron"]["TightObjWP"]["2016"]["idSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingTight80XHWW.txt" };
    mycfg.SF_files_map["electron"]["TightObjWP"]["2017"]["idSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017runB.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017runC.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017runD.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017runE.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017runF.txt"
    };
    mycfg.SF_files_map["electron"]["TightObjWP"]["2018"]["idSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingTight102XHWW_runABCD.txt" };
    // ttHMVA electron SF
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2016"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2016.txt" };
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2017"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunB.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunCD.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunE.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunF.txt"
    };                                                                                                                                   
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2018"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2018.txt" };   
    
    
    // HWW muon SF
    mycfg.SF_files_map["muon"]["TightObjWP"]["2016"]["idSF"]  = { mycfg.base + "/data/HWW_SF/muonID_TH2_SFs_2016_pt_eta.root" };
    mycfg.SF_files_map["muon"]["TightObjWP"]["2016"]["isoSF"] = { mycfg.base + "/data/HWW_SF/muonISO_TH2_SFs_2016_pt_eta.root" };
    mycfg.SF_files_map["muon"]["TightObjWP"]["2017"]["idSF"]  = { mycfg.base + "/data/HWW_SF/muonID_cut_Tight_HWW_combined_2017.root" };
    mycfg.SF_files_map["muon"]["TightObjWP"]["2017"]["isoSF"] = { mycfg.base + "/data/HWW_SF/muonISO_cut_Tight_HWW_combined_2017.root" };
    mycfg.SF_files_map["muon"]["TightObjWP"]["2018"]["idSF"]  = { mycfg.base + "/data/HWW_SF/muonID_TH2_SFs_2018_pt_eta.root" };
    mycfg.SF_files_map["muon"]["TightObjWP"]["2018"]["isoSF"] = { mycfg.base + "/data/HWW_SF/muonISO_TH2_SFs_2018_pt_eta.root" };
    
    // ttHMVA muon SF
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2016"]["ttHMVA"]     = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_2016.root" };
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2016"]["ttHMVA_SYS"] = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_SYS_2016.root" };
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2017"]["ttHMVA"]     = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_2017.root" };
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2017"]["ttHMVA_SYS"] = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_SYS_2017.root" };
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2018"]["ttHMVA"]     = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_2018.root" };
    mycfg.SF_files_map["muon"]["ttHMVA0p8"]["2018"]["ttHMVA_SYS"] = { mycfg.base + "/data/ttHMVA_SF/ttHMVA0p8_TightHWWCut_SFs_SYS_2018.root" };
    //
    
  }
  
  auto add_p4 = [](float pt, float eta, float phi)
    {
      return ROOT::Math::PtEtaPhiMVector(pt, eta, phi, 0.);
    };
  
  auto pair = [](ROOT::Math::PtEtaPhiMVector& p4_1, ROOT::Math::PtEtaPhiMVector& p4_2)
    {
      return std::vector<float>( { float((p4_1+p4_2).Pt()) , float((p4_1+p4_2).Eta()) , float((p4_1+p4_2).Phi()) , float((p4_1+p4_2).M()) } );
    };
  
}
#endif
