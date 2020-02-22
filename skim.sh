#!/bin/bash

set -e

INPUT_DIR="/media/shoh/02A1ACF427292FC0/latinov6"
OUTPUT_DIR=$1
# Sanitize input path, XRootD breaks if we double accidentally a slash
#if [ "${INPUT_DIR: -1}" = "/" ];
#then
#    INPUT_DIR=${INPUT_DIR::-1}
#fi

# Compile executable
echo ">>> Compile skimming executable ..."
COMPILER=$(root-config --cxx)
FLAGS=$(root-config --cflags --libs)
time $COMPILER -g -O3 -Wall -Wextra -Wpedantic -o skim skim.cxx $FLAGS

# Skim samples
while IFS=, read -r DIR SAMPLE LUMI WEIGHT1 WEIGHT2
do
    echo ">>> Skim sample ${SAMPLE}"
    INPUT=${INPUT_DIR}${DIR}/
    OUTPUT=${OUTPUT_DIR}/${SAMPLE}_Skim.root
    echo "./skim $INPUT $OUTPUT $SAMPLE $LUMI $WEIGHT1 $WEIGHT2"
    ./skim $INPUT $OUTPUT $SAMPLE $LUMI $WEIGHT1 $WEIGHT2
#done < test.csv
done < skim.csv
