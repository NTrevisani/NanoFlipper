import argparse
import sys, os

import ROOT
import numpy as np
from array import array
from math import sqrt

from mkHist import ptbin, eta_bin

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.SetDefaultSumw2()

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('-p','--plot', help='make mll distribution, default is false',action='store_true', default= False)
parser.add_argument('-f','--fit', help='fit to mll distribution, default is false',action='store_true', default= False)
parser.add_argument('-y','--year', help='chose all jobs in this year', choices=('2016','2017','2018'), default= '2017')
parser.add_argument('-r','--ratio', help='get ratio h_os divided by h_ss', action='store_true', default= False)

args = parser.parse_args()

zmass = '91.1876'

def fit(filename,ptbin,output):
    print('>>>>>>>>>>>>>>>>>>>> perform fit')
    year= filename.strip('.root').strip('hist_').split('_')[-1]
    eta_bin_array = array('f', eta_bin ) #[0.,1.0,1.5,2.5])
    fin=ROOT.TFile.Open(filename)
    histos=[]
    count={}
    count_err={}

    output+='/%s_mll' %ptbin
    if not os.path.exists(output): os.system('mkdir -p %s' %output )

    for tkey in fin.GetListOfKeys():
        key=tkey.GetName()
        if 'FAKE' in key: continue
        histos.append(key)
    for ihis in histos:
        if 'mll' not in ihis: continue
        if ptbin not in ihis: continue
        print('fit to: ',ihis)
        htmp=fin.Get(ihis)
        for ibin in range(0,60):
            if htmp.GetBinContent(ibin+1)<0:
                htmp.SetBinContent(ibin+1,0)
        # rebin
        #htmp.Rebin(2)
        nEvent=htmp.Integral()
        nHalf=0.8*nEvent
        w = ROOT.RooWorkspace("w")
        w.factory("BreitWigner:sig_bw(mll[76.2, 106.2], bwmean[91.1876,89,93],bwgamma[2.4952,2.4,2.6])")
        #w.factory("Landau:sig_lau(mll[76, 106], laumean[91.1876,89,93],lausigma[1,0.1,10])")
        w.factory("Gaussian:sig_gau(mll,gaumean[0,-100,100],gausigma[2.5,0.1,5])")
        #w.factory("CBShape:sig_cb(x, cbmean[0.,1.,10.], cbsigma[2.4952,2.4,2.6],cbalpha[20,0.,10],n[10,0.5,20])")
        w.factory("FCONV:bxc(mll,sig_bw,sig_gau)")
        w.factory("Exponential:bkg(mll,exalpha[-1.,-10,1])")
        # w.factory("SUM:model(sigfrac[0.5,0,1.]*bxc, bkgfrac[0.5,0,1.]*bkg)")
        w.factory("SUM:model(nsig["+str(nHalf)+",0,"+str(nEvent)+"]*bxc, nbkg["+str(nEvent-nHalf)+",0,"+str(nEvent)+"]*bkg)")
        mll=w.var('mll')
        pdf=w.pdf('model')
        dh=ROOT.RooDataHist('d'+ihis,'d'+ihis,ROOT.RooArgList(mll),htmp)
        getattr(w,'import')(dh)
        r = pdf.fitTo(dh, ROOT.RooFit.Save(True),ROOT.RooFit.Minimizer("Minuit2","Migrad"))
        #r = pdf.fitTo(dh, ROOT.RooFit.Save(True))
        #print('r.Print()       --------------------------------------------------------',w.var("nsig").getVal())
        #r.Print()
        c = ROOT.TCanvas()
        plot = mll.frame(ROOT.RooFit.Title(ihis))
        dh.plotOn(plot)
        pdf.plotOn(plot)
        pdf.plotOn(plot, ROOT.RooFit.Components("bkg"), ROOT.RooFit.LineStyle(2))
        pdf.plotOn(plot, ROOT.RooFit.Components("bxc"), ROOT.RooFit.LineColor(2), ROOT.RooFit.LineStyle(2))
        pdf.paramOn(plot,ROOT.RooFit.Layout(0.57,0.97,0.85))
        plot.Draw()
        c.GetPrimitive("model_paramBox").SetFillStyle(0)
        c.GetPrimitive("model_paramBox").SetBorderSize(0)
        '''
        c.GetPrimitive("model_paramBox").SetTextFont(102)
        tbox_title_old=['bwgamma','bwmean','exalpha','gaumean','gausigma','nbkg','nsig']
        tbox_title_old=['bwgamma','bwmean','exalpha','gaumean','gausigma','nbkg','nsig']
        tbox_title_new=['#Gamma_{BW}','mean_{BW}','#alpha_{Exp}','mean_{Gau}','#sigma_{Gau}','n_{Bkg}','n_{Sig}']
        for i in range(0,7):
            _str=c.GetPrimitive("model_paramBox").GetLine(i).GetTitle()
            _str=_str.replace(tbox_title_old[i],tbox_title_new[i])
            c.GetPrimitive("model_paramBox").GetLine(i).SetTitle(_str)
        '''
        c.SaveAs(output+'/c_'+ihis+'.png')
        mc = ROOT.RooStats.ModelConfig("ModelConfig_"+ihis,w)
        mc.SetPdf(pdf)
        mc.SetParametersOfInterest(ROOT.RooArgSet(w.var("nsig")))
        mc.SetSnapshot(ROOT.RooArgSet(w.var("nsig")))
        mc.SetObservables(ROOT.RooArgSet(w.var("mll")))
        #w.defineSet("nuisParams","nbkg,laumean,lausigma,gaumean,gausigma,exalpha")
        w.defineSet("nuisParams","nbkg,bwmean,bwgamma,gaumean,gausigma,exalpha")
        nuis = getattr(w,'set')("nuisParams")
        mc.SetNuisanceParameters(nuis)
        getattr(w,'import')(mc)
        w.writeToFile(output+'/'+ihis+"_config.root",True)
        count[ihis]=w.var("nsig").getVal()
        count_err[ihis]=w.var("nsig").getError()
    #print(count)
    #print(count_err)
    fout=ROOT.TFile(output+'/count_'+ptbin+'_'+filename,'recreate')
    h_ss_sub=ROOT.TH2D()
    h_os_sub=ROOT.TH2D()
    #samples=['DPS','WW_strong','FAKE','VVV','VZ','Vg','WW_EWK','TTV','DATA','DY']
    samples=['DATA','DY']
    ss_plots=[]
    os_plots=[]

    #print count.keys()
    for isample in samples:
        h_ss=ROOT.TH2D('h_'+ptbin+'_ss_'+isample,'h_'+ptbin+'_ss_'+isample, len(eta_bin)-1 , eta_bin_array , len(eta_bin)-1 , eta_bin_array )
        h_os=ROOT.TH2D('h_'+ptbin+'_os_'+isample,'h_'+ptbin+'_os_'+isample, len(eta_bin)-1 , eta_bin_array , len(eta_bin)-1 , eta_bin_array )
        for i in range(0,len(eta_bin)-1):
            for j in range(0,len(eta_bin)-1):
                h_ss.SetBinContent(i+1,j+1,count['analysis_'+isample+'_'+year+'_'+ptbin+"_ss_etabin"+str(i)+"_etabin"+str(j)+"_mll"])
                h_ss.SetBinError(i+1,j+1,count_err['analysis_'+isample+'_'+year+'_'+ptbin+"_ss_etabin"+str(i)+"_etabin"+str(j)+"_mll"])
                h_os.SetBinContent(i+1,j+1,count['analysis_'+isample+'_'+year+'_'+ptbin+"_os_etabin"+str(i)+"_etabin"+str(j)+"_mll"])
                h_os.SetBinError(i+1,j+1,count_err['analysis_'+isample+'_'+year+'_'+ptbin+"_os_etabin"+str(i)+"_etabin"+str(j)+"_mll"])
        if isample=='DATA':
            h_ss_sub=h_ss.Clone()
            h_ss_sub.SetName('h_'+ptbin+'_ss_DATASUB')
            h_ss_sub.SetTitle('h_'+ptbin+'_ss_DATASUB')
            h_os_sub=h_os.Clone()
            h_os_sub.SetName('h_'+ptbin+'_os_DATASUB')
            h_os_sub.SetTitle('h_'+ptbin+'_os_DATASUB')

        ss_plots.append(h_ss)
        os_plots.append(h_os)
    ##???
    for i in range(0,len(ss_plots)):
        if ss_plots[i].GetName() != 'h_'+ptbin+'_ss_DATA' and ss_plots[i].GetName() != 'h_'+ptbin+'_ss_DY' and ss_plots[i].GetName() != 'h_'+ptbin+'_ss_FAKE':
            print "ss_plots[i] : ", ss_plots[i]
            h_ss_sub.Add(ss_plots[i],-1)
    for i in range(0,len(os_plots)):
        if os_plots[i].GetName() != 'h_'+ptbin+'_os_DATA' and os_plots[i].GetName() != 'h_'+ptbin+'_os_DY' and ss_plots[i].GetName() != 'h_'+ptbin+'_os_FAKE':
            h_os_sub.Add(os_plots[i],-1)
    ss_plots.append(h_ss_sub)
    os_plots.append(h_os_sub)

    map(lambda x: x.Write() , ss_plots+os_plots)

    #for i in range(0,len(ss_plots)):
    #    ss_plots[i].Write()
    #    os_plots[i].Write()
    fout.Close()

    #print(count)
    pass

def ratio(filename,data,ptbin,output):
    ## ratio DATA
    year= filename.strip('.root').strip('hist_').split('_')[-1]
    fin=ROOT.TFile.Open(filename)
    h_ss=fin.Get('h_%s_ss_%s' %(ptbin,data)) # DATASUB
    h_os=fin.Get('h_%s_os_%s' %(ptbin,data))
    h_ratio=h_ss.Clone()
    h_ratio.Divide(h_os)
    # gotten ride of low stats figure, unreliable
    for i in range(0,h_ratio.GetNbinsX()):
        for j in range(0,h_ratio.GetNbinsY()):
            if h_ss.GetBinContent(i+1,j+1)<10:
                h_ratio.SetBinContent(i+1,j+1,0)
                h_ratio.SetBinError(i+1,j+1,0)
    h_ratio.SetName('h2_%s' %data)
    h_ratio.SetTitle('N_{SS}/N_{OS}')

    output+='/%s_mll' %ptbin
    if not os.path.exists(output): os.system('mkdir -p %s' %output )
    fout=ROOT.TFile( '%s/ratio_%s_%s_%s_mll.root' %(output,data,year,ptbin),'recreate')
    h_ratio.Write()
    fout.Write()
    fout.Close()

    c=ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    #ROOT.gStyle.SetPaintTextFormat("1.6f")
    #ROOT.gStyle.SetPaintTextFormat("4.1f") # HERE
    h_ss.Draw("colz texte")

    c.SaveAs( '%s/h_ss_%s_%s_%s_mll.png' %(output,data,year,ptbin))
    c.Clear()
    h_os.Draw("colz texte")
    c.SaveAs( '%s/h_os_%s_%s_%s_mll.png' %(output,data,year,ptbin))
    c.Clear()
    h_ratio.Draw("colz texte")
    c.SaveAs( '%s/h_ratio_%s_%s_%s_mll.png'%(output,data,year,ptbin))
    pass

if __name__ == '__main__':
    for ifile in os.listdir('.'):
        if ifile.split('_')[0] != 'hist': continue
        name= ifile.strip('.root').strip('hist_')
        #makdir directory
        if not os.path.exists('plots/%s/Zmassfit' %name): os.system('mkdir -p plots/%s/Zmassfit' %name)
        if not os.path.exists('plots/%s/Chflipfit' %name): os.system('mkdir -p plots/%s/Chflipfit' %name)

        #for iptbin in ptbin:
        #fit zmass
        for iptbin in ptbin:
            #iptbin="lowpt2"
            fit( ifile , iptbin , 'plots/%s/Zmassfit' %name )
            #compute ratio
            for idata in ['DATASUB','DY']:
                ratio( "plots/%s/Zmassfit/%s_mll/count_%s_hist_%s.root" %(name,iptbin,iptbin,name) , idata , iptbin , 'plots/%s/Chflipfit' %name )
