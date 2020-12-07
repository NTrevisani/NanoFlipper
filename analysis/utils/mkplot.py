import ROOT
import os, sys
from collections import OrderedDict

from helper import *

sys.path.append('%s/..' %os.getcwd() )
import mkHist

def mkplot( dataset ,  plotFake ):

    rf = 'hist_%s.root'%(dataset)
                                                                                                                                                                                         
    f = ROOT.TFile.Open(rf,"READ")                                                                                                                                                       
    output= 'plots/%s/mkHist_validation/noFake' %( dataset ) if not plotFake else 'plots/%s/mkHist_validation/withFake' %( dataset )                                                     
    if not os.path.exists(output): os.system('mkdir -p %s' %output)                                                                                                                      
                                                                                                                                                                                         
    # convert list of branch into key-branch dictionary                                                                                                                                  
    histkeys=[ key.GetName() for key in f.GetListOfKeys() ]                                                                                                                              
    histlist = OrderedDict( zip( map(lambda x : x, histkeys) , map(lambda x : f.Get(x), histkeys) ) )                                                                                    
                                                                                                                                                                                         
    #####################                                                                                                                                                                
                                                                                                                                                                                         
    oskeys = filter(lambda x : 'etabin' not in x and 'os' in x , histkeys)                                                                                                               
    sskeys = filter(lambda x : 'etabin' not in x and 'ss' in x , histkeys)                                                                                                               
    if not plotFake:                                                                                                                                                                     
        oskeys = filter(lambda x : 'FAKE' not in x , oskeys)                                                                                                                             
        sskeys = filter(lambda x : 'FAKE' not in x , sskeys)                                                                                                                             
                                                                                                                                                                                         
    #plot 1D STACK kinematics between DATA/MC                                                                                                                                            
    for ireg in [ sskeys , oskeys ]:                                                                                                                                                     
        for jvar in mkHist.variables:                                                                                                                                                           
            if jvar=='2d': continue                                                                                                                                                      
            regvar = filter( lambda x: jvar in x , ireg )                                                                                                                                
            insitu = OrderedDict( zip( map(lambda x : x , regvar) , map(lambda x : histlist[x], regvar) ) )                                                                              
            SaveHisto1D( insitu , regvar[0].strip('%s_' %regvar[0].split('_')[0]) , output , 0, 4, False , True if jvar in [ 'lep1_pt' , 'lep2_pt' ] else False , False )                
                                                                                                                                                                                         
    #plot 1D kinematics of SS/OS both for MC and Data                                                                                                                                    
    for sskey, oskey in zip ( sskeys , oskeys ):                                                                                                                                         
        #print 'sskey : ', sskey , ' ; oskey : ', oskey                                                                                                                                  
        h_sskey = histlist[sskey] ; h_oskey = histlist[oskey]                                                                                                                            
        SaveRatio( h_sskey , h_oskey , sskey , output )                                                                                                                                  
    pass  
