import json

MODEL = 'Meta-Llama-3.1-8B-Instruct'
ENCODING = 'wordsubstitution'
DATA_PATH = f'../../data/responses/{MODEL}/{ENCODING}.jsonl'
IDX = 27


with open(DATA_PATH, 'r') as f:
    data = [json.loads(ele) for ele in f.readlines()]


def print_format(title, content, no_dashes=50):
    print('-'*no_dashes)
    print(title)
    print('-'*no_dashes)
    print(content)


print_format('Question', data[IDX]['question'])
print_format('Prompt', data[IDX]['prompt'])
print_format('Response', data[IDX]['response'])