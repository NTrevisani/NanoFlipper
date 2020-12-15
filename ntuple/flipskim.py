#! /usr/bin/env python

from optparse import OptionParser
import os, sys, time

cwd = os.getcwd()
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
parser.add_option("-l","--location", action="store", type="string", dest="location", default="%s/data/filelists" %(cwd) )
parser.add_option("-s", "--Samples", action="append", type="string", dest="Samples" , default=[])
parser.add_option("-b","--batch", action="store_true", dest="batch", default=False)
parser.add_option("-t","--test", action="store_true", dest="test", default=False)
parser.add_option("-n","--nfile", action="store", type="int", dest="nfile", default=10)
parser.add_option("-o","--output", action="store", type="string", dest="output", default="%s/results/" %(cwd))
                  
(options, args) = parser.parse_args()

dataset = options.dataset
Samples = options.Samples
location = options.location + "/" + dataset
batch = options.batch
test = options.test
nfile = options.nfile
if batch:
    output = options.output + "/batch/%s" %(dataset)
else:
    output = options.output + "%s" %(dataset)

source=""

datasets={
    'nanov5_2016' : {
        'lumi'      : '35.867',
        'DATA_path' : 'Run2016_102X_nAODv5_Full2016v6/DATAl1loose2016v6__l2loose__l2tightOR2016v6',
        'MC_path'   : 'Summer16_102X_nAODv5_Full2016v6/MCl1loose2016v6__MCCorr2016v6__l2loose__l2tightOR2016v6'
    },
    'nanov5_2017' : {
        'lumi' : "41.53",
        'DATA_path' : 'Run2017_102X_nAODv5_Full2017v6/DATAl1loose2017v6__l2loose__l2tightOR2017v6',
        'MC_path'   : 'Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__l2loose__l2tightOR2017v6'
    },
    'nanov5_2018' : {
        'lumi' : "59.74",
        'DATA_path' : 'Run2018_102X_nAODv6_Full2018v6/DATAl1loose2018v6__l2loose__l2tightOR2018v6',
        'MC_path'   : 'Autumn18_102X_nAODv6_Full2018v6/MCl1loose2018v6__MCCorr2018v6__l2loose__l2tightOR2018v6'
    }
}

# detect database ; make list
if '/home/shoh'	in os.getcwd() :
    # my stash
    source="/media/shoh/02A1ACF427292FC0/nanov5"
elif '/lustre' in os.getcwd() or '/homeui' in os.getcwd() :
    # padova
    source = "/"
elif '/afs/cern.ch/user' in os.getcwd() :
    source = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano"
###################################################

def prepare( dataset_ , source_ , fake=False ):
    out=[]
    for isample in Samples:
        path=""
        if isample in [ 'SingleElectron' , 'SingleMuon' , 'MuonEG' , 'DoubleEG' , 'DoubleMuon' , 'EGamma' ]:
            path=datasets[dataset_]['DATA_path']
        else:
            path=datasets[dataset_]['MC_path']
        os.system( "ls %s/%s/*%s* > %s/%s.txt" %( source_ , path , isample , location , isample ) )
        out.append( "%s/%s.txt" %( location , isample ) )
    print("")
    print(" --> preparing samplelist : ", out)
    print("")
    return out
pass

def submit_script( sample_name__ , jobname_ , output_ , year_ ):
    outscript=jobname_.replace('.txt','.sh')
    outname=jobname_.split('/')[-1].split('.txt')[0]
    with open( outscript , 'a') as script :
        script.write('#!/bin/bash\n')
        # source environment ?
        # script.write('')
        script.write('make\n')
        script.write('./flipskim %s %s %s/%s.root %s\n' %( sample_name__ , jobname_ , output_ , outname , year_ ) )
    os.system( 'chmod +x %s' %outscript )
    pass

def text_writer( split_line_ , output_ , sample_name_ , year_ ):
    for num , ichunck in enumerate(split_line_) :
        jobname = '%s/%s__job%s.txt' %( output_ , sample_name_ , num )
        f=open( jobname , 'w' )
        f.write( '\n'.join(ichunck) )
        submit_script( sample_name_ , jobname , output_ , year_ )
        f.close()
    pass

def prepare_batch( proctxt , sample_name , year , nfile ):
    # text file
    textfile = open( proctxt , 'r')
    Lines = [ itxt.replace('\n','') for itxt in textfile.readlines() ]
    split_line = [ Lines[ i:i+nfile ] for i in range(0, len(Lines), nfile) ]
    text_writer( split_line , output , sample_name , year )
    pass

def execute( sample_ , iproc_ , output_ , year_ , batch_ ):
    cmd="./flipskim"
    if batch_ :
        prepare_batch( iproc_ , sample_ , year_ , nfile )
    else :
        trun = time.time();
        cmd+=" %s %s %s/%s.root %s" %( sample_ , iproc_ , output_ , sample_ , year_ )
        tproc = time.time()
        if not test: os.system("make")
        print(cmd)
        if not test: os.system(cmd)
        #os.system('gdb --args %s' %cmd)
        print("--- running on %s took : %.3f seconds (%.3f minutes) ---" % ( sample , (time.time() - tproc) , (time.time() - tproc)/60. ) )
        print("")
        print("--- Total run time : %.3f seconds (%.3f minutes) ---" % ( (time.time() - trun) , (time.time() - trun)/60. ) )
    pass
    
if __name__ == "__main__" :

    # detect database ; make list
    if '/home/shoh' in os.getcwd() :
    # my stash
        source="/media/shoh/02A1ACF427292FC0/nanov5"
    elif '/lustre' in os.getcwd() or '/homeui' in os.getcwd() :
        # padova
        source = "/"
    elif '/afs/cern.ch/user' in os.getcwd() :
        source = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano"

    if not os.path.exists(output)   : os.system( "mkdir -p %s" %output   )
    if not os.path.exists(location) : os.system( "mkdir -p %s" %location ) 
    
    # output filelist
    samplelists = prepare( dataset , source )
    trun = time.time();

    # samplelist refer to txt
    for iproc in samplelists:
        sample = iproc.split('/')[-1].split('.txt')[0]
        execute( sample , iproc , output , dataset.split('_')[-1] , batch )
