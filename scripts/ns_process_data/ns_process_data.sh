INPUT_DIR=$1
OUTPUT_DIR=$2

for file in `realpath $INPUT_DIR/*.txt`; do
    instance_cmd="module load singularity; singularity exec -B /work/:/work/ -B /shared/:/shared/ --nv docker://martinchen0530/nerfstudio:v0.1 /bin/bash /home/chen.sihe1/documents/bilarf/scripts/ns_process_data/gpu_task.sh $file ${OUTPUT_DIR}"
    echo $instance_cmd
    srun --partition=gpu --nodes=1 --gres=gpu:1 --exclude=c[2160,2162-2175] --ntasks=1 --cpus-per-gpu=8 --time=04:00:00 /bin/bash -c "$instance_cmd"
done


for file in `realpath $INPUT_DIR/*.txt`; do
    instance_cmd="module load singularity; singularity exec -B /work/:/work/ -B /shared/:/shared/ docker://martinchen0530/nerfstudio:v0.1 /bin/bash /home/chen.sihe1/documents/bilarf/scripts/ns_process_data/cpu_task.sh $file ${OUTPUT_DIR}"
    srun --partition=short --nodes=1 --ntasks=1 --cpus-per-task=12 --time=04:00:00 /bin/bash -c "$instance_cmd"
done
