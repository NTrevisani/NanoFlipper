import ROOT
from ROOT import array                                                                                                                      
import os, sys                                                                                                                                                                           
import numpy as np

from collections import OrderedDict                                                                                                                                                      
from array import array as arr

######
# 1.) make nominal histogram Data/MC agreement
# 2.) make histogram in different pt/eta bin
######

def initGrid( eta_bin ):
    etagrid=np.zeros((len(eta_bin)-1,len(eta_bin)-1),dtype=np.object)
    for i in range(len(etagrid)):
        for j in range(len(etagrid[i])):
            #etagrid[i][j]='lep1_eta >= '+str(eta_bin[i])+' && lep1_eta < '+str(eta_bin[i+1])+' && lep2_eta >= '+str(eta_bin[j])+' && lep2_eta < '+str(eta_bin[j+1])
            etagrid[i][j]='abs(lep1_eta)>='+str(eta_bin[i])+' && abs(lep1_eta)<'+str(eta_bin[i+1])+' && abs(lep2_eta)>='+str(eta_bin[j])+' && abs(lep2_eta)<'+str(eta_bin[j+1])
    bins=np.array(eta_bin)
    print(etagrid)
    print(bins)
    return [ bins , etagrid ];
pass

def makeEtaGrid( df2histo_ ,  etabin_ , df_ , histname_ ):
    for i in range(len(etabin_)):
        for j in range(len(etabin_[i])):
            name_ = histname_ + "_etabin" + str(i) + "_etabin" + str(j) + "_mll"
            df_tmp = df_.Filter(etabin_[i][j])
            df2histo_[name_] = df_tmp.Histo1D( ( name_ , "%s ; mll [GeV] ; Events" %name_ , 30, 76.2, 106.2 ), "mll" , "weights" )
pass

def mkVar( df_in , name_ , var_ , bins_ = None ):
    if 'eta' in var_:
        dfout = df_in.Histo1D( ( name_ , '%s ; %s ; Events' %(name_,var_) , 10 , -2.5 , 2.5 ) , var_ , 'weights' )
    elif 'pt' in var_ :
        dfout = df_in.Histo1D( ( name_ , '%s ; %s [GeV] ; Events' %(name_,var_) , 40 , 0. , 200. ) , var_ , 'weights' )
    elif var_ == '2d' and bins_ is not None :
        dfout = df_in.Define('abslep1eta','abs(lep1_eta)').Define('abslep2eta','abs(lep2_eta)').Histo2D( ( name_ , '%s ; Lepton eta 1 ; Lepton eta 2 ; Events' %name_ , len(bins_)-1 , np.asarray(bins_,'d') , len(bins_)-1 , np.asarray(bins_,'d') ) , 'abslep1eta' , 'abslep2eta' , 'weights' )
        #dfout = df_in.Histo2D( ( name_ , 'Event count ONLY %s ; Lepton eta 1 ; Lepton eta 2 ; Events' %name_ , len(bins_)-1 , np.asarray(bins_,'d') , len(bins_)-1 , np.asarray(bins_,'d') ) , 'lep1_eta' , 'lep2_eta' , 'weights' )
    elif var_ == 'mll' or var_ == 'Mll' :
        dfout = df_in.Histo1D( ( name_ , '%s ; %s [GeV]; Events' %(name_ , var_) , 30, 76.2, 106.2 ) , var_ , 'weights' )
    else :
        dfout = df_in
    return dfout
pass

def mkroot( dataset_ , df_ , info_ , wp_ , saveRoot=True ):

    cfg      = info_[0]
    presel   = info_[1]
    signness = info_[2]
    ptbins   = info_[3]
    etabins  = info_[4]
    vars     = info_[5]
    
    rf = ROOT.TFile.Open('hist_%s.root'%(dataset_),"RECREATE")
    df2histo= OrderedDict()

    bins, etagrid = initGrid( etabins )

    print( " Common selection : %s" %presel )

    for idf in df_ :
        # name
        name = idf.split('_')[0]
        print(" name : ", name )
        # define weight
        df = df_[idf].Define( 'weights' , '%s*%s' %( cfg['%s_w'%name] , cfg['WPs'][wp_] if name == 'MC' else cfg['WPs'][wp_].split('*LepSF')[0] ) )
        print( " Common weights : %s*%s" %( cfg['%s_w'%name] , cfg['WPs'][wp_] if name == 'MC' else cfg['WPs'][wp_].split('*LepSF')[0] ) )

        # preselection
        df = df.Filter( presel , "Preselection : %s" %presel )

        # SS/OS region
        for ireg in signness :
            df_tmp = df.Filter( signness[ireg] , '%s selection' %ireg )
            for ivar in vars:
                histname = '%s_%s_%s'%(idf,ireg,ivar)
                df2histo[histname] = mkVar( df_tmp , histname , ivar , bins )
                # make grid for Mll
                if ivar == 'mll' : 
                    for iptbin in ptbins :
                        histname_ptbin = 'analysis_%s_%s_%s' %( idf , ireg , iptbin )
                        df_tmp_ptbin = df_tmp.Filter( ptbins[iptbin] , iptbin  )
                        makeEtaGrid( df2histo , etagrid , df_tmp_ptbin , histname_ptbin )
    if saveRoot:
        print("Saving...")
        map(lambda x: df2histo[x].Write() , df2histo)
        rf.Close()
pass
