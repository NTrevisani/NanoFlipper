from array import array
import math
from ROOT import gPad, TCanvas, TH2D, TH1D, TFile, THStack, TLegend, gSystem, TLatex, TH1, gStyle, TGaxis
import os, sys

import CMS_lumi
#import tdrstyle
#TGaxis.SetMaxDigits(2)
TH1.SetDefaultSumw2()
gStyle.SetPaintTextFormat(".5f")

def setBotStyle(h, r=4, fixRange=True):
    h.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize()*(r-1));
    h.GetXaxis().SetLabelOffset(h.GetXaxis().GetLabelOffset()*(r-1));
    h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize()*(r-1));
    h.GetYaxis().SetNdivisions(505);
    h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset()/(r-1));
    if fixRange:
        h.GetYaxis().SetRangeUser(0., 2.)
        for i in range(1, h.GetNbinsX()+1):
            if h.GetBinContent(i)<1.e-6:
                h.SetBinContent(i, -1.e-6)
pass

def drawCMS(lumi, text, onTop=False):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)
    if (type(lumi) is float or type(lumi) is int) and float(lumi) > 0: latex.DrawLatex(0.95, 0.985, "%.1f fb^{-1}  (13 TeV)" % (float(lumi)/1000.))
    elif type(lumi) is str: latex.DrawLatex(0.95, 0.985, "%s fb^{-1}  (13 TeV)" % lumi)
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    latex.SetTextSize(0.05 if len(text)>0 else 0.06)
    if not onTop: latex.DrawLatex(0.15, 0.87 if len(text)>0 else 0.84, "CMS")
    else: latex.DrawLatex(0.20, 0.99, "CMS")
    latex.SetTextSize(0.04)
    latex.SetTextFont(52)
    if not onTop: latex.DrawLatex(0.15, 0.83, text)
    else: latex.DrawLatex(0.40, 0.98, text)
pass

def setHistStyle(hist, r=1.1):
    hist.GetXaxis().SetTitleSize(hist.GetXaxis().GetTitleSize()*r*r)
    hist.GetYaxis().SetTitleSize(hist.GetYaxis().GetTitleSize()*r*r)
    hist.GetXaxis().SetLabelSize(hist.GetXaxis().GetLabelSize()*r)
    hist.GetYaxis().SetLabelSize(hist.GetYaxis().GetLabelSize()*r)
    hist.GetXaxis().SetLabelOffset(hist.GetXaxis().GetLabelOffset()*r*r*r*r)
    hist.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset()*r)
    hist.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset())
    if hist.GetXaxis().GetTitle().find("GeV") != -1: # and not hist.GetXaxis().IsVariableBinSize()
        div = (hist.GetXaxis().GetXmax() - hist.GetXaxis().GetXmin()) / hist.GetXaxis().GetNbins()
        hist.GetYaxis().SetTitle("Events / %.1f GeV" % div)
pass

def drawRatio(data, bkg):
    errData = array('d', [1.0])
    errBkg = array('d', [1.0])
    intData = data.IntegralAndError(1, data.GetNbinsX(), errData)
    intBkg = bkg.IntegralAndError(1, bkg.GetNbinsX(), errBkg)
    ratio = intData / intBkg if intBkg!=0 else 0.
    error = math.hypot(errData[0]*ratio/intData,  errBkg[0]*ratio/intBkg) if intData>0 and intBkg>0 else 0
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.08)
    #latex.DrawLatex(0.25, 0.85, "Data/Bkg = %.3f #pm %.3f" % (ratio, error))
    latex.DrawLatex(0.15, 0.85, "Data/Bkg = %.3f #pm %.3f" % (ratio, error))
    print "  Ratio:\t%.3f +- %.3f" % (ratio, error)
    return [ratio, error]
pass

def drawKolmogorov(data, bkg):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.08)
    #latex.DrawLatex(0.55, 0.85, "#chi^{2}/ndf = %.2f,   K-S = %.3f" % (data.Chi2Test(bkg, "CHI2/NDF"), data.KolmogorovTest(bkg)))
    latex.DrawLatex(0.45, 0.85, "#chi^{2}/ndf = %.2f,   K-S = %.3f" % (data.Chi2Test(bkg, "CHI2/NDF"), data.KolmogorovTest(bkg)))
pass

def drawRelativeYield(data,bkg):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.08)
    latex.DrawLatex(0.75, 0.85, "rel. Yield= %.3f" % ((data.Integral()/bkg.Integral())*100) )
pass

def setTopPad(TopPad, r=4):
    TopPad.SetPad("TopPad", "", 0., 1./r, 1.0, 1.0, 0, -1, 0)
    TopPad.SetTopMargin(0.24/r)
    TopPad.SetBottomMargin(0.04/r)
    TopPad.SetRightMargin(0.05)
    TopPad.SetTicks(1, 1)
pass

def setBotPad(BotPad, r=4):
    BotPad.SetPad("BotPad", "", 0., 0., 1.0, 1./r, 0, -1, 0)
    BotPad.SetTopMargin(r/100.)
    BotPad.SetBottomMargin(r/10.)
    BotPad.SetRightMargin(0.05)
    BotPad.SetTicks(1, 1)
pass

def addOverflow(hist, addUnder=True):
    n = hist.GetNbinsX()
    hist.SetBinContent(n, hist.GetBinContent(n) + hist.GetBinContent(n+1))
    hist.SetBinError(n, math.sqrt( hist.GetBinError(n)**2 + hist.GetBinError(n+1)**2 ) )
    hist.SetBinContent(n+1, 0.)
    hist.SetBinError(n+1, 0.)
    if addUnder:
        hist.SetBinContent(1, hist.GetBinContent(0) + hist.GetBinContent(1))
        hist.SetBinError(1, math.sqrt( hist.GetBinError(0)**2 + hist.GetBinError(1)**2 ) )
        hist.SetBinContent(0, 0.)
        hist.SetBinError(0, 0.)
pass

def SaveHisto2D(histin,tokens,data=False):
    proc = 'DY' if not data else 'DATA'
    histname=histin.GetName()
    cam = TCanvas( histname , histname ,2000, 2000);
    cam.SetTopMargin(0.1);
    cam.SetBottomMargin(0.15);
    cam.SetLeftMargin(0.215);
    cam.SetRightMargin(0.15);

    cam.cd().SetLogz();
    histin.Draw("colztextE");
    histin.SetTitle(histname)

    #needed to move the axis a bit
    z_begin = 0.875;
    palette = histin.GetListOfFunctions().FindObject("palette");
    palette.SetX1NDC(z_begin);
    palette.SetX2NDC(z_begin + 0.05);
    histin.GetZaxis().SetTitle('N_SS/N_OS')
    gPad.Modified();
    gPad.Update();

    cam.SaveAs( 'plots/%s/Ratio_%s_%s.png' %(tokens,tokens,proc) )
    cam.SaveAs( 'plots/%s/Ratio_%s_%s.pdf' %(tokens,tokens,proc) )
    #cam.SaveAs('plots/%s/Ratio_%s_DY.C' %(histname.split('_')[-1],histname))
    return
pass

def SaveHisto1D(HIST, region, ivar ,tree , tokens, snorm=1, ratio=0, poisson=True, logy=False):

    bkgsum='BkgSum_%s_%s' %(region,ivar)
    HIST[bkgsum] = HIST['DATA_%s_%s'%(region,ivar)].Clone("BkgSum") if 'DATA_%s_%s'%(region,ivar) in HIST else HIST['DY_%s_%s'%(region,ivar)].Clone("BkgSum")
    HIST[bkgsum].Reset("MICES")
    HIST[bkgsum].SetFillStyle(3003)
    HIST[bkgsum].SetFillColor(1)
    HIST[bkgsum].SetMarkerStyle(0)
    for key,val in HIST.iteritems():
        if 'BkgSum' in key: continue
        if 'DATA' in key: continue
        HIST[bkgsum].Add(val)
        
    #### STYLE
    HIST['DATA_%s_%s'%(region,ivar)].SetMarkerStyle(20)
    HIST['DATA_%s_%s'%(region,ivar)].SetMarkerSize(1.25)
    HIST['DATA_%s_%s'%(region,ivar)].SetFillColor(418)
    HIST['DATA_%s_%s'%(region,ivar)].SetFillStyle(1001)
    HIST['DATA_%s_%s'%(region,ivar)].SetLineColor(1)
    HIST['DATA_%s_%s'%(region,ivar)].SetLineStyle(1)
    HIST['DATA_%s_%s'%(region,ivar)].SetLineWidth(2)
    
    HIST['DY_%s_%s'%(region,ivar)].SetFillColor(418)
    HIST['DY_%s_%s'%(region,ivar)].SetFillStyle(1001)
    HIST['DY_%s_%s'%(region,ivar)].SetLineColor(418)
    HIST['DY_%s_%s'%(region,ivar)].SetLineStyle(1)
    HIST['DY_%s_%s'%(region,ivar)].SetLineWidth(2)

    HIST['FAKE_%s_%s'%(region,ivar)].SetFillColor(921)
    HIST['FAKE_%s_%s'%(region,ivar)].SetFillStyle(1001)
    HIST['FAKE_%s_%s'%(region,ivar)].SetLineColor(921)
    HIST['FAKE_%s_%s'%(region,ivar)].SetLineStyle(1)
    HIST['FAKE_%s_%s'%(region,ivar)].SetLineWidth(2)

    for i, s in enumerate(HIST):
        addOverflow(HIST[s], False) # Add overflow

    #Stack
    bkg = THStack('bkg', ";"+HIST[bkgsum].GetXaxis().GetTitle()+";"+HIST[bkgsum].GetYaxis().GetTitle())
    for proc in [ 'DY' , 'FAKE' ]:
        bkg.Add(HIST['%s_%s_%s'%(proc,region,ivar)]) # ADD ALL BKG

    #Legend
    n=len(HIST)
    leg = TLegend(0.7, 0.9-0.05*n, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetTextSize(0.03)
    leg.AddEntry(HIST['DATA_%s_%s'%(region,ivar)], 'Data', "pl")
    leg.AddEntry(HIST['DY_%s_%s'%(region,ivar)], 'DY', "f")
    leg.AddEntry(HIST['FAKE_%s_%s'%(region,ivar)], 'Fake', "f")
    c1 = TCanvas("c1", HIST.values()[-1].GetXaxis().GetTitle(), 800, 800 if ratio else 600 )

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
    HIST[bkgsum].Draw("SAME, E2") # sum of bkg
    HIST['DATA_%s_%s'%(region,ivar)].Draw("SAME, PE") # data

    bkg.GetYaxis().SetTitleOffset(bkg.GetYaxis().GetTitleOffset()*1) #1.075

    bkg.SetMaximum((6.0 if logy else 1.5)*max(bkg.GetMaximum(), HIST['DATA_%s_%s'%(region,ivar)].GetBinContent(HIST['DATA_%s_%s'%(region,ivar)].GetMaximumBin())+HIST['DATA_%s_%s'%(region,ivar)].GetBinError(HIST['DATA_%s_%s'%(region,ivar)].GetMaximumBin())))
    bkg.SetMinimum(max(min(HIST[bkgsum].GetBinContent(HIST[bkgsum].GetMinimumBin()), HIST['DATA_%s_%s'%(region,ivar)].GetMinimum()), 5.e-1)  if logy else 0.)

    #bkg.SetMinimum(1.0)

    leg.Draw()

    setHistStyle(bkg, 1.2 if ratio else 1.1)
    setHistStyle(HIST[bkgsum], 1.2 if ratio else 1.1)

    ##########################
    if ratio:
        c1.cd(2)
        err = HIST[bkgsum].Clone("BkgErr;")
        err.SetTitle("")
        err.GetYaxis().SetTitle("Data / Bkg")
        for i in range(1, err.GetNbinsX()+1):
            err.SetBinContent(i, 1)
            if HIST[bkgsum].GetBinContent(i) > 0:
                err.SetBinError(i, HIST[bkgsum].GetBinError(i)/HIST[bkgsum].GetBinContent(i))
        setBotStyle(err)
        errLine = err.Clone("errLine")
        errLine.SetLineWidth(1)
        errLine.SetFillStyle(0)
        errLine.SetLineColor(1)
        err.Draw("E2")
        errLine.Draw("SAME, HIST")

        if 'DATA_%s_%s'%(region,ivar) in HIST:
            res = HIST['DATA_%s_%s'%(region,ivar)].Clone("Residues")
            for i in range(0, res.GetNbinsX()+1):
                if HIST[bkgsum].GetBinContent(i) > 0:
                    res.SetBinContent(i, res.GetBinContent(i)/HIST[bkgsum].GetBinContent(i))
                    res.SetBinError(i, res.GetBinError(i)/HIST[bkgsum].GetBinContent(i))
            setBotStyle(res)
            res.Draw("SAME, PE0")
            if len(err.GetXaxis().GetBinLabel(1))==0: # Bin labels: not a ordinary plot
                drawRatio(HIST['DATA_%s_%s'%(region,ivar)], HIST[bkgsum])
                drawKolmogorov(HIST['DATA_%s_%s'%(region,ivar)], HIST[bkgsum])
                #drawRelativeYield(HIST['DATA_%s_%s'%(region,ivar)], HIST[bkgsum])
        else: res = None
    c1.cd(1)
    if '2016' in tokens:
        drawCMS("35.87", "Object Study")
    elif '2017' in tokens:
        drawCMS("41.53", "Object Study")
    elif '2018' in tokens:
        drawCMS("59.74", "Object Study")

    c1.Update()

    if not os.path.exists('plots/%s/Object_studies' %(tokens)): os.mkdir('plots/%s/Object_studies' %(tokens))
    c1.Print( 'plots/%s/Object_studies/%s_%s_%s.png' %(tokens,region,tokens,ivar) )
    c1.Print( 'plots/%s/Object_studies/%s_%s_%s.pdf' %(tokens,region,tokens,ivar) )
    return
pass

def SaveRatio( hSS , hOS , _token , _isample , _ivar ):
 
    #CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
    #CMS_lumi.writeExtraText = 1
    #CMS_lumi.extraText = "Preliminary"

    hratio = hSS.Clone('hratio_%s'%_ivar)
    hratio.Divide(hOS)
    c1 = TCanvas( 'hratio_%s'%_ivar , 'hratio_%s'%_ivar , 800 , 600 )
    if _ivar=='2d':
        TGaxis.SetMaxDigits(2)
        fout = TFile.Open( 'plots/%s/Object_studies/Ratio_%s_%s_%s.root' %(_token,_token,_isample,_ivar), 'RECREATE' )
        c1.SetRightMargin(0.2)
        hratio.SetAxisRange(0.00001,0.01,"Z")
        hratio.SetTitle('')
        hratio.GetZaxis().SetTitle('N_SS/N_OS (%s)' %_isample)
        hratio.GetXaxis().SetTitle('Lepton1 eta')
        hratio.GetYaxis().SetTitle('Lepton2 eta')
        hratio.Draw('colztextE')
        hratio.Write()
        fout.Close()
        #counter=0
        #for ixbin in range(1,hratio.GetNbinsX()+1):
        #    for iybin in range(1,hratio.GetNbinsY()+1):
        #        print('%s_Z[%s] = %s; %s_Z_err[%s] = %s;' %(_isample , counter , hratio.GetBinContent(ixbin,iybin) , _isample , counter , hratio.GetBinError(ixbin,iybin) ) )
        #        counter+=1
    else:
        #hratio.SetTitle('N_SS/N_OS ratio Dependence for %s'%_isample)
        hratio.SetTitle('')
        hratio.GetYaxis().SetTitle('N_SS/N_OS Ratio (%s)' %_isample)
        hratio.Draw('PE')

    c1.cd()
    if '2016' in _token: CMS_lumi.lumi_13TeV = "35.87 fb^{-1}"
    elif '2017' in _token: CMS_lumi.lumi_13TeV = "41.53 fb^{-1}"
    elif '2018' in _token: CMS_lumi.lumi_13TeV = "59.74 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = "Preliminary"
    CMS_lumi.CMS_lumi(c1, 4, 0)
    gPad.RedrawAxis()

        #c1.cd()
        #if '2016' in _token:
        #    drawCMS("35.87", "Object Study")
        #elif '2017' in _token:
        #    drawCMS("41.53", "Object Study")
        #elif '2018' in _token:
        #    drawCMS("59.74", "Object Study")

    
    c1.Print( 'plots/%s/Object_studies/Ratio_%s_%s_%s.png' %(_token,_token,_isample,_ivar) )
    c1.Print( 'plots/%s/Object_studies/Ratio_%s_%s_%s.pdf' %(_token,_token,_isample,_ivar) )
    TGaxis.SetMaxDigits(5)

pass
