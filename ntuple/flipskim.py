#! /usr/bin/env python

from optparse import OptionParser
import os, sys, time

cwd = os.getcwd()
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
parser.add_option("-l","--location", action="store", type="string", dest="location", default="eos")
parser.add_option("-u","--usedataset", action="store", type="string", dest="usedataset", default="muon")
parser.add_option("-o","--output", action="store", type="string", dest="output", default="%s/results/" %(cwd))
                  
(options, args) = parser.parse_args()

dataset = options.dataset
locations = options.location
usedataset = options.usedataset
dirs = "%s/data/filelists/%s/" % (cwd,dataset)
output = options.output + "%s" %(dataset)
samplelists=[]
lumi=""

datasets={
    'nanov5_2016' : {
        'lumi' : '35.867',
        'mc' : [ "DYJetsToLL_M-50-LO_ext2.txt" ],
        'electron' : [ "SingleElectron.txt" , "DoubleEG.txt" ],
        'muon' : [ "SingleMuon.txt" ]
    },
    'nanov5_2017' : {
        'lumi' : "41.53",
        'mc' : [ "DYJetsToLL_M-50-LO_ext1.txt" ],
        'electron' : [ "SingleElectron.txt" , "DoubleEG.txt" ],
        'muon' : [ "SingleMuon.txt" ]
    },
    'nanov5_2018' : {
        'lumi' : "59.74",
        'mc' : [ "DYJetsToLL_M-50-LO.txt" ],
        'electron' : [ "EGamma.txt" ],
        'muon' : [ "SingleMuon" ]
    }
}

def prepare( dataset_ , usedataset_ , fake=False ):
    out=[]
    for itxt in ( datasets[dataset_]['mc'] + datasets[dataset_][usedataset_] ) :
        out.append( dirs + itxt )
        if fake and 'DY' not in i:
            itxt = 'Fake_'+itxt
            out.append( dirs + itxt )
    print("preparing samplelist : ", out)
    return out
pass

if not os.path.exists(output): os.system("mkdir -p %s" %output)

print("year : %s" %(datasets))
print("lumi : %s 1/fb" %(lumi))

if __name__ == "__main__" :

    #tcompile = time.time()
    #os.system("make")
    #print("--- compilation took : %.3f seconds (%.3f minutes) ---" % ( (time.time() - tcompile) , (time.time() - tcompile)/60. ) )
    
    samplelists = prepare( dataset , usedataset )

    trun = time.time();
    for iproc in samplelists:
        sample = iproc.split('/')[-1].split('.txt')[0]
        cmd="./flipskim"; cmd+=" %s %s %s/%s.root %s %s" %(sample,iproc,output,sample,lumi,dataset.split('_')[-1])
        tproc = time.time()
        print(cmd)
        #os.system(cmd)
        #os.system('gdb --args %s' %cmd)
        print("--- running on %s took : %.3f seconds (%.3f minutes) ---" % ( sample , (time.time() - tproc) , (time.time() - tproc)/60. ) )
        print("")
    print("--- Total run time : %.3f seconds (%.3f minutes) ---" % ( (time.time() - trun) , (time.time() - trun)/60. ) )
        
