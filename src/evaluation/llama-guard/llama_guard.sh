#!/bin/bash

#SBATCH -N 1
#SBATCH -c 10
#SBATCH --mem 100G
#SBATCH -G a30:1
#SBATCH -t 0-04:00:00
#SBATCH -p htc
#SBATCH -q public
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH --mail-type=ALL
#SBATCH --export=NONE


module purge
module load mamba/latest
module load cuda-11.6.2-gcc-12.1.0
module load cudnn-8.0.4.30-10.1-gcc-12.1.0

nvidia-smi

source activate /scratch/dhanda/mamba_envs/word_substitution

MODEL_NAME='meta-llama/LlamaGuard-7b'
HUGGINGFACE_TOKEN=$(cat huggingface_token.key)
HUGGINGFACE_CACHE='/scratch/dhanda/huggingface_cache'

model_names=('ChatGPT' 'GPT4' 'Gemini')
substitution_techniques=('JQ' 'ES' 'AS' 'RS' 'ES+P')

for model_name in "${model_names[@]}"; do
    for substitution_technique in "${substitution_techniques[@]}"; do
        data_file_path="../../../data/advbench_variants/${substitution_technique}.jsonl"
        save_path="../../../responses/${model_name}/${substitution_technique}.jsonl"
        python llama_guard.py --model $MODEL_NAME \
                              --token $HUGGINGFACE_TOKEN \
                              --cache $HUGGINGFACE_CACHE \
                              --file $data_file_path \
                              --output $save_path
    done
done