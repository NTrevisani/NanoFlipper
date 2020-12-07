#!/bin/bash

for idata in nanov5_2016 nanov5_2017 nanov5_2018
do
    echo "python mkHist.py -d $idata"
    python mkHist.py -d $idata
done

#python mkZfit.py
#python mkFlipSf.py
