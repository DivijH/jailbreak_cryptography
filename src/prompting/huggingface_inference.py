from tqdm import tqdm
import json
from pathlib import Path
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = 'meta-llama/Meta-Llama-3.1-8B-Instruct'
CONTEXT_LENGTH = 4096
TEMPERATURE = 0.1 # Not currently in use, defaults to 1
ENCODING = 'wordsubstitution'
INDEX = 0

FILE_PATH = f'../../data/encrypted_variants/{ENCODING}.jsonl'
# FILE_PATH = f'../../data/{ENCODING}.jsonl'
OUTPUT_PATH = f'../../data/responses/{MODEL_NAME.split("/")[-1]}/{ENCODING}.jsonl'
HUGGINGFACE_CACHE_DIR = '/data/data/dhanda/huggingface_cache'
HUGGINGFACE_TOKEN = open('../keys/huggingface.key').read()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, default=MODEL_NAME, required=False, help='Model name')
    parser.add_argument('-f', '--file', type=str, default=FILE_PATH, required=False, help='Input file path')
    parser.add_argument('-o', '--output', type=str, default=OUTPUT_PATH, required=False, help='Output file path')
    parser.add_argument('-c', '--context', type=int, default=CONTEXT_LENGTH, required=False, help='Context length')
    parser.add_argument('-t', '--temperature', type=str, default=TEMPERATURE, required=False, help='Temperature of the model')
    parser.add_argument('-d', '--huggingface_cache_dir', type=str, default=HUGGINGFACE_CACHE_DIR, required=False, help='Huggingface cache directory')
    parser.add_argument('-k', '--huggingface_token', type=str, default=HUGGINGFACE_TOKEN, required=False, help='Huggingface token key')
    parser.add_argument('-i', '--index', type=int, default=INDEX, required=False, help='Starting zero-index for evaluation')
    return parser.parse_args()


class HuggingInference:
    def __init__(
            self,
            cache_dir,
            token,
            model_name_or_path,
            tokenizer_name = None            
    ):
        self.cache_dir = cache_dir
        self.token = token
        self.model_name_or_path = model_name_or_path
        self.tokenizer_name = tokenizer_name if tokenizer_name else model_name_or_path
        self._load_tokenizer()
        self._load_model()
    
    def _load_tokenizer(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.tokenizer_name,
            cache_dir = self.cache_dir,
            token = self.token,
            trust_remote_code = True
        )
        if self.tokenizer_name.split('/')[0] == 'meta-llama':
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
    
    def _load_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path,
            device_map = 'auto',
            cache_dir = self.cache_dir,
            token = self.token,
            trust_remote_code = True
        )
    
    def get_response(self, prompt, context_length, temperature):
        input_ids = self.tokenizer(
            prompt,
            return_tensors = 'pt',
            return_token_type_ids = False
        )
        if input_ids['attention_mask'].shape[1] > context_length:
            return 'NO RESPONSE'
        
        with torch.no_grad():
            return self.tokenizer.decode(
                self.model.generate(
                    **input_ids.to('cuda'),
                    max_new_tokens = 1_000,
                    # temperature = temperature,
                )[0],
                skip_special_tokens=True
            )[len(prompt):]
                
    def write_response(self, json_ele, file_path):
        with open(file_path, 'a+') as f:
            f.write(json.dumps(json_ele)+'\n')
    
    def prompt_dataset(self, input_file_path, output_file_path, idx=0, context_length=4096, temperature=0):
        with open(input_file_path, 'r') as f:
            data = [json.loads(jline) for jline in f.readlines()][idx:]
            
        dir_path = '/'.join(output_file_path.split('/')[:-1])
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        with tqdm(total=len(data)) as pbar:
            for idx, ele in enumerate(data):
                response = self.get_response(ele['prompt'], context_length, temperature)
                # response = self.get_response(ele['question'] + '\n' + ele['priming_sentence'], context_length, temperature)
                ele['response'] = response
                self.write_response(ele, output_file_path)
                pbar.update(1)

if __name__ == '__main__':
    args = parse_args()
    
    huggingface_instance = HuggingInference(
        cache_dir = args.huggingface_cache_dir,
        token = args.huggingface_token,
        model_name_or_path = args.model
    )
    
    huggingface_instance.prompt_dataset(
        input_file_path = args.file,
        output_file_path = args.output,
        idx = args.index,
        context_length = args.context,
        temperature = args.temperature
    )