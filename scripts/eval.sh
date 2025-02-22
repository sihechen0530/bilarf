#!/bin/bash

# CONFIG=configs/360.gin  # For 360 scenes.
CONFIG=$1  # For forward-facing scenes.
# SCENE=strat
EXPERIMENT=$3  # Checkpoints, results, and logs will be saved to exp/${EXPERIMENT}.
# DATA_ROOT=/pathto/datasets/bilarf_data/testscenes/
DATA_DIR=$2


# Evaluation
python eval.py --gin_configs=${CONFIG} \
    --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
    --gin_bindings="Config.exp_name = '${EXPERIMENT}'"
