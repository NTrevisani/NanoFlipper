//
// Program to fit none-equidistant data points

const Int_t numberParam = 5;
const Int_t nBins = numberParam*numberParam;
Double_t paramA[numberParam],paramAE[numberParam];
Double_t paramB[numberParam],paramBE[numberParam];

Double_t MC_bins[nBins];
Double_t MC_e_bins[nBins];

Double_t DATA_bins[nBins];
Double_t DATA_e_bins[nBins];

Double_t fitfunc1(Int_t i, Double_t *par){

  Double_t value = 0.0; //par[0] transverse from left to right x axis ; bottom to top y axis
  if      (i == 0)   value = ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) / ( 1 - ( par[0] * (1-par[ 0]) + (1-par[ 0]) * par[ 0] ) );
  else if (i == 1)   value = ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) / ( 1 - ( par[0] * (1-par[ 1]) + (1-par[ 0]) * par[ 1] ) );
  else if (i == 2)   value = ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) / ( 1 - ( par[0] * (1-par[ 2]) + (1-par[ 0]) * par[ 2] ) );
  else if (i == 3)   value = ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) / ( 1 - ( par[0] * (1-par[ 3]) + (1-par[ 0]) * par[ 3] ) );
  else if (i == 4)   value = ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) / ( 1 - ( par[0] * (1-par[ 4]) + (1-par[ 0]) * par[ 4] ) );

  else if (i == 5)   value = ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) / ( 1 - ( par[1] * (1-par[ 0]) + (1-par[ 1]) * par[ 0] ) );
  else if (i == 6)   value = ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) / ( 1 - ( par[1] * (1-par[ 1]) + (1-par[ 1]) * par[ 1] ) );
  else if (i == 7)   value = ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) / ( 1 - ( par[1] * (1-par[ 2]) + (1-par[ 1]) * par[ 2] ) );
  else if (i == 8)   value = ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) / ( 1 - ( par[1] * (1-par[ 3]) + (1-par[ 1]) * par[ 3] ) );
  else if (i == 9)   value = ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) / ( 1 - ( par[1] * (1-par[ 4]) + (1-par[ 1]) * par[ 4] ) );

  else if (i == 10)  value = ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) / ( 1 - ( par[2] * (1-par[ 0]) + (1-par[ 2]) * par[ 0] ) );
  else if (i == 11)  value = ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) / ( 1 - ( par[2] * (1-par[ 1]) + (1-par[ 2]) * par[ 1] ) );
  else if (i == 12)  value = ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) / ( 1 - ( par[2] * (1-par[ 2]) + (1-par[ 2]) * par[ 2] ) );
  else if (i == 13)  value = ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) / ( 1 - ( par[2] * (1-par[ 3]) + (1-par[ 2]) * par[ 3] ) );
  else if (i == 14)  value = ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) / ( 1 - ( par[2] * (1-par[ 4]) + (1-par[ 2]) * par[ 4] ) );

  else if (i == 15)  value = ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) / ( 1 - ( par[3] * (1-par[ 0]) + (1-par[ 3]) * par[ 0] ) );
  else if (i == 16)  value = ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) / ( 1 - ( par[3] * (1-par[ 1]) + (1-par[ 3]) * par[ 1] ) );
  else if (i == 17)  value = ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) / ( 1 - ( par[3] * (1-par[ 2]) + (1-par[ 3]) * par[ 2] ) );
  else if (i == 18)  value = ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) / ( 1 - ( par[3] * (1-par[ 3]) + (1-par[ 3]) * par[ 3] ) );
  else if (i == 19)  value = ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) / ( 1 - ( par[3] * (1-par[ 4]) + (1-par[ 3]) * par[ 4] ) );

  else if (i == 20)  value = ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) / ( 1 - ( par[4] * (1-par[ 0]) + (1-par[ 4]) * par[ 0] ) );
  else if (i == 21)  value = ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) / ( 1 - ( par[4] * (1-par[ 1]) + (1-par[ 4]) * par[ 1] ) );
  else if (i == 22)  value = ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) / ( 1 - ( par[4] * (1-par[ 2]) + (1-par[ 4]) * par[ 2] ) );
  else if (i == 23)  value = ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) / ( 1 - ( par[4] * (1-par[ 3]) + (1-par[ 4]) * par[ 3] ) );
  else if (i == 24)  value = ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) / ( 1 - ( par[4] * (1-par[ 4]) + (1-par[ 4]) * par[ 4] ) );

  return value;

}

// minimization function
void fcnMC(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{
  //calculate chisquare
  Double_t chisq = 0;
  Double_t delta;
  for (Int_t i=0;i<nBins; i++) {
    delta  = (MC_bins[i]-fitfunc1(i,par))/MC_e_bins[i];
    chisq += delta*delta;
  }
  f = chisq;
}

void fcnDATA(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{
  //calculate chisquare
  Double_t chisq = 0;
  Double_t delta;
  for (Int_t i=0;i<nBins; i++) {
    delta  = (DATA_bins[i]-fitfunc1(i,par))/DATA_e_bins[i];
    chisq += delta*delta;
  }
  f = chisq;
}

// LeastSquares_PtIndependent
void flip1(TString prefit)
{

  std::cout<<"Reading in root file : "<< prefit <<std::endl;
  TFile* tfile = new TFile(prefit);

  // fit MC
  TH2D* h2D_MC = (TH2D*)tfile->Get("prefit_mc");
  
  Int_t counter=0;
  for (Int_t ix=1 ; ix < h2D_MC->GetNbinsX()+1 ; ix++){
    for (Int_t iy=1 ; iy < h2D_MC->GetNbinsY()+1 ; iy++){
      std::cout<<"MC bincontent : "<<h2D_MC->GetBinContent(ix,iy)<<std::endl;
      std::cout<<"MC bin : "<<h2D_MC->GetBinError(ix,iy)<<std::endl;

      MC_bins[counter] = h2D_MC->GetBinContent(ix,iy);
      MC_e_bins[counter] = h2D_MC->GetBinError(ix,iy);
      counter++;
    }
  }

  TMinuit *gMinuit = new TMinuit(numberParam);  //initialize TMinuit with a maximum of N params
  gMinuit->SetFCN(fcnMC);
  Double_t arglist[numberParam];
  Int_t ierflg = 0;

  arglist[0] = 1;
  gMinuit->mnexcm("SET ERR", arglist ,1,ierflg);

  // Set starting values and step size for parameters
  Double_t vstart[numberParam] = {0.1,0.1,0.1,0.1,0.1};
  Double_t step[numberParam] = {0.0001,0.0001,0.0001,0.0001,0.0001};
  gMinuit->mnparm(0 , "q0",  vstart[0 ], step[0 ], 0,0,ierflg);
  gMinuit->mnparm(1 , "q1",  vstart[1 ], step[1 ], 0,0,ierflg);
  gMinuit->mnparm(2 , "q2",  vstart[2 ], step[2 ], 0,0,ierflg);
  gMinuit->mnparm(3 , "q3",  vstart[3 ], step[3 ], 0,0,ierflg);
  gMinuit->mnparm(4 , "q4",  vstart[4 ], step[4 ], 0,0,ierflg);
  // Now ready for minimization step                                                                                                                                                     
  arglist[0] = 500;
  arglist[1] = 1.;
  gMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);

  // Print results                                                                                                                                                                 
  Double_t amin,edm,errdef;
  Int_t nvpar,nparx,icstat;
  gMinuit->mnstat(amin,edm,errdef,nvpar,nparx,icstat);
  gMinuit->mnprin(3,amin);

  for(int i=0; i<numberParam; i++){
    gMinuit->GetParameter(i,paramA[i],paramAE[i]);
  }

  // Fit DATA
  TH2D* h2D_DATA = (TH2D*)tfile->Get("prefit_data");
  counter=0;
  for (Int_t ix=1 ; ix < h2D_DATA->GetNbinsX()+1 ; ix++){
    for (Int_t iy=1 ; iy < h2D_DATA->GetNbinsY()+1 ; iy++){
      std::cout<<"DATA bincontent : "<<h2D_DATA->GetBinContent(ix,iy)<<std::endl;
      std::cout<<"DATA bin : "<<h2D_DATA->GetBinError(ix,iy)<<std::endl;
      DATA_bins[counter] = h2D_DATA->GetBinContent(ix,iy);
      DATA_e_bins[counter] = h2D_DATA->GetBinError(ix,iy);
      counter++;
    }
  }

  TMinuit *fMinuit = new TMinuit(numberParam);  //initialize TMinuit with a maximum of N params
  fMinuit->SetFCN(fcnDATA);
  //arglist
  ierflg = 0;

  arglist[0] = 1;
  fMinuit->mnexcm("SET ERR", arglist ,1,ierflg);

  // Set starting values and step size for parameters
  Double_t vstart2[numberParam] = {0.1,0.1,0.1,0.1,0.1};
  Double_t step2[numberParam] = {0.0001,0.0001,0.0001,0.0001,0.0001};
  fMinuit->mnparm(0 , "q0",  vstart2[0 ], step2[0 ], 0,0,ierflg);
  fMinuit->mnparm(1 , "q1",  vstart2[1 ], step2[1 ], 0,0,ierflg);
  fMinuit->mnparm(2 , "q2",  vstart2[2 ], step2[2 ], 0,0,ierflg);
  fMinuit->mnparm(3 , "q3",  vstart2[3 ], step2[3 ], 0,0,ierflg);
  fMinuit->mnparm(4 , "q4",  vstart2[4 ], step2[4 ], 0,0,ierflg);
  
  // Now ready for minimization step
  arglist[0] = 500;
  arglist[1] = 1.;
  fMinuit->mnexcm("MIGRAD", arglist ,2,ierflg);

  // Print results
  Double_t amin2,edm2,errdef2;
  Int_t nvpar2,nparx2,icstat2;
  fMinuit->mnstat(amin2,edm2,errdef2,nvpar2,nparx2,icstat2);
  fMinuit->mnprin(3,amin2);

  for(int i=0; i<numberParam; i++){
    fMinuit->GetParameter(i,paramB[i],paramBE[i]);
  }


  Double_t SF0=paramB[0]/paramA[0];
  Double_t eSF0=sqrt(pow(paramBE[0]/paramA[0],2)+pow(paramAE[0]*paramB[0]/(paramA[0]*paramA[0]),2));

  Double_t SF1=paramB[1]/paramA[1];
  Double_t eSF1=sqrt(pow(paramBE[1]/paramA[1],2)+pow(paramAE[1]*paramB[1]/(paramA[1]*paramA[1]),2));

  Double_t SF2=paramB[2]/paramA[2];
  Double_t eSF2=sqrt(pow(paramBE[2]/paramA[2],2)+pow(paramAE[2]*paramB[2]/(paramA[2]*paramA[2]),2));

  Double_t SF3=paramB[3]/paramA[3];
  Double_t eSF3=sqrt(pow(paramBE[3]/paramA[3],2)+pow(paramAE[3]*paramB[3]/(paramA[3]*paramA[3]),2));

  Double_t SF4=paramB[4]/paramA[4];
  Double_t eSF4=sqrt(pow(paramBE[4]/paramA[4],2)+pow(paramAE[4]*paramB[4]/(paramA[4]*paramA[4]),2));

  
  std::cout << "SF0 = " << SF0 << " +- " << eSF0 << " (" << 100*(eSF0/SF0) << "%) \n";
  std::cout << "SF1 = " << SF1 << " +- " << eSF1 << " (" << 100*(eSF1/SF1) << "%) \n";
  std::cout << "SF2 = " << SF2 << " +- " << eSF2 << " (" << 100*(eSF2/SF2) << "%) \n";
  std::cout << "SF3 = " << SF3 << " +- " << eSF3 << " (" << 100*(eSF3/SF3) << "%) \n";
  std::cout << "SF4 = " << SF4 << " +- " << eSF4 << " (" << 100*(eSF4/SF4) << "%) \n";

}
