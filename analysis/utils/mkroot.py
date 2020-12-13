import ROOT
from ROOT import array                                                                                                                                                                   
import os, sys                                                                                                                                                                           
import numpy as np

from collections import OrderedDict                                                                                                                                                      
from array import array as arr

sys.path.append('%s/..' %os.getcwd() )

from mkHist import *

######
# 1.) make nominal histogram Data/MC agreement
# 2.) make histogram in different pt/eta bin
######

def initGrid( eta_bin ):
    etagrid=np.zeros((len(eta_bin)-1,len(eta_bin)-1),dtype=np.object)
    for i in range(len(etagrid)):
        for j in range(len(etagrid[i])):
            etagrid[i][j]='abs(lep1_eta)>='+str(eta_bin[i])+' && abs(lep1_eta)<'+str(eta_bin[i+1])+' && abs(lep2_eta)>='+str(eta_bin[j])+' && abs(lep2_eta)<'+str(eta_bin[j+1])
    bins=np.array(eta_bin)
    return [ bins , etagrid ];
pass

def makeEtaGrid(etagrid,indf,iterdf,prefix):    
    for i in range(len(etagrid)):                                                                                                                                                               for j in range(len(etagrid[i])):                                                                                                                                                            prefix_tmp=prefix+"_etabin"+str(i)+"_etabin"+str(j)+"_mll"                                                                                                                              dftmp=iterdf.Filter(etagrid[i][j])                                                                                                                                                      indf[prefix_tmp]=dftmp.Histo1D( ( prefix_tmp , "%s ; mll [GeV] ; Events" %prefix_tmp , 30, 76.2, 106.2 ), "mll","weights")
pass

def addWeights( df_in , name , wp ):   
    dfout = df_in[name]                                                                                                                                           
    weight='1==1'

    if 'DY' in name:                                                                                                                                                                     
        # SFweight2l = puWeight*TriggerEffWeight_2l*Lepton_RecoSF[0]*Lepton_RecoSF[1]*EMTFbug_veto                                                                                       
        # XSWeight = baseW*genWeight                                                                                                                                                     
        # METFilter_Common = vent.Flag_goodVertices*\                                                                                                                                    
        #         event.Flag_globalSuperTightHalo2016Filter*\                                                                                                                            
        #         event.Flag_HBHENoiseFilter*\                                                                                                                                           
        #         event.Flag_HBHENoiseIsoFilter*\                                                                                                                                        
        #         event.Flag_EcalDeadCellTriggerPrimitiveFilter*\                                                                                                                        
        #         event.Flag_BadPFMuonFilter\                                                                                                                                            
        # GenLepMatch2l = event.Lepton_genmatched[0]*\                                                                                                                                   
        #                 event.Lepton_genmatched[1] \                                                                                                                                   
        # gen_promptmatch = Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1]
        common="ptllDYW*SFweight2l*XSWeight*METFilter_MC*GenLepMatch2l"   
        if '2016' in name:                                                                                                                                                               
            weight="35.92*%s*%s" %( common , WPs['2016'][wp] )                                                                                                                           
        elif '2017' in name:                                                                                                                                                             
            weight="41.53*%s*%s" %(common,WPs['2017'][wp])                                                                                                                               
        elif '2018' in name:                                                                                                                                                             
            weight="59.74*%s*%s" %(common,WPs['2018'][wp])                                                                                                                               
        print( " MC weights : %s" %weight )                                                                                                                                              
    elif 'DATA' in name:                                                                                                                                                                 
        common="METFilter_DATA*Trigger_dblEl" #Trigger_dblEl
        if '2016' in name:                                                                                                                                                               
            weight="%s*%s" %( common , WPs['2016'][wp].replace( WPs['2016'][wp].split('*')[-1], "(1==1)" ) )                                                                             
        elif '2017' in name:                                                                                                                                                             
            weight="%s*%s" %( common ,  WPs['2017'][wp].replace( WPs['2017'][wp].split('*')[-1], "(1==1)" ) )                                                                            
        elif '2018' in name:                                                                                                                                                             
            weight="%s*%s" %( common ,  WPs['2018'][wp].replace( WPs['2018'][wp].split('*')[-1], "(1==1)" ) )                                                                            
        print( " DATA weights : %s" %weight )                                                                                                                                            
    elif 'FAKE' in name:                                                                                                                                                                 
        common="METFilter_FAKE*Trigger_dblEl"
        if '2016' in name:                                                                                                                                                               
            weight="%s*%s" %( common , WPs['2016']['fake_'+wp] )                                                                                                                         
        elif '2017' in name:                                                                                                                                                             
            weight="%s*%s" %( common , WPs['2017']['fake_'+wp] )                                                                                                                         
        elif '2018' in name:                                                                                                                                                             
            weight="%s*%s" %( common , WPs['2018']['fake_'+wp] )                                                                                                                         
        print( " FAKE weights : %s" %weight )                                                                                                                                            
                                                                                                                                                                                         
    return dfout.Define('weights',weight).Define('abslep1eta','abs(lep1_eta)').Define('abslep2eta','abs(lep2_eta)')
pass

def mkroot( dataset_ , DFS , eta_bin_ , presel , WPs_ , saveRoot=True ):
    
    rf = ROOT.TFile.Open('hist_%s.root'%(dataset_),"RECREATE")
    df2histo= OrderedDict()

    bins, etagrid = initGrid(eta_bin_)

    print( " Common selection : %s" %presel )
                                                                                                                                                                                         
    for idf in DFS:                                                                                                                           
        DYregion = addWeights( DFS , idf , WPs_ )
        # common cuts                                                                                                                                           
        DYregion = DYregion.Filter( presel , presel )                                                                                             
        #SS/OS
        for ireg in signness:                                                                                                                                                            
            tmp_df_1 = DYregion.Filter( signness[ireg] , '%s selection' %ireg )                                                                                                          
            for ivar in variables:                                                                                                                                                       
                if 'eta' in ivar:                                                                                                                                                        
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar) , '%s_%s_%s ; %s; Events' %(idf,ireg,ivar,ivar) , 10 , -2.5 , 2.5 ) , ivar , 'weights' )
                elif 'pt' in ivar:
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar) , '%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,ivar,ivar) , 40 , 0. , 200. ) , ivar , 'weights' )
                #################################################################################################################                     
                elif ivar=='2d':                                                                                                                                                         
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)] = tmp_df_1.Histo2D( ( '%s_%s_%s'%(idf,ireg,ivar) ,' %s_%s_%s ; Lepton eta 1 ; Lepton eta 2 ; Events.' %(idf,ireg,ivar), len(bins)-1 , np.asarray(bins,'d') , len(bins)-1 , np.asarray(bins,'d') ) , 'abslep1eta' , 'abslep2eta' , 'weights' )
                elif ivar=='mll':
                    df2histo['%s_%s_%s'%(idf,ireg,ivar)]  = tmp_df_1.Histo1D( ( '%s_%s_%s'%(idf,ireg,ivar), '%s_%s_%s ; %s [GeV]; Events' %(idf,ireg,ivar,ivar) , 30, 76.2, 106.2 ) , ivar , 'weights' )
                    ## mll in different etabins and ptbins
                    for iptbin in ptbin:                                                                                                                                                 
                        tmp_df_2 = tmp_df_1.Filter( ptbin[iptbin] , '%s selection' %iptbin )                                                                                             
                        makeEtaGrid( etagrid , df2histo , tmp_df_2 , 'analysis_%s_%s_%s'%(idf,iptbin,ireg) )                                                                                       
            #report = tmp_df_1.Report()
            #report.Print()
    if saveRoot:
        map(lambda x: df2histo[x].Write() , df2histo)                                                                                                                                        
        rf.Close()                                                                                                                                                                     
                                                                                                                                                                                         
    pass                                                                              
