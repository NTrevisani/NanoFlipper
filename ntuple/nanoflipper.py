#! /usr/bin/env python

from optparse import OptionParser
import os, sys, time
cwd = os.getcwd()
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
parser.add_option("-l","--location", action="store", type="string", dest="location", default="eos")
parser.add_option("-o","--output", action="store", type="string", dest="output", default="%s/results/" %(cwd))
                  
(options, args) = parser.parse_args()

datasets = options.dataset
locations = options.location
dirs = "%s/data/filelists/%s/" % (cwd,datasets)
output = options.output + "%s" %(datasets)
samplelists=[]
lumi=""

tcompile = time.time()
os.system("make")
print("--- compilation took : %.3f seconds (%.3f minutes) ---" % ( (time.time() - tcompile) , (time.time() - tcompile)/60. ) )

# predefined samples
if datasets == 'nanov5_2016':
    lumi = "35.867"
    for itxt in [ "DYJetsToLL_M-10to50-LO.txt" , "DYJetsToLL_M-50-LO_ext2.txt" , "SingleElectron.txt" , "Fake_SingleElectron.txt" , "DoubleEG.txt" , "Fake_DoubleEG.txt" ]:
        if 'DY' in itxt : continue;
        samplelists.append( dirs + itxt )
elif datasets == 'nanov5_2017':
    lumi="41.53"
    for	itxt in [ "DYJetsToLL_M-10to50-LO_ext1.txt" , "DYJetsToLL_M-50-LO_ext1.txt" , "SingleElectron.txt" , "Fake_SingleElectron.txt" , "DoubleEG.txt" , "Fake_DoubleEG.txt" ]:
        if 'DY' in itxt : continue;
        samplelists.append( dirs + itxt )
elif datasets == 'nanov5_2018':
    lumi = "59.74"
    for itxt in [ "DYJetsToLL_M-10to50-LO_ext1.txt" , "DYJetsToLL_M-50-LO.txt" , "EGamma.txt" , "Fake_EGamma.txt" ]:
        if 'DY' in itxt : continue;
        samplelists.append( dirs + itxt )
else:
    print(' >>> ERROR: Dude... really? Pick one datasets here <<<')
    os.system('ls data/filelists/')
    print(' exp: python nanotnp.py -d nanov5_2016')
    sys.exit(0)

if not os.path.exists(output):
    os.system("mkdir -p %s" %output)

print("year : %s" %(datasets))
print("lumi : %s 1/fb" %(lumi))

#if len(samplelists)!=3: print("ERROR: len(samplelists)!=3"); sys.exit(0);

trun = time.time();
for iproc in samplelists:
    sample = iproc.split('/')[-1].split('.txt')[0]
    cmd="./nanoflipper"; cmd+=" %s %s %s/%s.root %s %s" %(sample,iproc,output,sample,lumi,datasets.split('_')[-1])
    tproc = time.time()
    print(cmd)
    os.system(cmd)
    #os.system('gdb --args %s' %cmd)
    print("--- running on %s took : %.3f seconds (%.3f minutes) ---" % ( sample , (time.time() - tproc) , (time.time() - tproc)/60. ) )
print("--- Total run time : %.3f seconds (%.3f minutes) ---" % ( (time.time() - trun) , (time.time() - trun)/60. ) )
