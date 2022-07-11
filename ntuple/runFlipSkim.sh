#!/bin/bash

# Commands to produce charge-flip probabilities on nanoAOD_v5 production
# python flipskim.py -d nanov5_2016 --Samples "SingleElectron" --Samples "DoubleEG"           --Samples "DYJetsToLL_M-50-LO_ext2" --Samples "DYJetsToLL_M-50"      -b
# python flipskim.py -d nanov5_2017 --Samples "SingleElectron" --Samples "DoubleEG"           --Samples "DYJetsToLL_M-50-LO_ext1" --Samples "DYJetsToLL_M-50_ext1" -b
# python flipskim.py -d nanov5_2018 --Samples "EGamma"         --Samples "DYJetsToLL_M-50-LO" --Samples "DYJetsToLL_M-50_ext2"                                     -b

# python flipskim.py -d nanov5_2016 --Samples "SingleMuon"     --Samples "WZTo3LNu_mllmin01_ext1" --Samples "MuonEG" --Samples "DoubleMuon" --Samples "SingleElectron" --Samples "DoubleEG"


# Commands to produce charge-flip probabilities on nanoAOD_v7 production

# Testing on 2018
# python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/eos/user/n/ntrevisa/charge_flip/"  --Samples "EGamma" -b
# python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/eos/user/n/ntrevisa/charge_flip/"  --Samples "DYJetsToLL_M-50_ext2" -b
# python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/eos/user/n/ntrevisa/charge_flip/"  --Samples "DYJetsToLL_M-50-LO" -b

python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/results/"  --Samples "EGamma" -b
python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/results/"  --Samples "DYJetsToLL_M-50_ext2" -b
python flipskim.py --dataset 2018 --location "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/data/nano_v7/filelists/" --output "/afs/cern.ch/user/n/ntrevisa/work/latinos/charge_flip/CMSSW_12_4_0/src/NanoFlipper/ntuple/results/"  --Samples "DYJetsToLL_M-50-LO" -b

