EXP_ARGS="batch_experiment_args.txt"
PARALLEL_NUM=4

cat ${EXP_ARGS} | xargs -I{} -P${PARALLEL_NUM} bash -c 'srun --partition=gpu --nodes=1 --gres=gpu:1 --exclude=c[2160,2162-2175] --ntasks=1 --time=04:00:00 /bin/bash -c "source ~/.bashrc; cd ~/documents/bilarf; source environment.sh; bash scripts/train_render.sh {}; bash scripts/eval.sh {}"'
