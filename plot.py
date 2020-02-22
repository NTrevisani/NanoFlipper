# Implementation of the plotting step of the analysis
# The plotting combines the histograms to plots which allow us to study the
# initial dataset based on observables motivated through physics.

import argparse
import ROOT
ROOT.gROOT.SetBatch(True)

# Declare human readable label for each variable
label = {
    "ele_pt1"  : "Electron 1 p_{T} / GeV",
    "ele_pt2"  : "Electron 2 p_{T} / GeV",
    "ele_eta1" : "Electron 1 #eta",
    "ele_eta2" : "Electron 2 #eta",
    "mll"      : "M(ll) / GeV",
    }

# Specify the color for each process
colors = {
    "DY" : ROOT.TColor.GetColor(418),
}

# Retrieve a histogram from the input file based on the process and the variable
# name
def getHistogram(tfile, name, variable, tag=""):
    name = "{}_{}{}".format(name, variable, tag)
    h = tfile.Get(name)
    if not h:
        raise Exception("Failed to load histogram {}.".format(name))
    return h

# main function of the plotting step
#
# The major part of the code below is dedicated to define a nice-looking layout.
# The interesting part is the combination of the histograms to the QCD estimation.
# There, we take the data histogram from the control region and subtract all known
# processes defined in simulation and define the remaining part as QCD. Then,
# this shape is extrapolated into the signal region with a scale factor.

def main(path, output, variable, scale):
    tfile = ROOT.TFile(path, "READ")
