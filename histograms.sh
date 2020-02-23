#!/bin/bash

set -e

INPUT_DIR=$1
OUTPUT_DIR=$2

# Produce histograms from skimmed samples
while IFS=, read -r SAMPLE PROCESS
do
    YEAR=`echo ${INPUT_DIR} | awk -F "/" '{ print $NF }'`
    if [ -z "$YEAR" ]; then
	YEAR=`echo ${INPUT_DIR} | awk -F "/" '{ print $(NF-1) }'`
    fi

    if [ ! -e ${OUTPUT_DIR}/${YEAR} ]; then
        mkdir -p ${OUTPUT_DIR}/${YEAR}
    fi
    
    INPUT=${INPUT_DIR}/${SAMPLE}_Skim.root
    OUTPUT=${OUTPUT_DIR}/${YEAR}/histograms_${PROCESS}.root
    echo "python histograms.py $INPUT $PROCESS $OUTPUT"
    python histograms.py $INPUT $PROCESS $OUTPUT
done < histograms.csv

# Merge histograms in a single file
hadd -f ${OUTPUT_DIR}/${YEAR}/histograms.root ${OUTPUT_DIR}/${YEAR}/histograms_*.root
