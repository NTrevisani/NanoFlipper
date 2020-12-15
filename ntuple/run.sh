#!/bin/bash

#python flipskim.py -d nanov5_2016 --Samples "SingleElectron" --Samples "DY" -t
#python flipskim.py -d nanov5_2017 --Samples "SingleElectron" --Samples "DY" -t
#python flipskim.py -d nanov5_2018 --Samples "SingleElectron" --Samples "DY" -t

python flipskim.py -d nanov5_2016 --Samples "WZTo3LNu_mllmin01_ext1" --Samples "SingleMuon" --Samples "MuonEG" --Samples "DoubleMuon" --Samples "SingleElectron" --Samples "DoubleEG"
#python flipskim.py -d nanov5_2017 --Samples "SingleMuon" --Samples "WZ" -t
#python flipskim.py -d nanov5_2018 --Samples "SingleMuon" --Samples "WZ" -t
