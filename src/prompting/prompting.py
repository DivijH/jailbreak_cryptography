import time
from tqdm import tqdm
import json
from pathlib import Path
import argparse
import google.generativeai as genai    # pip install -q -U google-generativeai
from openai import OpenAI              # pip install openai

ENCODING = 'gridencoding'
MODEL_NAME = 'gpt-4o'
INPUT_FILE_PATH = f'../../data/encrypted_variants_overdefense/{ENCODING}.jsonl'
# INPUT_FILE_PATH = f'../../data/cipherbench/cipherbench.jsonl'
OUTPUT_FILE_PATH = f'../../data/encrypted_variants_overdefense/responses/{MODEL_NAME}/{ENCODING}.jsonl'
API_KEY = open('../keys/openai.key').read().strip()
STARTING_INDEX = 0
TEMPERTATURE = 0
WAIT_TIME = 0


class CommercialModel:
    def __init__(self, model_name, api_key, wait_time):
        if 'gpt' in model_name:
            self.is_gpt = True
            self.is_gemini = False
            self.client = OpenAI(api_key=api_key)
        elif 'gemini' in model_name:
            self.is_gpt = False
            self.is_gemini = True
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            raise NotImplementedError(f'{model_name} is not supported')
        
        self.model_name = model_name
        self.input_tokens = 0
        self.output_tokens = 0
        self.wait_time = wait_time

    def _format_prompt(self, prompt):
        if self.is_gemini:
            return prompt
        elif self.is_gpt:
            return [{
                'role': 'user',
                'content': prompt
            }]
    
    def _prompt_model(self, prompt, temperature=0):
        if type(prompt) == str:
            prompt = self._format_prompt(prompt)

        if self.is_gemini:
            response = self.model.generate_content(
                prompt,
                generation_config = genai.GenerationConfig(
                    temperature = temperature
                )
            )
            self.input_tokens += response.usage_metadata.prompt_token_count
            self.output_tokens += response.usage_metadata.candidates_token_count
            try:
                return response.text, self.input_tokens, self.output_tokens
            except:
                return "NO RESPONSE", self.input_tokens, self.output_tokens

        elif self.is_gpt:
            completion = self.client.chat.completions.create(
                model = self.model_name,
                messages = prompt,
                temperature = temperature
            )
            self.input_tokens += completion.usage.prompt_tokens
            self.output_tokens += completion.usage.completion_tokens
            return completion.choices[0].message.content, self.input_tokens, self.output_tokens

    def _save_output(self, output_ele, output_path):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'a') as f:
            f.write(json.dumps(output_ele) + '\n')

    def prompt_dataset(self, dataset_path, output_path, index=0, temperature=0):
        with open(dataset_path, 'r') as f:
            data = [json.loads(ele) for ele in f.readlines()][index:]
        
        with tqdm(total=len(data)) as pbar:
            for ele in data:
                prompt = ele['prompt']
                # prompt = ele['question'] + '\n' + ele['priming_sentence']
                ele['response'], input_tokens, output_tokens = self._prompt_model(prompt, temperature)
                self._save_output(ele, output_path)
                pbar.set_description(f'Input Tokens: {input_tokens}, Output Tokens: {output_tokens}')
                time.sleep(self.wait_time)
                pbar.update(1)
    
    def prompt_cipherbench(self, dataset_path, output_path, index=0, temperature=0):
        with open(dataset_path, 'r') as f:
            data = [json.loads(ele) for ele in f.readlines()][index:]
        
        with tqdm(total=len(data)) as pbar:
            for ele in data:
                json_ele = {
                    "sentence": ele['sentence'],
                    "long": ele['long'],
                    "question": ele['question'],
                    "random": ele['random']
                }
                for key, value in ele.items():
                    if key not in ['sentence', 'long', 'question', 'random']:
                        json_ele[key], input_tokens, output_tokens = self._prompt_model(value, temperature)

                self._save_output(json_ele, output_path)
                pbar.set_description(f'Input Tokens: {input_tokens}, Output Tokens: {output_tokens}')
                time.sleep(self.wait_time)
                pbar.update(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model_name', type=str, required=False, default=MODEL_NAME, help='Model name')
    parser.add_argument('-f', '--file', type=str, required=False, default=INPUT_FILE_PATH, help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=False, default=OUTPUT_FILE_PATH, help='Output file path')
    parser.add_argument('-k', '--api_key', type=str, required=False, default=API_KEY, help='API key')
    parser.add_argument('-i', '--index', type=int, required=False, default=STARTING_INDEX, help='Starting zero-index for evaluation')
    parser.add_argument('-t', '--temperature', type=float, required=False, default=TEMPERTATURE, help='Temperature for generation')
    parser.add_argument('-w', '--wait_time', type=int, required=False, default=WAIT_TIME, help='Wait time between prompts')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    model = CommercialModel(args.model_name, args.api_key, args.wait_time)
    model.prompt_dataset(args.file, args.output, args.index, args.temperature)
    # model.prompt_cipherbench(args.file, args.output, args.index, args.temperature)