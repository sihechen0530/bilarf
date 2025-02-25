EXP_ARGS="batch_experiment_args.txt"
PARALLEL_NUM=4

cat ${EXP_ARGS} | xargs -I{} -P${PARALLEL_NUM} bash -c 'srun --partition=gpu --nodes=1 --gres=gpu:v100-sxm2:1 --ntasks=1 --time=04:00:00 /bin/bash -c "source ~/.bashrc; cd ~/documents/bilarf; source environment.sh; bash scripts/train_render.sh {}; bash scripts/eval.sh {}"'
