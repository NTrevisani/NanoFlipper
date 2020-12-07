import ROOT
from ROOT import gROOT, gStyle
import os, sys
from collections import OrderedDict

ROOT.ROOT.EnableImplicitMT(12)
ROOT.TH1.SetDefaultSumw2()
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat(".5f")

from mkHist import *
from utils.helper import *
from utils.mkroot import *

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

double getFlip( const double pt1_in , const double eta1_in , const double pt2_in , const double eta2_in , bool useData_ )
{
    //std::cout<<"Eval::Accessing : "<< SFmap["sf"]->GetNbinsX() <<std::endl;

    double flip1 =0.; double flip1_sys=0.; double flip2=0.; double flip2_sys=0.; double commonW=1.;
    const std::string SFmapKey = (useData_) ? "data" : "mc";

    flip1     = SFmap[SFmapKey]->GetBinContent( SFmap[SFmapKey]->FindBin( abs(eta1_in) , pt1_in ));
    flip1_sys = SFmap[ SFmapKey+"_sys" ]->GetBinContent( SFmap[ SFmapKey+"_sys" ]->FindBin( abs(eta1_in) , pt1_in) );

    flip2     = SFmap[SFmapKey]->GetBinContent( SFmap[SFmapKey]->FindBin( abs(eta2_in) , pt2_in ));
    flip2_sys = SFmap[ SFmapKey+"_sys" ]->GetBinContent( SFmap[ SFmapKey+"_sys" ]->FindBin( abs(eta2_in) , pt2_in ));

    commonW = flip1 * ( 1. - flip2 ) + flip2 * ( 1. - flip1 );

    return commonW;
}

double getSF( const double pt1_in , const double eta1_in , const double pt2_in , const double eta2_in , const int pdgId1 , const int pdgId2 )
{
    double sf1=1.; double sf2=1.; double SF=1.;
    //if ( pdgId1*pdgId2 == 11*11 || pdgId1*pdgId2 == 11*13 ){
    sf1 = SFmap["sf"]->GetBinContent( SFmap["sf"]->FindBin( abs(eta1_in) , pt1_in ) );
    sf2 = SFmap["sf"]->GetBinContent( SFmap["sf"]->FindBin( abs(eta2_in) , pt2_in ) );
    //}
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

def drawLegend( hist_left , name_left , hist_right , name_right ):
    legend = ROOT.TLegend(0.6618911,0.5711253,0.8911175,0.6666667);
    legend.SetBorderSize(0)
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(1001)
    legend.AddEntry( hist_left , name_left, "l" )
    legend.AddEntry( hist_right , name_right, "l" )
    return legend
pass

def presel(dataset):

    presel="nLepton==2"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL DZ v*
    if dataset == "nanov5_2016" :
        presel+=" && lep1_pt>28 && lep2_pt>15"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*
    elif dataset == "nanov5_2017" :
        presel+=" && lep1_pt>35 && lep2_pt>15"
    # HLT Ele23 Ele12 CaloIdL TrackIdL IsoVL v*
    elif dataset == "nanov5_2018" :
        presel+=" && lep1_pt>35 && lep2_pt>15"
    return presel
pass

def PrepareDF( DF , presel , wp_ ):

    dfval = OrderedDict()

    for idf in DF :
        DYregion = addWeights( DF , idf , wp_ )
        DYregion = DYregion.Filter( presel , presel )
        for ireg in signness:
            dfval['%s_%s'%(idf,ireg)] = DYregion.Filter( signness[ireg] , '%s selection' %ireg )
    return dfval
pass

def PrepareVariable( df_in , name , dataset_ , testname_ , weight_ ):
    h = OrderedDict()
    h[ name + '_mll' ]     = df_in.Histo1D( ( name + '_mll'      , '%s %s ; mll [GeV]     ; Events' %( testname_ , dataset_ ) , 30, 76.2, 106.2 ) , 'mll'      , weight_ )
    h[ name + '_lep1_eta'] = df_in.Histo1D( ( name + '_lep1_eta' , '%s %s ; lep1_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep1_eta' , weight_ )
    h[ name + '_lep2_eta'] = df_in.Histo1D( ( name + '_lep2_eta' , '%s %s ; lep2_eta      ; Events' %( testname_ , dataset_ ) , 10 , -2.5 , 2.5 ) , 'lep2_eta' , weight_ )
    h[ name + '_lep1_pt']  = df_in.Histo1D( ( name + '_lep1_pt'  , '%s %s ; lep1_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep1_pt'  , weight_ )
    h[ name + '_lep2_pt']  = df_in.Histo1D( ( name + '_lep2_pt'  , '%s %s ; lep2_pt [GeV] ; Events' %( testname_ , dataset_ ) , 40 , 0. , 200.  ) , 'lep2_pt'  , weight_ )
    return h
pass

# VALIDATION 1
def mkVal1( df_dicts , dataset_ , output_ ):
    testName="f_mc x N_os_mc != N_ss_mc"

    k_N_os_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DY'   in x , df_dicts ) ]
    k_N_os_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DATA' in x , df_dicts ) ]
    k_N_ss_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DY'   in x , df_dicts ) ]
    k_N_ss_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DATA' in x , df_dicts ) ]
    
    # check key
    if len(k_N_os_mc)   !=1 : sys.exit()
    if len(k_N_os_data) !=1 : sys.exit()
    if len(k_N_ss_mc)   !=1 : sys.exit()
    if len(k_N_ss_data) !=1 : sys.exit()
    
    print testName
    # f_mc x N_os_mc
    df_N_os_mc = k_N_os_mc[0][1].Define( 'f_mc' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , 0 )' ).Define( 'totalW' , 'f_mc*weights' )
    dict_N_os_mc_var = PrepareVariable( df_N_os_mc , k_N_os_mc[0][0] , dataset_ , testName , 'totalW' )
    # N_ss_mc
    df_N_ss_mc = k_N_ss_mc[0][1].Define( 'totalW' , 'weights')
    dict_N_ss_mc_var = PrepareVariable( df_N_ss_mc , k_N_ss_mc[0][0] , dataset_ , testName , 'totalW' )

    # cosmetic
    for ihist in dict_N_os_mc_var: 
        #print ihist
        dict_N_os_mc_var[ihist].SetLineColor(ROOT.kGreen)
    for ihist in dict_N_ss_mc_var: 
        #print ihist
        dict_N_ss_mc_var[ihist].SetLineColor(ROOT.kRed)
    
    c = ROOT.TCanvas()
    
    for hos , hss in zip( dict_N_os_mc_var , dict_N_ss_mc_var ):
        c.cd();
        var = hos.split('_')[-2]+"_"+hos.split('_')[-1] if 'lep' in hos else  hos.split('_')[-1]
        if 'pt' in hos and 'pt' in hss: c.SetLogy()
        dict_N_os_mc_var[hos].Draw()
        dict_N_ss_mc_var[hss].Draw("SAMES")
        drawChi2( dict_N_ss_mc_var[hss].GetPtr() , dict_N_os_mc_var[hos].GetPtr() )
        
        if 'mll' in hos and 'mll' in hss:
            drawMean( dict_N_os_mc_var[hos] , 'f_{mc} * N_os' , 0.6346705 , 0.7537155 )
            drawMean( dict_N_ss_mc_var[hss] , 'N_ss' , 0.6776504 , 0.7133758 )

        legends = drawLegend( dict_N_os_mc_var[hos].GetPtr() , "f_mc x N_os_mc" , dict_N_ss_mc_var[hss].GetPtr() , "N_ss_mc" )
        legends.Draw()
        c.Update()
        c.Print( '%s/test_1_%s.png' %( output_ , var ) )
pass

#VALIDATION 2
def mkVal2( df_dicts , dataset_ , output_ ):
    testName="SF x N_ss_mc != N_ss_data"

    k_N_os_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DY'   in x , df_dicts ) ]
    k_N_os_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DATA' in x , df_dicts ) ]
    k_N_ss_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DY'   in x , df_dicts ) ]
    k_N_ss_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DATA' in x , df_dicts ) ]

    # check key                                                                                                                                                                          
    if len(k_N_os_mc)   !=1 : sys.exit()
    if len(k_N_os_data) !=1 : sys.exit()
    if len(k_N_ss_mc)   !=1 : sys.exit()
    if len(k_N_ss_data) !=1 : sys.exit()

    print testName
    # SF x N_ss_mc
    df_N_ss_mc = k_N_ss_mc[0][1].Define( 'SF' , 'getSF( lep1_pt , lep1_eta , lep2_pt , lep2_eta , lep1_pdgId , lep2_pdgId )' ).Define( 'totalW' , 'SF*weights' )
    dict_N_ss_mc_var = PrepareVariable( df_N_ss_mc , k_N_ss_mc[0][0] , dataset_ , testName , 'totalW' )
    # N_ss_data
    df_N_ss_data = k_N_ss_data[0][1].Define( 'totalW' , 'weights')
    dict_N_ss_data_var = PrepareVariable( df_N_ss_data , k_N_ss_data[0][0] , dataset_ , testName , 'totalW' )
    
    #plot 1D STACK kinematics between DATA/MC
    for hmc , hdata in zip( dict_N_ss_mc_var , dict_N_ss_data_var ):
        var = hmc.split('_')[-2]+"_"+hmc.split('_')[-1] if 'lep' in hmc else hmc.split('_')[-1]
        saveHisto1DCompare( dict_N_ss_mc_var[hmc].GetPtr() , dict_N_ss_data_var[hdata].GetPtr() , output_ , "Test2_%s_%s" %( dataset_ , var ) , 0, 4, False , True if 'pt' in hmc else False )
pass

# VALIDATION 3
def mkVal3( df_dicts , dataset_ , output_ ):
    testName="f_data x N_os_mc != N_ss_data"

    k_N_os_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DY'   in x , df_dicts ) ]
    k_N_os_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DATA' in x , df_dicts ) ]
    k_N_ss_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DY'   in x , df_dicts ) ]
    k_N_ss_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DATA' in x , df_dicts ) ]

    # check key
    if len(k_N_os_mc)   !=1 : sys.exit()
    if len(k_N_os_data) !=1 : sys.exit()
    if len(k_N_ss_mc)   !=1 : sys.exit()
    if len(k_N_ss_data) !=1 : sys.exit()

    print testName
    # f_data x N_os_mc
    df_N_os_mc = k_N_os_mc[0][1].Define( 'f_data' , 'getFlip( lep1_pt , lep1_eta , lep2_pt , lep2_eta , 1 )' ).Define( 'totalW' , 'f_data*weights' )
    dict_N_os_mc_var = PrepareVariable( df_N_os_mc , k_N_os_mc[0][0] , dataset_ , testName , 'totalW' )
    # N_ss_data
    df_N_ss_data = k_N_ss_data[0][1].Define( 'totalW' , 'weights')
    dict_N_ss_data_var = PrepareVariable( df_N_ss_data , k_N_ss_data[0][0] , dataset_ , testName , 'totalW' )

    #plot 1D STACK kinematics between DATA/MC
    for hmc , hdata in zip( dict_N_os_mc_var , dict_N_ss_data_var ):
        var = hmc.split('_')[-2]+"_"+hmc.split('_')[-1] if 'lep' in hmc else hmc.split('_')[-1]
        saveHisto1DCompare( dict_N_os_mc_var[hmc].GetPtr() , dict_N_ss_data_var[hdata].GetPtr() , output_ , "Test3_%s_%s" %( dataset_ , var ) , 0, 4, False , True if 'pt' in hmc else False )

pass

# VALIDATION 4
def mkVal4( df_dicts , dataset_ ):

    k_N_os_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DY'   in x , df_dicts ) ]
    k_N_os_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'os' in x and 'DATA' in x , df_dicts ) ]
    k_N_ss_mc   = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DY'   in x , df_dicts ) ]
    k_N_ss_data = [ [ x , df_dicts[x] ] for x in filter( lambda x : 'ss' in x and 'DATA' in x , df_dicts ) ]

    # check key
    if len(k_N_os_mc)   !=1 : sys.exit()
    if len(k_N_os_data) !=1 : sys.exit()
    if len(k_N_ss_mc)   !=1 : sys.exit()
    if len(k_N_ss_data) !=1 : sys.exit()
    
    df_N_ss_mc = k_N_ss_mc[0][1].Sum("weights").GetValue();
    df_N_os_mc = k_N_os_mc[0][1].Sum("weights").GetValue();
    print "Computation on R(MC)"
    print "(%s) frac R_mc : %.4f , accessing 1 - R_mc : %.4f" %( dataset_ , df_N_ss_mc/( df_N_ss_mc + df_N_os_mc) , 1 - ( df_N_ss_mc/( df_N_ss_mc + df_N_os_mc) ) )
pass

if __name__ == '__main__' :

    ntuple="%s/../ntuple/results/" %os.getcwd()

    for idataset in [ 'nanov5_2016',  'nanov5_2017',  'nanov5_2018' ] :
        #if idataset != 'nanov5_2016': continue
        print "dataset : ", idataset
        
        output="plots/%s/validation" %idataset
        if not os.path.exists(output): os.system('mkdir -p %s' %output)

        # initialize 2D histogram
        if not os.path.exists("data/chargeFlip_%s_SF.root" %idataset):
            print "ERROR, file does not exist"
            sys.exit()

        ROOT.loadSF2D( "data/chargeFlip_%s_SF.root" %idataset )

        # load dataset
        DF = OrderedDict({
            'DY_%s' %(idataset) : ROOT.ROOT.RDataFrame("flipper", '%s/%s/DYJetsToLL_M*.root' %( ntuple , idataset ) ),
            'DATA_%s' %(idataset) : ROOT.ROOT.RDataFrame("flipper", [ '%s/%s/DoubleEG.root' %( ntuple , idataset ) ] if idataset != "nanov5_2018" else [ '%s/%s/EGamma.root' %( ntuple , idataset ) ] ),
        })

        #histlist = { key.GetName() : fhist.Get(key.GetName()) for key in ROOT.gDirectory.GetListOfKeys() if not 'analysis' in key.GetName() }
        DF_Dict = PrepareDF( DF , presel(idataset) , "mvaBased_tthmva" )

        mkVal1( DF_Dict , idataset , output )
        mkVal2( DF_Dict , idataset , output )
        mkVal3( DF_Dict , idataset , output )
        mkVal4( DF_Dict , idataset )
