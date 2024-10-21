import os
import json
import pprint

DATA_PATH = '../../data/cipherbench/'
MODELS = [
    'gpt-4o',
    'gemini_1.5_flash'
]

LONG = '*' # True, False, *
QUESTION = '*' # True, False, *
RANDOM = '*' # True, False, *

if __name__ == '__main__':
    for model in MODELS:
        data_path = os.path.join(DATA_PATH, model+'.jsonl')
        metrics = {}

        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f.readlines()]
        
        for instance in data:
            if (
                (LONG == '*' or instance['long'] == eval(LONG)) and
                (QUESTION == '*' or instance['question'] == eval(QUESTION)) and
                (RANDOM == '*' or instance['random'] == eval(RANDOM))
            ):
                for key, value in instance.items():
                    if key not in ['sentence', 'long', 'question', 'random']:
                        is_correct = instance['sentence'][:-1] in value
                        if key not in metrics:
                            metrics[key] = {
                                'total': 1,
                                'correct': 1 if is_correct else 0
                            }
                        else:
                            metrics[key]['total'] += 1
                            metrics[key]['correct'] += 1 if is_correct else 0

        print('*'*100)
        print(f'Model: {model}')
        print('*'*100)
        pprint.pprint(metrics)
        print('Correct:', sum(item['correct'] for item in metrics.values()))
        print('Total:', sum(item['total'] for item in metrics.values()))
    print('*'*100)