#!/bin/bash

# Directory containing the files (change this)
DIR_PATH="/work/SuperResolutionData/sihe.chen/history/ns_process_data_result/video/sRGB"

# Output directory for the split files
OUTPUT_DIR="/home/chen.sihe1/documents/data/20250223_ns_process_data/sRGB"
mkdir -p "$OUTPUT_DIR"

# Number of file paths per output file
BATCH_SIZE=6

# Get list of all file paths in the directory
file_list=($(realpath $DIR_PATH/*))

# Total number of files
num_files=${#file_list[@]}
num_batches=$(( (num_files + BATCH_SIZE - 1) / BATCH_SIZE ))

# Split and save to different files
for ((i=0; i<num_batches; i++)); do
    start=$((i * BATCH_SIZE))
    end=$((start + BATCH_SIZE - 1))
    batch_file="$OUTPUT_DIR/batch_$((i+1)).txt"

    echo "${file_list[@]:start:BATCH_SIZE}" | tr ' ' '\n' > "$batch_file"
    echo "Saved: $batch_file"
done

echo "All batches saved in $OUTPUT_DIR"

