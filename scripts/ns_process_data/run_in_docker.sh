export PATH=/shared/centos7/cuda/11.8/bin:$PATH

INPUT_FILE=$1
PARALLEL_NUM=$(wc -l $INPUT_FILE | cut -d " " -f1)
# base of all videos
OUTPUT_DIR=$2

# command_file=$1.gpu
# rm $command_file

# for path in `cat $INPUT_FILE`; do
#     video_name=$(basename $path .MP4)
#     echo $video_name
#     output_dir="$OUTPUT_DIR/$video_name"
#     tmp_dir="/dev/shm/$video_name"
#     log_path="$output_dir/log"
#     echo "mkdir -p $output_dir; rm -rf $output_dir/*; rm -rf $tmp_dir; ns-process-data video --data $path --output-dir $tmp_dir >> $log_path 2>&1; mv $tmp_dir/* $output_dir/" >> $command_file
# done


command_file=$1.cpu
rm $command_file

for path in `cat $INPUT_FILE`; do
    video_name=$(basename $path .MP4)
    echo $video_name
    output_dir="$OUTPUT_DIR/$video_name"
    log_path="$output_dir/log"
    # cpu add --verbose
    echo "ns-process-data video --data $path --output-dir $output_dir --verbose >> $log_path 2>&1; cd $output_dir; ln -s colmap/* ." >> $command_file
done

cat $command_file | xargs -I{} -P$PARALLEL_NUM bash -c "{}"
