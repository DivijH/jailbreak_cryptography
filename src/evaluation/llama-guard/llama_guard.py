import argparse
from pathlib import Path
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

DEFAULT_CACHE_DIR = '/scratch/dhanda/huggingface_cache/'

class LlamaGuard:
    def __init__(self, model_name, huggingface_token, cache_dir=None):
        self.model_name = model_name
        self.huggingface_token = huggingface_token
        self.cache_dir = cache_dir
        self.device = 'cuda' if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            cache_dir = self.cache_dir,
            token = self.huggingface_token
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype = torch.bfloat16,
            device_map = self.device,
            cache_dir = self.cache_dir,
            token = self.huggingface_token
        )
    
    def evaluate(self, prompt):
        if type(prompt) == 'str':
            prompt = self.convert_prompt(prompt)
        input_ids = self.tokenizer.apply_chat_template(prompt, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids=input_ids, max_new_tokens=100, pad_token_id=0)
        prompt_len = input_ids.shape[-1]
        return self.tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True)

    def convert_prompt(self, orig_question, model_response=None, follow_up_question=None, final_model_response=None):
        prompt = []
        prompt.append({
            'role': 'user',
            'content': orig_question
        })
        if model_response is not None and model_response != '':
            prompt.append({
                'role': 'assistant',
                'content': model_response
            })
        if follow_up_question is not None and follow_up_question != '':
            prompt.append({
                'role': 'user',
                'content': follow_up_question
            })
        if final_model_response is not None and final_model_response != '':
            prompt.append({
                'role': 'assistant',
                'content': final_model_response
            })
        return prompt

    def evaluate_file(self, file_path):
        with open(file_path, 'r') as f:
            data = [json.loads(line) for line in f.readlines()]
        responses = []
        for ele in data:
            prompt = self.convert_prompt(
                ele['prompt'],
                ele['response_1'] if ele['final_response']==1 else ele['response_2'],
                ele['follow_up_question'],
                ele['final_response']
            )
            responses.append(self.evaluate(prompt))
        return responses

def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate prompts using LlamaGuard-7b')
    parser.add_argument('-m', '--model', type=str, help='Model name or path', required=True)
    parser.add_argument('-t', '--token', type=str, help='Huggingface API token', required=True)
    parser.add_argument('-c', '--cache', type=str, help='Cache directory', required=False, default=DEFAULT_CACHE_DIR)
    parser.add_argument('-f', '--file', type=str, help='JSONL File containing prompts', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file path', required=False)
    return parser.parse_args()

def save_responses(responses, file_path):
    with open(file_path, 'w') as f:
        for response in responses:
            f.write(json.dumps(response)+'\n')

if __name__ == '__main__':
    args = parse_args()

    llama_guard = LlamaGuard(
        model_name = args.model,
        huggingface_token = args.token,
        cache_dir = args.cache
    )

    responses = llama_guard.evaluate_file(args.file)
    save_responses(responses, args.output)