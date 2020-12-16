import ROOT
import os, sys
from collections import OrderedDict

from helper import *

#sys.path.append('%s/..' %os.getcwd() )
#import analysis

def mkplot( dataset , info_ ):
    
    cfg      = info_[0]
    presel   = info_[1]
    signness = info_[2]
    ptbins   = info_[3]
    etabins  = info_[4]
    vars     = info_[5]


    rf = 'hist_%s.root'%(dataset)
                                                                                                                                                                                         
    f = ROOT.TFile.Open(rf,"READ")                                                                                                                                                       
    output= 'plots/%s/step1_plot_ntuple' %( dataset )            
    if not os.path.exists(output): os.system('mkdir -p %s' %output)                                                                                                                      
                                                                                                                                                                                         
    # convert list of branch into key-branch dictionary                                                                                                                                  
    histkeys=[ key.GetName() for key in f.GetListOfKeys() ]                                                                                                                              
    histlist = OrderedDict( zip( map(lambda x : x, histkeys) , map(lambda x : f.Get(x), histkeys) ) )                                                                                    
                                                                                                                                                                                         
    #####################                                                                                                                                                                
                                                                                                                                                                                         
    oskeys = filter(lambda x : 'etabin' not in x and 'os' in x , histkeys)                                                                                                               
    sskeys = filter(lambda x : 'etabin' not in x and 'ss' in x , histkeys)

    #plot 1D STACK kinematics between DATA/MC                                                                                                                                            
    for ireg in [ sskeys , oskeys ]:                                                                                                                                                     
        for jvar in vars:                                                                                                                                                           
            if jvar=='2d': continue                                                                                                                                                      
            regvar = filter( lambda x: jvar in x , ireg )                                                                                                                                
            # data ; mc pair same region same variable
            insitu = OrderedDict( zip( map(lambda x : x , regvar) , map(lambda x : histlist[x], regvar) ) )
            
            SaveHisto1D( insitu , regvar[0].strip('%s_' %regvar[0].split('_')[0]) , output , 0, 4, False , True if jvar in [ 'lep1_pt' , 'lep2_pt' ] else False , False )                
                                                                                                                                                                                         
    #plot 1D kinematics of SS/OS both for MC and Data                                                                                                                                    
    for sskey, oskey in zip ( sskeys , oskeys ):                                                                                                                                         
        #print 'sskey : ', sskey , ' ; oskey : ', oskey                                                                                                                                  
        h_sskey = histlist[sskey] ; h_oskey = histlist[oskey]                                                                                                                            
        SaveRatio( h_sskey , h_oskey , sskey , output )                                                                                                                                  
    pass  
