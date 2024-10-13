#!/bin/bash

GPUS=1
MODELS=(
    "meta-llama/Llama-3.1-8B-Instruct"
    # "meta-llama/Llama-3.1-70B-Instruct"
)
TEMPERATURE=0.01  # Not currently in use, defaults to 1
ENCODINGS=(
    # "base_64"
    # "gridencoding"
    # "keyboardcipher"
    # "leetspeak"
    # "rot13"
    # "upsidedown"
    # "wordreversal"
    # "wordsubstitution"
    "substitution_rot13_mapping"
    "substitution_rot13_mapping_sentence"
    "substitution_rot13_sentence"

    "substitution_reversal_mapping"
    "substitution_reversal_mapping_sentence"
    "substitution_reversal_sentence"

    "substitution_keyboard_mapping"
    "substitution_keyboard_mapping_sentence"
    "substitution_keyboard_sentence"

    "substitution_grid_mapping"
    "substitution_grid_mapping_sentence"
    "substitution_grid_sentence"
)

BASE_PATH="/home/zzhan645/jailbreak_cryptography/data/encrypted_variants"
OUTPUT_PATH="/home/zzhan645/jailbreak_cryptography/data/responses"
HUGGINGFACE_CACHE_DIR="/scratch/zzhan645/huggingface_cache"
HUGGINGFACE_TOKEN=$(cat src/keys/huggingface.key | tr -d '[:space:]')
INDEX=0


for model in "${MODELS[@]}"; do
    if [ "$model" == "mistralai/Mistral-7B-Instruct-v0.2" ]; then
        context_length=32768
    elif [ "$model" == "google/gemma-7b-it" ] || [ "$model" == "google/gemma-2b-it" ]; then
        context_length=8192
    else
        context_length=4096
    fi
    
    model_name=$(echo "${model}" | cut -d'/' -f2)
    
    # check if each file is exist
    for encoding in "${ENCODINGS[@]}"; do
        if [ ! -f "${BASE_PATH}/${encoding}.jsonl" ]; then
            echo "File ${BASE_PATH}/${encoding}.jsonl does not exist"
        fi
    done

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