#!/bin/bash

source environment.sh
CONFIG="$1" # For 360 scenes.
# CONFIG=configs/llff.gin  # For forward-facing scenes.
DATA_DIR="$2"
EXPERIMENT="$3"  # Checkpoints, results, logs will be saved to exp/${EXPERIMENT}.

# for render log to successfully generate
mkdir -p exp/$EXPERIMENT

CONVERT_FROM="$4"
CONVERT_TO="$5"
MAX_STEPS="$6"
CCM="$7"

# Render testing views
python render.py --gin_configs=${CONFIG} \
    --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
    --gin_bindings="Config.exp_name = '${EXPERIMENT}'" \
    --gin_bindings="Config.convert_from = '${CONVERT_FROM}'" \
    --gin_bindings="Config.convert_to = '${CONVERT_TO}'" \
    --gin_bindings="Config.ccm = '${CCM}'"


# Render path
python render.py --gin_configs=${CONFIG} \
    --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
    --gin_bindings="Config.exp_name = '${EXPERIMENT}'" \
    --gin_bindings="Config.render_path = True" \
    --gin_bindings="Config.render_path_frames = 120" \
    --gin_bindings="Config.render_video_fps = 60" \
    --gin_bindings="Config.convert_from = '${CONVERT_FROM}'" \
    --gin_bindings="Config.convert_to = '${CONVERT_TO}'" \
    --gin_bindings="Config.ccm = '${CCM}'"

python eval.py --gin_configs=${CONFIG} \
    --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
    --gin_bindings="Config.exp_name = '${EXPERIMENT}'" \
    --gin_bindings="Config.convert_from = '${CONVERT_FROM}'" \
    --gin_bindings="Config.convert_to = '${CONVERT_TO}'"

# # Render training views
# # Comment the last line to render training views without
# # per-view bilateral grids applied.
# python render.py --gin_configs=${CONFIG} \
#     --gin_bindings="Config.data_dir = '${DATA_DIR}'" \
#     --gin_bindings="Config.exp_name = '${EXPERIMENT}'" \
#     --gin_bindings="Config.render_train = True" \
#     --gin_bindings="Model.bilateral_grid = True"
