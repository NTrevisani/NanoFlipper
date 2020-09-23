from ROOT import TH2D, TCanvas, gStyle
import ROOT
import csv, sys, os
from collections import OrderedDict
from array import array as arr

from mkHist import ptbin, eta_bin, mkplot
from utils.helper import *

ROOT.gInterpreter.Declare(
'''
static std::map<const std::string,TH2D*> SFmap;

void loadSF2D( const char *filename )
{
    TFile f = TFile( filename , "READ" );

    //Declare histogram
    TH2D *h_mc       = (TH2D*) f.Get("mc")->Clone();
    TH2D *h_mc_sys   = (TH2D*) f.Get("mc_sys")->Clone();
    TH2D *h_data     = (TH2D*) f.Get("data")->Clone();
    TH2D *h_data_sys = (TH2D*) f.Get("data_sys")->Clone();
    TH2D *h_sf       = (TH2D*) f.Get("sf")->Clone();
    TH2D *h_sf_sys   = (TH2D*) f.Get("sf_sys")->Clone();

    h_mc->SetDirectory(0); h_mc_sys->SetDirectory(0);
    h_data->SetDirectory(0); h_data_sys->SetDirectory(0);
    h_sf->SetDirectory(0); h_sf_sys->SetDirectory(0);

    SFmap.insert(std::make_pair( "mc"       , h_mc       ));
    SFmap.insert(std::make_pair( "mc_sys"   , h_mc_sys   ));
    SFmap.insert(std::make_pair( "data"     , h_data     ));
    SFmap.insert(std::make_pair( "data_sys" , h_data_sys ));
    SFmap.insert(std::make_pair( "sf"       , h_sf       ));
    SFmap.insert(std::make_pair( "sf_sys"   , h_sf_sys   ));

    std::cout<<"loaded 2D map : "<<filename<<std::endl;
    //std::cout<<"Load::Accessing : "<< SFmap["sf"]->GetNbinsX() <<std::endl;

    f.Close();
}

double getFlip( const double pt1_in , const double eta1_in , const double pt2_in , const double eta2_in , const int pdgId1 , const int pdgId2 , bool useData_ )
{
    //std::cout<<"Eval::Accessing : "<< SFmap["sf"]->GetNbinsX() <<std::endl;

    double flip1 =0.; double flip1_sys=0.; double flip2=0.; double flip2_sys=0.; double commonW=1.;
    const std::string SFmapKey = (useData_) ? "data" : "mc";

    flip1     = SFmap[SFmapKey]->GetBinContent( SFmap[SFmapKey]->FindBin( abs(eta1_in) , pt1_in ));
    flip1_sys = SFmap[ SFmapKey+"_sys" ]->GetBinContent( SFmap[ SFmapKey+"_sys" ]->FindBin( abs(eta1_in) , pt1_in) );

    flip2     = SFmap[SFmapKey]->GetBinContent( SFmap[SFmapKey]->FindBin( abs(eta2_in) , pt2_in ));
    flip2_sys = SFmap[ SFmapKey+"_sys" ]->GetBinContent( SFmap[ SFmapKey+"_sys" ]->FindBin( abs(eta2_in) , pt2_in ));

    // opposite sign , either one is flip
    if ( pdgId1*pdgId2 == -11*11){
        commonW = flip1 * ( 1. - flip2 ) + flip2 * ( 1. - flip1 );
    }
    // both are flip
    else if ( pdgId1*pdgId2 == -11*13 ){
        commonW = flip1 + flip2;
    }
    // the same sign region, get the SF
    //else if ( pdgId1*pdgId2 == 11*11 || pdgId1*pdgId2 == 11*13 ){
    //}

    return commonW;
}

double getSF( const double pt1_in , const double eta1_in , const double pt2_in , const double eta2_in , const int pdgId1 , const int pdgId2 )
{
    double sf1=1.; double sf2=1.; double SF=1.;
    if ( pdgId1*pdgId2 == 11*11 || pdgId1*pdgId2 == 11*13 ){
        sf1 = SFmap["sf"]->GetBinContent( SFmap["sf"]->FindBin( abs(eta1_in) , pt1_in ) );
        sf2 = SFmap["sf"]->GetBinContent( SFmap["sf"]->FindBin( abs(eta2_in) , pt2_in ) );
    }
    SF = sf1*sf2;

    return SF;
}

'''
)

def drawChi2(data, bkg):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.03)
    latex.DrawLatex( 0.6361032 , 0.8428875 , "#chi^{2}/ndf = %.2f,   K-S = %.3f" % (data.Chi2Test(bkg, "CHI2/NDF"), data.KolmogorovTest(bkg , 'N')))
    print  "#chi^{2}/ndf = %.2f,   K-S = %.3f" % (data.Chi2Test(bkg, "CHI2/NDF"), data.KolmogorovTest(bkg , 'N' ))
pass

def drawMean( hist_ , name_ , xpos , ypos ):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.03)
    latex.DrawLatex( xpos , ypos , "%s mean: %.2f GeV" % ( name_ , hist_.GetMean() ) )
pass


def mkval_postfit( dataset_ , rdflist , ptbin_ , output_ , test=1 ):

    #rdf_CR_OS = rdflist[0]
    #rdf_CR_SS = rdflist[1]

    #gStyle.SetOptStat(0);

    # looking at mll variable
    h_os_keys = filter(lambda x : 'etabin' not in x and 'FAKE' not in x and ptbin_ in x and 'os' in x , rdflist )
    h_ss_keys = filter(lambda x : 'etabin' not in x and 'FAKE' not in x and ptbin_ in x and 'ss' in x , rdflist )

    # list
    k_N_os_mc   = filter(lambda x : 'DY' in x   , h_os_keys )[0]
    k_N_os_data = filter(lambda x : 'DATA' in x , h_os_keys )[0]

    k_N_ss_mc   = filter(lambda x : 'DY' in x   , h_ss_keys )[0]
    k_N_ss_data = filter(lambda x : 'DATA' in x , h_ss_keys )[0]

    c = TCanvas();
    hlist_L=OrderedDict() ; hlist_R=OrderedDict()
    # f_mc x N_os_mc == N_ss_mc
    if test == 1 :
        print "Test 1 : f_mc x N_os_mc != N_ss_mc"

        # f_mc x N_os_mc
        df_N_os_mc = rdflist[k_N_os_mc].Define( 'f_mc' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , lep1_pdgId , lep2_pdgId , 0 )' ).Define( 'totalW' , 'f_mc*weights' )
        hlist_L['h_N_os_mc_mll']      = df_N_os_mc.Histo1D( ( 'N_os_mc_mll'      , 'f_mc x N_os_mc != N_ss_mc %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_L['h_N_os_mc_lep1_eta'] = df_N_os_mc.Histo1D( ( 'N_os_mc_lep1_eta' , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_L['h_N_os_mc_lep2_eta'] = df_N_os_mc.Histo1D( ( 'N_os_mc_lep2_eta' , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_L['h_N_os_mc_lep1_pt']  = df_N_os_mc.Histo1D( ( 'N_os_mc_lep1_pt'  , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_L['h_N_os_mc_lep2_pt']  = df_N_os_mc.Histo1D( ( 'N_os_mc_lep2_pt'  , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )
        # N_ss_mc
        df_N_ss_mc = rdflist[k_N_ss_mc].Define( 'totalW' , 'weights')
        hlist_R['h_N_ss_mc_mll']      = df_N_ss_mc.Histo1D( ( 'N_ss_mc_mll'      , 'f_mc x N_os_mc != N_ss_mc %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_R['h_N_ss_mc_lep1_eta'] = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep1_eta' , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_R['h_N_ss_mc_lep2_eta'] = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep2_eta' , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_R['h_N_ss_mc_lep1_pt']  = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep1_pt'  , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_R['h_N_ss_mc_lep2_pt']  = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep2_pt'  , 'f_mc x N_os_mc != N_ss_mc %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )

        for ihist in hlist_L: hlist_L[ihist].SetLineColor(ROOT.kGreen)
        for ihist in hlist_R: hlist_R[ihist].SetLineColor(ROOT.kRed)

        for hist_l , hist_r in zip( hlist_L , hlist_R ):
            var = hist_l.split('_')[-2]+"_"+hist_l.split('_')[-1] if 'lep' in hist_l else  hist_l.split('_')[-1]
            #if var=='mll': gStyle.SetOptStat(1111111);

            c.cd();
            if 'pt' in hist_l: c.SetLogy()
            hlist_R[hist_r].Draw() ; hlist_L[hist_l].Draw("SAMES")
            drawChi2( hlist_R[hist_r].GetPtr() , hlist_L[hist_l].GetPtr() )
            if 'mll' in hist_l:
                drawMean( hlist_L[hist_l] , 'f_{mc} * N_os' , 0.6346705 , 0.7537155 )
                drawMean( hlist_R[hist_r] , 'N_ss' , 0.6776504 , 0.7133758 )
            c.Update()
            c.Print( '%s/test_1_%s.png' %( output_ , var ) )

            #gStyle.SetOptStat(0);
    elif test == 2 :
        print "Test 2 : SF x N_ss_mc != N_ss_data"

        # SF x N_ss_mc
        df_N_ss_mc = rdflist[k_N_ss_mc].Define( 'SF' , 'getSF( lep1_pt , lep1_eta , lep2_pt , lep2_eta , lep1_pdgId , lep2_pdgId )' ).Define( 'totalW' , 'SF*weights' )
        hlist_L['h_N_ss_mc_mll']      = df_N_ss_mc.Histo1D( ( 'N_ss_mc_mll'      , 'SF x N_ss_mc != N_ss_data %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_L['h_N_ss_mc_lep1_eta'] = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep1_eta' , 'SF x N_ss_mc != N_ss_data %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_L['h_N_ss_mc_lep2_eta'] = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep2_eta' , 'SF x N_ss_mc != N_ss_data %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_L['h_N_ss_mc_lep1_pt']  = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep1_pt'  , 'SF x N_ss_mc != N_ss_data %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_L['h_N_ss_mc_lep2_pt']  = df_N_ss_mc.Histo1D( ( 'N_ss_mc_lep2_pt'  , 'SF x N_ss_mc != N_ss_data %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )
        # N_ss_data
        df_N_ss_data = rdflist[k_N_ss_data].Define( 'totalW' , 'weights')
        hlist_R['h_N_ss_data_mll']      = df_N_ss_data.Histo1D( ( 'N_ss_data_mll'      , 'SF x N_ss_mc != N_ss_data %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_R['h_N_ss_data_lep1_eta'] = df_N_ss_data.Histo1D( ( 'N_ss_data_lep1_eta' , 'SF x N_ss_mc != N_ss_data %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_R['h_N_ss_data_lep2_eta'] = df_N_ss_data.Histo1D( ( 'N_ss_data_lep2_eta' , 'SF x N_ss_mc != N_ss_data %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_R['h_N_ss_data_lep1_pt']  = df_N_ss_data.Histo1D( ( 'N_ss_data_lep1_pt'  , 'SF x N_ss_mc != N_ss_data %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_R['h_N_ss_data_lep2_pt']  = df_N_ss_data.Histo1D( ( 'N_ss_data_lep2_pt'  , 'SF x N_ss_mc != N_ss_data %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )

        #plot 1D STACK kinematics between DATA/MC
        for hist_l , hist_r in zip( hlist_L , hlist_R ):
            insitu=OrderedDict()
            insitu[ 'DY_Test2_%s'% hist_l.replace('_mc_','_') ] = hlist_L[hist_l].GetPtr()
            insitu[ 'DATA_Test2_%s'% hist_r.replace('_data_','_') ] = hlist_R[hist_r].GetPtr()
            SaveHisto1D( insitu , 'Test2_%s' % hist_l.replace('_mc_','_') , output_ , 0, 4, False , True if 'pt' in hist_l else False , True ) #isvalidation
        ###

    elif test == 3 :
        print "Test 3 : f_data x N_os_mc != N_ss_data"

        # f_data x N_os_mc
        df_N_os_mc = rdflist[k_N_os_mc].Define( 'f_data' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , lep1_pdgId , lep2_pdgId , 1 )' ).Define( 'totalW' , 'f_data*weights' )
        hlist_L['h_N_os_mc_mll']      = df_N_os_mc.Histo1D( ( 'N_os_mc_mll'      , 'f_data x N_os_mc != N_ss_data %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_L['h_N_os_mc_lep1_eta'] = df_N_os_mc.Histo1D( ( 'N_os_mc_lep1_eta' , 'f_data x N_os_mc != N_ss_data %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_L['h_N_os_mc_lep2_eta'] = df_N_os_mc.Histo1D( ( 'N_os_mc_lep2_eta' , 'f_data x N_os_mc != N_ss_data %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_L['h_N_os_mc_lep1_pt']  = df_N_os_mc.Histo1D( ( 'N_os_mc_lep1_pt'  , 'f_data x N_os_mc != N_ss_data %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_L['h_N_os_mc_lep2_pt']  = df_N_os_mc.Histo1D( ( 'N_os_mc_lep2_pt'  , 'f_data x N_os_mc != N_ss_data %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )
        # N_ss_data
        df_N_ss_data = rdflist[k_N_ss_data].Define( 'totalW' , 'weights')
        hlist_R['h_N_ss_data_mll']      = df_N_ss_data.Histo1D( ( 'N_ss_data_mll'      , 'f_data x N_os_mc != N_ss_data %s %s ; mll [GeV]     ; Events' %( dataset_ , ptbin_ ) , 30, 76.2, 106.2 ) , 'mll'      , 'totalW' )
        hlist_R['h_N_ss_data_lep1_eta'] = df_N_ss_data.Histo1D( ( 'N_ss_data_lep1_eta' , 'f_data x N_os_mc != N_ss_data %s %s ; lep1_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep1_eta' , 'totalW' )
        hlist_R['h_N_ss_data_lep2_eta'] = df_N_ss_data.Histo1D( ( 'N_ss_data_lep2_eta' , 'f_data x N_os_mc != N_ss_data %s %s ; lep2_eta      ; Events' %( dataset_ , ptbin_ ) , 50 , -2.5 , 2.5 ) , 'lep2_eta' , 'totalW' )
        hlist_R['h_N_ss_data_lep1_pt']  = df_N_ss_data.Histo1D( ( 'N_ss_data_lep1_pt'  , 'f_data x N_os_mc != N_ss_data %s %s ; lep1_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , 'totalW' )
        hlist_R['h_N_ss_data_lep2_pt']  = df_N_ss_data.Histo1D( ( 'N_ss_data_lep2_pt'  , 'f_data x N_os_mc != N_ss_data %s %s ; lep2_pt [GeV] ; Events' %( dataset_ , ptbin_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , 'totalW' )

        for ihist in hlist_L: hlist_L[ihist].SetLineColor(ROOT.kGreen)
        for ihist in hlist_R: hlist_R[ihist].SetLineColor(ROOT.kRed)

        #for hist_l , hist_r in zip( hlist_L , hlist_R ):
        #    var = hist_l.split('_')[-2]+"_"+hist_l.split('_')[-1] if 'lep' in hist_l else  hist_l.split('_')[-1]
        #    print var
        #    c.cd();
        #    if 'pt' in hist_l: c.SetLogy()
        #    hlist_R[hist_r].Draw() ; hlist_L[hist_l].Draw("SAME")
        #    drawChi2( hlist_R[hist_r].GetPtr() , hlist_L[hist_l].GetPtr() )
        #    c.Update()
        #    c.Print( '%s/test_3_%s.png' %( output_ , var ) )

        #plot 1D STACK kinematics between DATA/MC
        for hist_l , hist_r in zip( hlist_L , hlist_R ):
            insitu=OrderedDict()
            tag='Test3_'+hist_l.split('_')[-2]+"_"+hist_l.split('_')[-1]
            insitu[ 'DY_%s' %tag  ] = hlist_L[hist_l].GetPtr()
            insitu[ 'DATA_%s' %tag  ] = hlist_R[hist_r].GetPtr()
            SaveHisto1D( insitu , tag , output_ , 0, 4, False , True if 'pt' in hist_l else False , True ) #isvalidation

    elif test == 4 :
        print "Test 4 : perform computation on R(MC)"
        df_N_ss_mc = rdflist[k_N_ss_mc].Sum("weights").GetValue();
        df_N_os_mc = rdflist[k_N_os_mc].Sum("weights").GetValue();
        print "(%s) frac R_mc : %.4f , impacting 1 - R_mc : %.4f" %( dataset_ , df_N_ss_mc/( df_N_ss_mc + df_N_os_mc) , 1 - ( df_N_ss_mc/( df_N_ss_mc + df_N_os_mc) ) )
    else:
        print "ERROR"
        sys.exit()
    pass

if __name__ == '__main__':

    ptbin = 'lowpt2'

    for ifile in os.listdir('.'):
        #if '2018' not in ifile: continue
        print ifile
        if ifile.split('_')[0] != 'hist': continue
        dataset= ifile.strip('.root').strip('hist_')
        output="plots/%s/post-diagnostics" %dataset
        if not os.path.exists(output): os.system('mkdir -p %s' %output)

        # initialize 2D
        if not os.path.exists("data/chargeFlip_%s_SF.root" %dataset):
            print "ERROR, file does not exist"
            sys.exit()

        ROOT.loadSF2D( "data/chargeFlip_%s_SF.root" %dataset )

        # point to ntuple
        ntupleDIR='%s/../ntuple/results/%s' %( os.getcwd() , dataset )
        DF_val= OrderedDict({
            'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", ntupleDIR+'/DYJetsToLL_M*.root' ),
            'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/SingleElectron.root' , ntupleDIR+'/DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/EGamma.root' ] ),
            #'FAKE_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_SingleElectron.root' , ntupleDIR+'/Fake_DoubleEG.root' ] if dataset != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
        })

        #DF_val = OrderedDict({
        #    'DY_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", '%s/../ntuple/results/%s/DYJetsToLL_M*.root' %( os.getcwd() , dataset ) ),
        #    'DATA_%s' %(dataset.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ '%s/../ntuple/results/%s/DoubleEG.root' %( os.getcwd() , dataset ) ]\
        #    if dataset != "nanov5_2018" else [ '%s/../ntuple/results/%s/EGamma.root' %( os.getcwd() , dataset ) ] ),
        #    #'FAKE_%s' %(dataset_.split('_')[-1]) : ROOT.ROOT.RDataFrame("flipper", [ ntupleDIR+'/Fake_DoubleEG.root' ] if dataset_ != "nanov5_2018" else [ ntupleDIR+'/Fake_EGamma.root' ] )
        #})

        # test 1 ; 2 ; 3 ; 4
        CR_OS = mkplot( dataset , ptbin , True , DF_val , 1 )
        CR_SS = mkplot( dataset , ptbin , True , DF_val , 0 )
        for i in range(4):
            i+=1
            #if i!=1: continue
            mkval_postfit( dataset , CR_OS , ptbin , output , i )
    pass
