# Implementing histogramming

import argparse
import ROOT
ROOT.gROOT.SetBatch(True)

# Declare range of the histogram for each variables
# Each entry in the dictionary contains of the variable name as key and a tuple
# specifying the histogram layout as value. The tuple sets the number of bins,
# the lower edge and the upper edge of the histogram.
default_nbins = 30
ranges = {
    "ele_pt1"  : (default_nbins, 0, 200),
    "ele_pt2"  : (default_nbins, 0, 200),
    "ele_eta1" : (default_nbins, -2.5, 2.5),
    "ele_eta2" : (default_nbins, -2.5, 2.5),
    "mll"      : (default_nbins, 70, 110),
    }

# Book a histogram for a specific variable
def bookHistogram(df, variable, range_):
    return df.Histo1D(ROOT.ROOT.RDF.TH1DModel(variable, variable, range_[0], range_[1], range_[2]),\
                      variable, "weight")

# Write a histogram with a given name to the output ROOT file
def writeHistogram(h, name):
    h.SetName(name)
    h.Write()

# main function will loop over the outputs from the skimming step and produces
# required histograms for the final plotting.
# perform selection on same sign and opposite sign only
def main(sample, process, output):
    # Create output file
    tfile = ROOT.TFile(output, "RECREATE")
    variables = ranges.keys()

    # Process skimmed datasets and produce histograms of variables
    print(">>> Process skimmed sample {} for process {}".format(sample, process))

    # Load skimmed dataset and apply baseline selection (if any)
    df = ROOT.ROOT.RDataFrame("Events", sample)

    # Book histograms for opposite sign
    df1 = df.Filter("isOS", "Opposite sign region")
    hists_os = {}
    for variable in variables:
        hists_os[variable] = bookHistogram(df1, variable, ranges[variable])
    report1 = df1.Report()

    # Book histogram for same sign
    df2 = df.Filter("isSS", "Same sign region")
    hists_ss = {}
    for variable in variables:
        hists_ss[variable] = bookHistogram(df2, variable, ranges[variable])
    report2 = df2.Report()

    # Write histograms to output file
    for variable in variables:
        writeHistogram(hists_os[variable], "{}_{}_OS".format(process, variable))
    for variable in variables:
        writeHistogram(hists_ss[variable], "{}_{}_SS".format(process, variable))

    # Print cut-flow report
    print("Cut-flow report (signal region):")
    report1.Print()
    print("Cut-flow report (control region):")
    report2.Print()

    tfile.Close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sample", type=str, help="Full path to skimmed sample")
    parser.add_argument("process", type=str, help="Process name")
    parser.add_argument("output", type=str, help="Output file with histograms")
    args = parser.parse_args()
    main(args.sample, args.process, args.output)
    
