#!/bin/bash

GPUS=0,1
MODELS=(
    "meta-llama/Meta-Llama-3.1-8B-Instruct"
    # "meta-llama/Meta-Llama-3.1-70B-Instruct"
)
TEMPERATURE=0.01  # Not currently in use, defaults to 1
ENCODINGS=(
    # "base_64"
    # "gridencoding"
    # "keyboardcipher"
    # "rot13"
    # "upsidedown"
    # "wordreversal"
    # "wordsubstitution"
    "substitution_rot13"
)

BASE_PATH="data/encrypted_variants"
OUTPUT_PATH="data/responses"
HUGGINGFACE_CACHE_DIR="huggingface_cache"
HUGGINGFACE_TOKEN=$(cat src/keys/huggingface.key | tr -d '[:space:]')
INDEX=509


for model in "${MODELS[@]}"; do
    if [ "$model" == "mistralai/Mistral-7B-Instruct-v0.2" ]; then
        context_length=32768
    elif [ "$model" == "google/gemma-7b-it" ] || [ "$model" == "google/gemma-2b-it" ]; then
        context_length=8192
    else
        context_length=4096
    fi
    
    model_name=$(echo "${model}" | cut -d'/' -f2)
    
    for encoding in "${ENCODINGS[@]}"; do
        echo "Starting running ${model_name} -- ${encoding} -- ${GPUS}"
        CUDA_VISIBLE_DEVICES=${GPUS} python src/prompting/huggingface_inference.py \
                -m "${model}" \
                -f "${BASE_PATH}/${encoding}.jsonl" \
                -o "${OUTPUT_PATH}/${model_name}/${encoding}.jsonl" \
                -c "${context_length}" \
                -t "${TEMPERATURE}" \
                -d "${HUGGINGFACE_CACHE_DIR}" \
                -k "${HUGGINGFACE_TOKEN}" \
                -i "${INDEX}"
    done
done