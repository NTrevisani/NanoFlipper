from ROOT import gROOT, TChain, TH2D, TCanvas, gStyle, TH1, TMath
from ROOT import TEfficiency, TCanvas, TFile
import ROOT
import os, sys
import numpy as np
from ROOT import array
import time
from collections import OrderedDict

ROOT.ROOT.EnableImplicitMT(12)

TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

from optparse import OptionParser
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
(options, args) = parser.parse_args()

DIR = os.getcwd()
dataset= options.dataset
variables=['lep1_pt','lep1_eta','lep2_pt','lep2_eta','mll','2d']
ntupleDIR= DIR+"/../ntuple/results/"+dataset

start_time = time.time()

DF= OrderedDict({
    'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
    'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/SingleElectron.root' , ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] )
})

signness= OrderedDict({
    'os' : 'lep1_pdgId*lep2_pdgId == -11*11',
    'ss' : 'lep1_pdgId*lep2_pdgId == 11*11'
})

ptbin= OrderedDict({
    'trigpt' : 'lep1_pt > 23 && lep2_pt > 23',
    'highpt' : 'lep1_pt > 25 && lep2_pt > 25',
    'lowpt2' : 'lep1_pt > 25 && lep2_pt > 35',
    'lowpt1' : 'lep1_pt > 25 && lep2_pt <= 35 && lep2_pt > 25',
    'lowpt0' : 'lep1_pt > 25 && lep2_pt <= 25 && lep2_pt > 12'
})

eta_bin = ['0.','1.0','1.5','2.5']
#eta_bin = [ 0. , 0.5  , 1.0  , 1.5  , 2.0 , 2.5 ]
etagrid=np.zeros((len(eta_bin)-1,len(eta_bin)-1),dtype=np.object)
for i in range(len(etagrid)):
    for j in range(len(etagrid[i])):
        etagrid[i][j]='abs(lep1_eta)>='+str(eta_bin[i])+' && abs(lep1_eta)<'+str(eta_bin[i+1])+' && abs(lep2_eta)>='+str(eta_bin[j])+' && abs(lep2_eta)<'+str(eta_bin[j+1])

df2histo= OrderedDict()
bins=np.array(eta_bin)

def makeEtaGrid(indf,iterdf,prefix):
    for i in range(len(etagrid)):
        for j in range(len(etagrid[i])):
            prefix_tmp=prefix+"_etabin"+str(i)+"_etabin"+str(j)+"_mll"
            dftmp=iterdf.Filter(etagrid[i][j])
            indf[prefix_tmp]=dftmp.Histo1D( ( prefix_tmp , "%s ; mll [GeV] ; Events" %prefix_tmp , 30, 76.2, 106.2 ), "mll","weights")
    pass

if __name__ == '__main__':

    rf = ROOT.TFile.Open('hist_%s.root'%(dataset),"RECREATE")

    for idf in DF:

        # weight
        weight='1==1'
        if 'DY' in idf:
            if '2016' in idf:
                weight="ptllDYW*SFweight2l*XSWeight*METFilter_MC*LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*LepSF2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*35.92*GenLepMatch2l"
            elif '2017' in idf:
                weight="ptllDYW*SFweight2l*XSWeight*METFilter_MC*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*41.53*GenLepMatch2l"
            elif '2018' in idf:
                weight="ptllDYW*SFweight2l*XSWeight*METFilter_MC*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*LepSF2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*59.74*GenLepMatch2l"
        else:
            if '2016' in idf:
                weight="METFilter_DATA*LepCut2l__ele_cut_WP_Tight80X_SS__mu_cut_Tight80x*trigger"
            elif '2017' in idf:
                weight="METFilter_DATA*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*trigger"
            elif '2018' in idf:
                weight="METFilter_DATA*LepCut2l__ele_mvaFall17V1Iso_WP90_SS__mu_cut_Tight_HWWW*trigger"
        DYregion = DF[idf].Define('weights',weight).Define('abslep1eta','abs(lep1_eta)').Define('abslep2eta','abs(lep2_eta)')
    
        #SS/OS
        for ireg in signness:
            tmp_df_1 = DYregion.Filter( signness[ireg] , '%s selection' %ireg )
            for iptbin in ptbin:
                tmp_df_2 = tmp_df_1.Filter( ptbin[iptbin] , '%s selection' %iptbin )
                for ivar in variables:
                    if 'eta' in ivar:
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) , '%s_%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,iptbin,ivar,ivar) , 10 , -2.5 , 2.5 ) , ivar , 'weights' )
                    elif 'pt' in ivar:
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) , '%s_%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,iptbin,ivar,ivar) , 40 , 0. , 200. ) , ivar , 'weights' )
                #################################################################################################################
                    elif ivar=='mll':
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)]  = tmp_df_2.Histo1D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar), '%s_%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,iptbin,ivar,ivar) , 30, 76.2, 106.2 ) , ivar , 'weights' )
                        ## mll in different etabins
                        makeEtaGrid(df2histo,tmp_df_2,'%s_%s_%s'%(idf,iptbin,ireg))
                #################################################################################################################
                    elif ivar=='2d':
                        df2histo['%s_%s_%s_%s'%(idf,ireg,iptbin,ivar)] = tmp_df_2.Histo2D( ( '%s_%s_%s_%s'%(idf,ireg,iptbin,ivar) ,' %s_%s_%s_%s ; Lepton eta 1 ; Lepton eta 2 ; Events.' %(idf,ireg,iptbin,ivar), len(bins)-1 , np.asarray(bins,'d') , len(bins)-1 , np.asarray(bins,'d') ) , 'abslep1eta' , 'abslep2eta' , 'weights' )

    map(lambda x: df2histo[x].Write() , df2histo)
    rf.Close()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s minutes ---" % ( (time.time() - start_time)/60. ))
    print("--- %s hours ---" % ( (time.time() - start_time)/3600. ))
