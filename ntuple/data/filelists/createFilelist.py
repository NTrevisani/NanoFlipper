#!/bin/python

import os

# 2016
#MCdir="/media/shoh/02A1ACF427292FC0/nanov5/Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6"
#DATAdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__l2tightOR2016v6"
#FAKEdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2016_102X_nAODv5_Full2016v6_ForNewWPs/DATAl1loose2016v6__l2loose__fakeW"

# 2017
#MCdir="/media/shoh/02A1ACF427292FC0/nanov5/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6"
#DATAdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__l2tightOR2017v6"
#FAKEdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2017_102X_nAODv5_Full2017v6_ForNewWPs/DATAl1loose2017v6__l2loose__fakeW"

# 2018
MCdir="/media/shoh/02A1ACF427292FC0/nanov5/Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6"
DATAdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__l2tightOR2018v6"
FAKEdir="/media/shoh/02A1ACF427292FC0/nanov5/Run2018_102X_nAODv6_Full2018v6_ForNewWPs/DATAl1loose2018v6__l2loose__fakeW"


year="2016"
if "2017" in MCdir and "2017" in DATAdir and "2017" in FAKEdir: year = "2017"
if "2018" in MCdir and "2018" in DATAdir and "2018" in FAKEdir:	year = "2018"

if os.path.isdir('%s/%s' %( os.getcwd() , year ) ):
    os.system('rm -r %s/%s' %( os.getcwd() , year ))
os.mkdir('%s/%s' %( os.getcwd() , year ) )

MClist = list(dict.fromkeys([ x.strip('nanoLatino_').split('__')[0] for x in os.listdir(MCdir) ]))
DATAlist = list(dict.fromkeys([ x.strip('nanoLatino_').split('__')[0].split('_')[0] for x in os.listdir(DATAdir) ]))
FAKElist = map( lambda x: "%s_fake" %x , list(dict.fromkeys([ x.strip('nanoLatino_').split('__')[0].split('_')[0] for x in os.listdir(FAKEdir) ])))

for i, ilist in enumerate([ MClist , DATAlist , FAKElist ]) :
    if i == 0 : directory=MCdir
    if i == 1 : directory=DATAdir
    if i == 2 : directory=FAKEdir
    for iprocess in ilist:
        print('creating filelist for process ', iprocess)
        os.system('ls %s/*%s* > %s/%s.txt' %( directory , iprocess if i !=2 else iprocess.split('_')[0] , year , iprocess  ) )
