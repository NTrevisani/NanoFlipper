#!/bin/bash

# 35.87
# 41.53
# 59.74

HISTOGRAMS=$1
OUTPUT=$2

YEAR=`echo ${HISTOGRAMS} | awk -F "/" '{ print $(NF-1) }'`

if [[ "$YEAR" == "2016" ]]; then
    SCALE=35.87
elif [[ "$YEAR" == "2017" ]]; then
    SCALE=41.53
elif [[ "$YEAR" == "2018" ]]; then
    SCALE=59.74
fi

if [ ! -e ${OUTPUT}/${YEAR} ]; then
    mkdir -p ${OUTPUT}/${YEAR}/
fi

echo "python plot.py $HISTOGRAMS ${OUTPUT}/${YEAR}/ $SCALE"
python plot.py $HISTOGRAMS ${OUTPUT}/${YEAR}/ $SCALE
