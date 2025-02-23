#!/bin/bash

# CONFIG=configs/360.gin  # For 360 scenes.
CONFIG=$1  # For forward-facing scenes.
# SCENE=strat
EXPERIMENT=$3  # Checkpoints, results, and logs will be saved to exp/${EXPERIMENT}.
# DATA_ROOT=/pathto/datasets/bilarf_data/testscenes/
DATA_DIR=$2
CONVERT_FROM="$4"
CONVERT_TO="$5"
NORMALIZE="$6"


# Evaluation
python eval.py --gin_configs=${CONFIG} \
    --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
    --gin_bindings="Config.exp_name = '${EXPERIMENT}'" \
    --gin_bindings="Config.convert_from = '${CONVERT_FROM}'" \
    --gin_bindings="Config.convert_to = '${CONVERT_TO}'" \
    --gin_bindings="Config.normalize = ${NORMALIZE}"
