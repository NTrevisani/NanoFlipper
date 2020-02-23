#!/bin/bash

set -e

INPUT_DIR="/media/shoh/02A1ACF427292FC0/latinov6"
OUTPUT_DIR=$1

# Compile executable
echo ">>> Compile skimming executable ..."
COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
time $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS

# Skim samples
while IFS=, read -r DIR SAMPLE LUMI WEIGHT1 WEIGHT2
do
    [[ $DIR =~ ^#.* ]] && continue
    
    echo ">>> Skim sample ${SAMPLE}"
    INPUT=${INPUT_DIR}${DIR}/

    if [[ $DIR == *"fake"* ]]; then
	OUTPUT=${OUTPUT_DIR}/${SAMPLE}_fake_Skim.root
    else
	OUTPUT=${OUTPUT_DIR}/${SAMPLE}_Skim.root
    fi
    echo "./skim $INPUT $OUTPUT $SAMPLE $LUMI $WEIGHT1 $WEIGHT2"
    ./skim $INPUT $OUTPUT $SAMPLE $LUMI $WEIGHT1 $WEIGHT2

done < skim.csv
