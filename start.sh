#!/usr/bin/env bash

set -e

if [[ $# -eq 0 ]] ; then
    echo "Please give one argument to the script: <input_filename> <arguments>."
    echo "Example is: ./$0 coinbaseUSD.csv --use_quantiles"
    exit 0
fi

WORK_DIR=~/deep-learning-bitcoin


if [ -d "$WORK_DIR" ]; then
    echo "Folder already exists."
    source ${WORK_DIR}/venv/bin/activate
else
    mkdir -p ${WORK_DIR}
    virtualenv -p python3.6 ${WORK_DIR}/venv
    source ${WORK_DIR}/venv/bin/activate
    pip install -r requirements.txt
fi

INPUT_FILENAME=$1
RESAMPLE_FREQUENCY=5Min

INPUT_FILENAME_WO_EXT=$(basename ${INPUT_FILENAME} .csv)
RESAMPLE_FILENAME=${WORK_DIR}/${INPUT_FILENAME_WO_EXT}_$RESAMPLE_FREQUENCY.csv


python cli.py --action tick_count --input_filename ${INPUT_FILENAME}

python cli.py --action resample --input_filename ${INPUT_FILENAME} --resample_frequency ${RESAMPLE_FREQUENCY} --output_filename ${RESAMPLE_FILENAME}

python cli.py --action generate_plots --input_filename ${RESAMPLE_FILENAME} --output_dir ${WORK_DIR}/plots/