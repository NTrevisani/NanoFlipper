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
    mycfg.SF_files_map["electron"]["TightObjWP"]["2016"]["wpSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA80Xwp90Iso16.txt" };
    mycfg.SF_files_map["electron"]["TightObjWP"]["2017"]["wpSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunB.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunCD.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunE.txt",
								     mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2017RunF.txt"
    };
    mycfg.SF_files_map["electron"]["TightObjWP"]["2018"]["wpSF"] = { mycfg.base + "/data/HWW_SF/egammaEffi_passingMVA102Xwp90isoHWWiso0p06_2018.txt" };
    
    ////////////////////////
    // ttHMVA electron SF
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2016"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2016.txt" };
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2017"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunB.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunCD.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunE.txt",
								      mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2017RunF.txt"
    };                                                                                                                                   
    mycfg.SF_files_map["electron"]["ttHMVA0p7"]["2018"]["ttHMVA"] = { mycfg.base + "/data/ttHMVA_SF/egammaEffi_TightHWW_ttHMVA_0p7_SFs_2018.txt" };   
  }
}
#endif
