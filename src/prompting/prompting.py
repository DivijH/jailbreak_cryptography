import time
from tqdm import tqdm
import json
from pathlib import Path
import argparse
import google.generativeai as genai    # pip install -q -U google-generativeai
import openai                          # pip install openai

GEMINI_MODEL_NAME = 'gemini-pro'
GPT4_MODEL_NAME = 'gpt-4-0125-preview'
GPT3_MODEL_NAME = 'gpt-3.5-turbo-0125'

WAIT_TIME = 30

def get_response(messages, model_name, model=None, temp=0.0):
    if model_name == GEMINI_MODEL_NAME:
        if model.count_tokens(messages).total_tokens > 30_720:
            return "NO RESPONSE"
        response = model.generate_content(
            messages,
            generation_config = genai.types.GenerationConfig(
                candidate_count = 1,
                temperature = temp,
            )
        )
        try:
            return response.text
        except:
            return "NO RESPONSE"
    
    elif model_name == GPT4_MODEL_NAME or model_name == GPT3_MODEL_NAME:
        response = openai.ChatCompletion.create(
            model = model_name,
            messages = messages,
            temperature = temp
        )
        return response.choices[0].message.content
    
    else:
        raise Exception(f'{model_name} is not supported')

def write_response(json_ele, file_path):
    with open(file_path, 'a+') as f:
        f.write(json.dumps(json_ele)+'\n')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, required=True, help='Model name')
    parser.add_argument('-f', '--file', type=str, required=True, help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file path')
    parser.add_argument('-k', '--model_api_key', type=str, required=True, help='API key')
    parser.add_argument('-i', '--index', type=int, required=False, help='Starting zero-index for evaluation')
    parser.add_argument('-t', '--temperature', type=float, required=False, default=0.0, help='Temperature for generation')
    return parser.parse_args()

def create_prompt(ele, model_name):
    if ele['response_1'] == '':
        return [{"role": "user", "parts": [ele['prompt']]}] if model_name == GEMINI_MODEL_NAME else [{"role": "user", "content": ele['prompt']}]

    if ele['follow_up_question'] == '':
        return None

    if ele['selected_response'] == 1:
        selected_response = ele['response_1']
    elif ele['selected_response'] == 2:
        selected_response = ele['response_2']
    else:
        raise Exception('Missing evaluation :(')

    if model_name == GEMINI_MODEL_NAME:
        chat_history = [
            {"role": "user", "parts": [ele['prompt']]},
            {"role": "model", "parts": [selected_response]},
            {"role": "user", "parts": [ele['follow_up_question']]}
        ]
    elif model_name == GPT4_MODEL_NAME or model_name == GPT3_MODEL_NAME:
        chat_history = [
            {'role': 'user', 'content': ele['prompt']},
            {'role': 'assistant', 'content': selected_response},
            {'role': 'user', 'content': ele['follow_up_question']}
        ]
    
    return chat_history

if __name__ == '__main__':
    # Getting arguments
    args = parse_args()

    # Loading the Gemini-Pro and OpenAI API instances
    if args.model.lower()=='gemini-pro' or args.model.lower()=='gemini':
        genai.configure(api_key=args.model_api_key)
        model_name = GEMINI_MODEL_NAME
        model = genai.GenerativeModel(model_name)
    elif args.model.lower()=='gpt4' or args.model.lower()=='gpt-4':
        with open('openai.api.key') as f:
            openai.api_key = f.read()
        model_name = GPT4_MODEL_NAME
    elif args.model.lower()=='gpt3' or args.model.lower()=='gpt-3':
        with open('openai.api.key') as f:
            openai.api_key = f.read()
        model_name = GPT3_MODEL_NAME
    else:
        raise Exception(f'{args.model} is not supported')


    # Reading the instance
    with open(args.file, 'r') as f:
        if args.index:
            data = [json.loads(jline) for jline in f.readlines()][args.index:]
        else:
            data = [json.loads(jline) for jline in f.readlines()]
    
    # Creating the directory where the files will be saved
    dir_path = '/'.join(args.output.split('/')[:-1])
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    # Prompting the model
    with tqdm(total=len(data)*2) as pbar:
        for idx, ele in enumerate(data):
            for response_num in range(1, 3):
                prompt = create_prompt(ele, model_name)
                if prompt is None:
                    response = ''
                else:
                    if model_name == GEMINI_MODEL_NAME:
                        response = get_response(
                            text = prompt,
                            model_name = model_name,
                            model = model,
                            temp = args.temperature
                        )
                    elif model_name == GPT4_MODEL_NAME or model_name == GPT3_MODEL_NAME:
                        response = get_response(
                            text = prompt,
                            model_name = model_name,
                            temp = args.temperature
                        )
                ele[f'response_{response_num}'] = response
                write_response(ele, args.output)
                time.sleep(WAIT_TIME)
                pbar.update(1)