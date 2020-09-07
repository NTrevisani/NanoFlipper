
#include "TFile.h"
#include "TTree.h"
#include "TROOT.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TGraph.h"

#include "TF2.h"
#include "TH2.h"
#include "TCutG.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TPaletteAxis.h"


#include <iostream>
#include <fstream>
#include <string>
using namespace std;
#include <cmath>


#include "TObject.h"
#include "TString.h"
#include "TGraph.h"
//#include "TRatioPlot"




// MASTER THESIS



   Double_t fitf(Double_t *val,Double_t *par) {

        Double_t fitval =0;
        Float_t x = val[0];
        Float_t y = val[1];
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=0.0 && val[1]<1.0) fitval = (par[0]*(1-par[0])+par[0]*(1-par[0]))/(1-(par[0]*(1-par[0])+par[0]*(1-par[0])));
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=1.0 && val[1]<1.5) fitval = (par[0]*(1-par[1])+par[1]*(1-par[0]))/(1-(par[0]*(1-par[1])+par[1]*(1-par[0])));
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=1.5 && val[1]<2.5) fitval = (par[0]*(1-par[2])+par[2]*(1-par[0]))/(1-(par[0]*(1-par[2])+par[2]*(1-par[0])));

        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=0.0 && val[1]<1.0) fitval = (par[1]*(1-par[0])+par[0]*(1-par[1]))/(1-par[1]*(1-par[0])-par[0]*(1-par[1]));
        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=1.0 && val[1]<1.5) fitval = (par[1]*(1-par[1])+par[1]*(1-par[1]))/(1-par[1]*(1-par[1])-par[1]*(1-par[1]));
        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=1.5 && val[1]<2.5) fitval = (par[1]*(1-par[2])+par[2]*(1-par[1]))/(1-par[1]*(1-par[2])-par[2]*(1-par[1]));

        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=0.0 && val[1]<0.5) fitval = (par[2]*(1-par[0])+par[0]*(1-par[2]))/(1-par[2]*(1-par[0])-par[0]*(1-par[2]));
        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=0.5 && val[1]<1.0) fitval = (par[2]*(1-par[1])+par[1]*(1-par[2]))/(1-par[2]*(1-par[1])-par[1]*(1-par[2]));
        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=1.0 && val[1]<1.5) fitval = (par[2]*(1-par[2])+par[2]*(1-par[2]))/(1-par[2]*(1-par[2])-par[2]*(1-par[2]));

        return fitval;
}
 Double_t fitf2(Double_t *val,Double_t *par) {

        Double_t fitval =0;
        Float_t x = val[0];
        Float_t y = val[1];
        
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=0.0 && val[1]<1.0) fitval = (par[0]*(1-par[3])+par[3]*(1-par[0]))/(1-(par[0]*(1-par[3])+par[3]*(1-par[0])));
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=1.0 && val[1]<1.5) fitval = (par[0]*(1-par[4])+par[4]*(1-par[0]))/(1-(par[0]*(1-par[4])+par[4]*(1-par[0])));
        if (val[0]>=0.0 && val[0]<1.0 && val[1]>=1.5 && val[1]<2.5) fitval = (par[0]*(1-par[5])+par[5]*(1-par[0]))/(1-(par[0]*(1-par[5])+par[5]*(1-par[0])));

        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=0.0 && val[1]<1.0) fitval = (par[1]*(1-par[3])+par[3]*(1-par[1]))/(1-par[1]*(1-par[3])-par[3]*(1-par[1]));
        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=1.0 && val[1]<1.5) fitval = (par[1]*(1-par[4])+par[4]*(1-par[1]))/(1-par[1]*(1-par[4])-par[4]*(1-par[1]));
        if (val[0]>=1.0 && val[0]<1.5 && val[1]>=1.5 && val[1]<2.5) fitval = (par[1]*(1-par[5])+par[5]*(1-par[1]))/(1-par[1]*(1-par[5])-par[5]*(1-par[1]));

        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=0.0 && val[1]<0.5) fitval = (par[2]*(1-par[3])+par[3]*(1-par[2]))/(1-par[2]*(1-par[3])-par[3]*(1-par[2]));
        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=0.5 && val[1]<1.0) fitval = (par[2]*(1-par[4])+par[4]*(1-par[2]))/(1-par[2]*(1-par[4])-par[4]*(1-par[2]));
        if (val[0]>=1.5 && val[0]<2.5 && val[1]>=1.0 && val[1]<1.5) fitval = (par[2]*(1-par[5])+par[5]*(1-par[2]))/(1-par[2]*(1-par[5])-par[5]*(1-par[2]));

        return fitval;
}



void LeastSquares_PtIndependent(TString FileNameDY, TString FileNameData)
{
	
        TFile* fileDYScale_MC = new TFile(FileNameDY);
        TFile* fileDYScale_DATA = new TFile(FileNameData);

        TH1F* h2D_MC = (TH1F*)fileDYScale_MC->Get("h2_DY");
        TH1F* h2D_DATA = (TH1F*)fileDYScale_DATA->Get("h2_DATASUB");

        TF2 *f2D_MC= new TF2("f2D_MC",fitf,0,2.5,0,2.5,3);
        f2D_MC->SetParLimits(0,0.,1);
        f2D_MC->SetParLimits(1,0.,1);
        f2D_MC->SetParLimits(2,0.,1);

        TCanvas *canvas1 = new TCanvas("canvas1","canvas1");
        canvas1->Divide(1, 1);
        canvas1->cd(1);
        h2D_MC->Draw("lego");
        h2D_MC->Fit("f2D_MC");

        double p0_MC=f2D_MC->GetParameter(0);
        double p1_MC=f2D_MC->GetParameter(1);
        double p2_MC=f2D_MC->GetParameter(2);

        double e0_MC=f2D_MC->GetParError(0);
        double e1_MC=f2D_MC->GetParError(1);
        double e2_MC=f2D_MC->GetParError(2);

        TCanvas *canvas2 = new TCanvas("canvas2","canvas2");
        canvas2->Divide(1, 1);
        canvas2->cd(1);
        h2D_DATA->Draw("lego");
        h2D_DATA->Fit("f2D_MC");

        double p0_DATA=f2D_MC->GetParameter(0);
        double p1_DATA=f2D_MC->GetParameter(1);
        double p2_DATA=f2D_MC->GetParameter(2);

        double e0_DATA=f2D_MC->GetParError(0);
        double e1_DATA=f2D_MC->GetParError(1);
        double e2_DATA=f2D_MC->GetParError(2);

        double SF0=p0_DATA/p0_MC;
        double eSF0=sqrt(pow(e0_DATA/p0_MC,2)+pow(e0_MC*p0_DATA/(p0_MC*p0_MC),2));
        double SF1=p1_DATA/p1_MC;
        double eSF1=sqrt(pow(e1_DATA/p1_MC,2)+pow(e1_MC*p1_DATA/(p1_MC*p1_MC),2));
        double SF2=p2_DATA/p2_MC;
        double eSF2=sqrt(pow(e2_DATA/p2_MC,2)+pow(e2_MC*p2_DATA/(p2_MC*p2_MC),2));

        cout << "SF0 = " << SF0 << " +- " << eSF0 << "\n";
        cout << "SF1 = " << SF1 << " +- " << eSF1 << "\n";
        cout << "SF2 = " << SF2 << " +- " << eSF2 << "\n";
}

void LeastSquares_PtDependent_2bin(TString FileNameDY_Bin1, TString FileNameDY_Bin2,TString FileNameDATA_Bin1,TString FileNameDATA_Bin2)
{
        TFile* fileDYScale_DY_PtBin1 = new TFile(FileNameDY_Bin1);
        TFile* fileDYScale_DY_PtBin2 = new TFile(FileNameDY_Bin2);
        TFile* fileDYScale_DATA_PtBin1 = new TFile(FileNameDATA_Bin1);
        TFile* fileDYScale_DATA_PtBin2 = new TFile(FileNameDATA_Bin2);

        TH1F* h2D_DY_PtBin1 = (TH1F*)fileDYScale_DY_PtBin1->Get("h2_DY");
        TH1F* h2D_DY_PtBin2 = (TH1F*)fileDYScale_DY_PtBin2->Get("h2_DY");
        TH1F* h2D_DATA_PtBin1 = (TH1F*)fileDYScale_DATA_PtBin1->Get("h2_DATASUB");
        TH1F* h2D_DATA_PtBin2 = (TH1F*)fileDYScale_DATA_PtBin2->Get("h2_DATASUB");


	TF2 *f2D_DY_PtBin2= new TF2("f2D_DY_PtBin2",fitf,0,2.5,0,2.5,3);
	f2D_DY_PtBin2->SetParLimits(0,0,1);
	f2D_DY_PtBin2->SetParLimits(1,0,1);
	f2D_DY_PtBin2->SetParLimits(2,0,1);
	TF2 *f2D_DATA_PtBin2= new TF2("f2D_DATA_PtBin2",fitf,0,2.5,0,2.5,3);
	f2D_DATA_PtBin2->SetParLimits(0,0,1);
	f2D_DATA_PtBin2->SetParLimits(1,0,1);
	f2D_DATA_PtBin2->SetParLimits(2,0,1);

        // high pt DY
        TCanvas *canvas1 = new TCanvas("canvas1","canvas1");
        canvas1->Divide(1, 1);
        canvas1->cd(1);
        h2D_DY_PtBin2->Draw("lego");
        h2D_DY_PtBin2->Fit("f2D_DY_PtBin2");

        double p0_DY=f2D_DY_PtBin2->GetParameter(0);
        double p1_DY=f2D_DY_PtBin2->GetParameter(1);
        double p2_DY=f2D_DY_PtBin2->GetParameter(2);

        double e0_DY=f2D_DY_PtBin2->GetParError(0);
        double e1_DY=f2D_DY_PtBin2->GetParError(1);
        double e2_DY=f2D_DY_PtBin2->GetParError(2);

        // low pt DY
        TF2 *f2D_DY_PtBin1= new TF2("f2D_DY_PtBin1",fitf2,0,2.5,0,2.5,6);
        f2D_DY_PtBin1->FixParameter(0,p0_DY);
        f2D_DY_PtBin1->FixParameter(1,p1_DY);
        f2D_DY_PtBin1->FixParameter(2,p2_DY);
        f2D_DY_PtBin1->SetParLimits(3,0,1);
        f2D_DY_PtBin1->SetParLimits(4,0,1);
        f2D_DY_PtBin1->SetParLimits(5,0,1);


        TCanvas *canvas2 = new TCanvas("canvas2","canvas2");
        canvas2->Divide(1, 1);
        canvas2->cd(1);
        h2D_DY_PtBin1->Draw("lego");
        h2D_DY_PtBin1->Fit("f2D_DY_PtBin1");


        double p3_DY=f2D_DY_PtBin1->GetParameter(3);
        double p4_DY=f2D_DY_PtBin1->GetParameter(4);
        double p5_DY=f2D_DY_PtBin1->GetParameter(5);

        double e3_DY=f2D_DY_PtBin1->GetParError(3);
        double e4_DY=f2D_DY_PtBin1->GetParError(4);
        double e5_DY=f2D_DY_PtBin1->GetParError(5);

        // high pt DATA
        TCanvas *canvas3 = new TCanvas("canvas3","canvas3");
        canvas3->Divide(1, 1);
        canvas3->cd(1);
        h2D_DATA_PtBin2->Draw("lego");
        h2D_DATA_PtBin2->Fit("f2D_DATA_PtBin2");

        double p0_DATA=f2D_DATA_PtBin2->GetParameter(0);
        double p1_DATA=f2D_DATA_PtBin2->GetParameter(1);
        double p2_DATA=f2D_DATA_PtBin2->GetParameter(2);

        double e0_DATA=f2D_DATA_PtBin2->GetParError(0);
        double e1_DATA=f2D_DATA_PtBin2->GetParError(1);
        double e2_DATA=f2D_DATA_PtBin2->GetParError(2);

        // low pt DATA
        TF2 *f2D_DATA_PtBin1= new TF2("f2D_DATA_PtBin1",fitf2,0,2.5,0,2.5,6);
        f2D_DATA_PtBin1->FixParameter(0,p0_DATA);
        f2D_DATA_PtBin1->FixParameter(1,p1_DATA);
        f2D_DATA_PtBin1->FixParameter(2,p2_DATA);
        f2D_DATA_PtBin1->SetParLimits(3,0,1);
        f2D_DATA_PtBin1->SetParLimits(4,0,1);
        f2D_DATA_PtBin1->SetParLimits(5,0,1);

        TCanvas *canvas4 = new TCanvas("canvas4","canvas4");
        canvas4->Divide(1, 1);
        canvas4->cd(1);
        h2D_DATA_PtBin1->Draw("lego");
        h2D_DATA_PtBin1->Fit("f2D_DATA_PtBin1");


        double p3_DATA=f2D_DATA_PtBin1->GetParameter(3);
        double p4_DATA=f2D_DATA_PtBin1->GetParameter(4);
        double p5_DATA=f2D_DATA_PtBin1->GetParameter(5);

        double e3_DATA=f2D_DATA_PtBin1->GetParError(3);
        double e4_DATA=f2D_DATA_PtBin1->GetParError(4);
        double e5_DATA=f2D_DATA_PtBin1->GetParError(5);

        double SF0=p0_DATA/p0_DY;
        double eSF0=sqrt(pow(e0_DATA/p0_DY,2)+pow(e0_DY*p0_DATA/(p0_DY*p0_DY),2));
        double SF1=p1_DATA/p1_DY;
        double eSF1=sqrt(pow(e1_DATA/p1_DY,2)+pow(e1_DY*p1_DATA/(p1_DY*p1_DY),2));
        double SF2=p2_DATA/p2_DY;
        double eSF2=sqrt(pow(e2_DATA/p2_DY,2)+pow(e2_DY*p2_DATA/(p2_DY*p2_DY),2));
        
        double SF3=p3_DATA/p3_DY;
        double eSF3=sqrt(pow(e3_DATA/p3_DY,2)+pow(e3_DY*p3_DATA/(p3_DY*p3_DY),2));
        double SF4=p4_DATA/p4_DY;
        double eSF4=sqrt(pow(e4_DATA/p4_DY,2)+pow(e4_DY*p4_DATA/(p4_DY*p4_DY),2));
        double SF5=p5_DATA/p5_DY;
        double eSF5=sqrt(pow(e5_DATA/p5_DY,2)+pow(e5_DY*p5_DATA/(p5_DY*p5_DY),2));

        cout << "SF0 = " << SF0 << " +- " << eSF0 << "\n";
        cout << "SF1 = " << SF1 << " +- " << eSF1 << "\n";
        cout << "SF2 = " << SF2 << " +- " << eSF2 << "\n";
        cout << "SF3 = " << SF3 << " +- " << eSF3 << "\n";
        cout << "SF4 = " << SF4 << " +- " << eSF4 << "\n";
        cout << "SF5 = " << SF5 << " +- " << eSF5 << "\n";
}