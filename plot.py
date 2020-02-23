# Implementation of the plotting step of the analysis
# The plotting combines the histograms to plots which allow us to study the
# initial dataset based on observables motivated through physics.

import argparse
import ROOT
from helper import *
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2()
ROOT.gStyle.SetOptStat(0)

# Declare human readable label for each variable
labels = {
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

def main(path, output, variable, xlabel, scale, ratio=0, logy=False):
    tfile = ROOT.TFile(path, "READ")

    hist={}
    
    ########################################################################
    # Simulation
    #  DY
    DY = getHistogram(tfile, "DYJetsToLL_M-10to50-LO", variable)
    DY2 = getHistogram(tfile, "DYJetsToLL_M-50-LO_ext2", variable)
    DY.Add(DY2)
    hist['DY'] = DY
    
    # clone bkgsum template
    hist['BkgSum'] = hist['DY'].Clone("BkgSum")
    
    # Data
    data = getHistogram(tfile, "DoubleEG", variable)
    hist['DATA'] = data

    # Fake
    fake = getHistogram(tfile, "DoubleEG_fake", variable)
    hist['Fake'] = fake

    ######################################################################3
    # Plotting style
    #hist['BkgSum'].Reset("MICES")
    hist['BkgSum'].SetFillStyle(3003)
    hist['BkgSum'].SetFillColor(1)
    hist['BkgSum'].SetMarkerStyle(0)

    # simulation
    hist['DY'].SetFillColor(418)
    hist['DY'].SetFillStyle(1001)
    hist['DY'].SetLineColor(418)
    hist['DY'].SetLineStyle(1)
    hist['DY'].SetLineWidth(2)

    # data
    hist['DATA'].SetMarkerStyle(20)
    hist['DATA'].SetMarkerSize(1.25)
    hist['DATA'].SetFillColor(418)
    hist['DATA'].SetFillStyle(1001)
    hist['DATA'].SetLineColor(1)
    hist['DATA'].SetLineStyle(1)
    hist['DATA'].SetLineWidth(2)

    # fake
    hist['Fake'].SetFillColor(921)
    hist['Fake'].SetFillStyle(1001)
    hist['Fake'].SetLineColor(921)
    hist['Fake'].SetLineStyle(1)
    hist['Fake'].SetLineWidth(2)

    #############################################################################

    for i, s in enumerate(hist):
        addOverflow(hist[s], False) # Add overflow

    # stack
    bkg = THStack('bkg', ";"+xlabel+";"+hist['BkgSum'].GetYaxis().GetTitle())
    for proc in [ 'DY' , 'Fake' ]:
        bkg.Add(hist[proc]) # ADD ALL BKG

    #Legend
    n=len(hist)
    leg = TLegend(0.7, 0.9-0.05*n, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetTextSize(0.03)
    leg.AddEntry(hist['DATA'], 'Data', "pl")
    leg.AddEntry(hist['DY'], 'DY', "f")
    leg.AddEntry(hist['Fake'], 'Fake', "f")
    c1 = TCanvas("c1", list(hist.values())[-1].GetXaxis().GetTitle(), 800, 800 if ratio else 600 )

    #Ratio pad
    if ratio:
        c1.Divide(1, 2)
        setTopPad(c1.GetPad(1), ratio)
        setBotPad(c1.GetPad(2), ratio)

    c1.cd(1)
    c1.GetPad(bool(ratio)).SetTopMargin(0.06)
    c1.GetPad(bool(ratio)).SetRightMargin(0.05)
    c1.GetPad(bool(ratio)).SetTicks(1, 1)
    if logy:
        c1.GetPad(bool(ratio)).SetLogy()

    #Draw
    bkg.Draw("HIST") # stack
    hist['BkgSum'].Draw("SAME, E2") # sum of bkg
    hist['DATA'].Draw("SAME, PE") # data

    bkg.GetYaxis().SetTitleOffset(bkg.GetYaxis().GetTitleOffset()*1) #1.075
    bkg.SetMaximum((6.0 if logy else 1.5)*max(bkg.GetMaximum(), hist['DATA'].GetBinContent(hist['DATA'].GetMaximumBin())+hist['DATA'].GetBinError(hist['DATA'].GetMaximumBin())))
    bkg.SetMinimum(max(min(hist['BkgSum'].GetBinContent(hist['BkgSum'].GetMinimumBin()), hist['DATA'].GetMinimum()), 5.e-1)  if logy else 0.)

    #bkg.SetMinimum(1.0)

    leg.Draw()

    setHistStyle(bkg, 1.2 if ratio else 1.1)
    setHistStyle(hist['BkgSum'], 1.2 if ratio else 1.1)

    #####################################################################
    if ratio:
        c1.cd(2)
        err = hist['BkgSum'].Clone("BkgErr;")
        err.SetTitle("")
        err.GetYaxis().SetTitle("Data / Bkg")
        err.GetXaxis().SetTitle(xlabel)
        for i in range(1, err.GetNbinsX()+1):
            err.SetBinContent(i, 1)
            if hist['BkgSum'].GetBinContent(i) > 0:
                err.SetBinError(i, hist['BkgSum'].GetBinError(i)/hist['BkgSum'].GetBinContent(i))
        setBotStyle(err)
        errLine = err.Clone("errLine")
        errLine.SetLineWidth(1)
        errLine.SetFillStyle(0)
        errLine.SetLineColor(1)
        err.Draw("E2")
        errLine.Draw("SAME, HIST")

        if 'DATA' in hist:
            res = hist['DATA'].Clone("Residues")
            for i in range(0, res.GetNbinsX()+1):
                if hist['BkgSum'].GetBinContent(i) > 0:
                    res.SetBinContent(i, res.GetBinContent(i)/hist['BkgSum'].GetBinContent(i))
                    res.SetBinError(i, res.GetBinError(i)/hist['BkgSum'].GetBinContent(i))
            setBotStyle(res)
            res.Draw("SAME, PE0")
            if len(err.GetXaxis().GetBinLabel(1))==0: # Bin labels: not a ordinary plot
                drawRatio(hist['DATA'], hist['BkgSum'])
                drawKolmogorov(hist['DATA'], hist['BkgSum'])
        else: res = None
    c1.cd(1)
    drawCMS("%s" %scale, "Object Study")

    c1.Update()
    
    c1.SaveAs("{}/{}.pdf".format(output, variable))
    c1.SaveAs("{}/{}.png".format(output, variable))


# Loop over all variable names and make a plot for each
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Full path to ROOT file with all histograms")
    parser.add_argument("output", type=str, help="Output directory for plots")
    parser.add_argument("scale", type=float, help="Scaling of the integrated luminosity")
    args = parser.parse_args()
    for variable in labels.keys():
        for reg in ['OS','SS']:
            var = variable+'_%s' %reg
            main(args.path, args.output, var, labels[variable] , args.scale, 4, True if 'pt' in variable else False )
        
