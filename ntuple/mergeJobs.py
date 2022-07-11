#! /usr/bin/env python
from optparse import OptionParser
import os, sys, time

cwd = os.getcwd()
usage = "usage: %prog [options]"
parser = OptionParser(usage)

parser.add_option("-d", "--dataset",  action="store", type="string", dest="dataset",  default="nanov5_2016")
parser.add_option("-l", "--location", action="store", type="string", dest="location", default="%s/results/batch" %(cwd) )
parser.add_option("-o", "--output",   action="store", type="string", dest="output",   default="%s/results" %(cwd))
#parser.add_option("-s", "--Samples", action="append", type="string", dest="Samples" , default=[])

(options, args) = parser.parse_args()

dataset  = options.dataset
location = options.location + "/" + dataset
output   = options.output + "/" + dataset

# infer samples
megalist = os.listdir(location)
Samples_dict = dict.fromkeys( map(lambda x : x.split('__')[0].split('/')[0] , megalist ) )
Samples = list( Samples_dict )
print( "Inferred Samples : ", Samples )

errJob=[]
rootfiles=[]
# check health of jobs
for ierr in megalist :
    if '.root' in ierr: rootfiles.append(ierr)
    if '.err' not in ierr: continue
    filesize = os.path.getsize( location + "/" + ierr)
    if filesize != 0 : errJob.append(ierr)

if len(errJob)>0:
    print(" -- > Job Error found , please resubmit:")
    for ijoberr in errJob :
        print(ijoberr)
    sys.exit()
else:
    print(" --> ALL JOB PROCESSED <-- ")
    
# MERGING
for isample in Samples :
    Samples_dict[isample] = []
    for iroot in rootfiles :
        if isample+"__" == iroot.split('job')[0] :
            Samples_dict[isample].append( location + "/" + iroot )

if not os.path.exists(output) : 
    os.system( "mkdir -p %s" %output   )
else:
    os.system( "rm -rf %s" %output   )
    os.system( "mkdir -p %s" %output   )

for iname in Samples_dict :
    print(     "python haddnano.py %s/%s.root %s" %( output , iname , " ".join(Samples_dict[iname]) ) )
    os.system( "python haddnano.py %s/%s.root %s" %( output , iname , " ".join(Samples_dict[iname]) ) )
    
