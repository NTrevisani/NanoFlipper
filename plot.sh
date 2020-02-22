#!/bin/bash

# 35.87
# 41.53
# 59.74

HISTOGRAMS=$1
OUTPUT=$2
SCALE=35.87 # lumi 

python plot.py $HISTOGRAMS $OUTPUT $SCALE
