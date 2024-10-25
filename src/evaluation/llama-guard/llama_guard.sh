#!/bin/bash

CUDA_VISIBLE_DEVICES=0
MODEL_NAME='meta-llama/Llama-Guard-3-8B'
HUGGINGFACE_TOKEN=$(cat /data/data/dhanda/projects/jailbreak_cryptography/jailbreak_cryptography/src/keys/huggingface.key | tr -d '[:space:]')
HUGGINGFACE_CACHE='/data/data/dhanda/huggingface_cache'


ENCODINGS=(
    'advbench_50'
    'base_64'
    'gridencoding'
    'keyboardcipher'
    'leetspeak'
    'rot13'
    'upsidedown'
    'wordreversal'
    'wordsubstitution'
)
MODELS=(
    # 'gemini_1.5_flash'
    'gpt-4o'
    'Meta-Llama-3.1-8B-Instruct'
    # 'Meta-Llama-3.1-70B-Instruct'
)


for encoding in "${ENCODINGS[@]}"; do
    for model in "${MODELS[@]}"; do
        data_file_path="../../../data/responses/${model}/${encoding}.jsonl"
        save_path="../../../data/verified/${model}/${encoding}.jsonl"

        echo "================ Starting ${encoding} ${model} ================"
        CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES python llama_guard.py \
                            --model $MODEL_NAME \
                            --token $HUGGINGFACE_TOKEN \
                            --cache $HUGGINGFACE_CACHE \
                            --file $data_file_path \
                            --output $save_path
    done
done