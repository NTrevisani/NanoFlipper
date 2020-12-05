#!/bin/bash

for idata in nanov5_2017 #nanov5_2016 nanov5_2017 nanov5_2018
do
    echo "python nanoflipper.py -d $idata"
    python nanoflipper.py -d $idata
done
