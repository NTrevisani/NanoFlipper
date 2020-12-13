#! /usr/bin/env python

from optparse import OptionParser
import os, sys, time

cwd = os.getcwd()
usage = "usage: %prog [options]"
parser = OptionParser(usage)
parser.add_option("-d","--dataset", action="store", type="string", dest="dataset", default="nanov5_2016")
parser.add_option("-l","--location", action="store", type="string", dest="location", default="eos")
parser.add_option("-u","--usedataset", action="store", type="string", dest="usedataset", default="muon")
parser.add_option("-b","--batch", action="store_true", dest="batch", default=True)
parser.add_option("-o","--output", action="store", type="string", dest="output", default="%s/results/" %(cwd))
                  
(options, args) = parser.parse_args()

dataset = options.dataset
locations = options.location
usedataset = options.usedataset
dirs = "%s/data/filelists/%s/" % (cwd,dataset)
batch = options.batch
if batch:
    output = options.output + "/batch/%s" %(dataset)
else:
    output = options.output + "%s" %(dataset)

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
###################################################

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

def prepare_batch( proctxt , sample_name , year , nfile=2 ):
    # text file
    textfile = open( proctxt , 'r')
    Lines = [ itxt.replace('\n','') for itxt in textfile.readlines() ]
    split_line = [ Lines[ i:i+nfile ] for i in range(0, len(Lines), nfile) ]
    text_writer( split_line , output , sample_name , year )
    pass

def execute( sample_ , iproc_ , output_ , year_ , batch_ ):
    cmd="./flipskim"
    if batch_ :
        prepare_batch( iproc_ , sample_ , year_ )
    else :
        trun = time.time();
        cmd+=" %s %s %s/%s.root %s" %( sample_ , iproc_ , output_ , sample_ , year_ )
        tproc = time.time()
        os.system("make")
        print(cmd)
        #os.system(cmd)
        #os.system('gdb --args %s' %cmd)
        print("--- running on %s took : %.3f seconds (%.3f minutes) ---" % ( sample , (time.time() - tproc) , (time.time() - tproc)/60. ) )
        print("")
        print("--- Total run time : %.3f seconds (%.3f minutes) ---" % ( (time.time() - trun) , (time.time() - trun)/60. ) )
    pass
    
if __name__ == "__main__" :

    if not os.path.exists(output): os.system( "mkdir -p %s" %( output ) )
    
    samplelists = prepare( dataset , usedataset )
    #lumi = datasets[dataset]['lumi']
    trun = time.time();

    # samplelist refer to txt
    for iproc in samplelists: 
        sample = iproc.split('/')[-1].split('.txt')[0]
        execute( sample , iproc , output , dataset.split('_')[-1] , batch )