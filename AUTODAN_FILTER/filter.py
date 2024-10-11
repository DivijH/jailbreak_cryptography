import json
import pprint

with open('llama3.1_8b_0_normal.json', 'r') as f:
    data = json.load(f)

with open('../../advbench_50.jsonl', 'r') as f:
    adv_data = [json.loads(line) for line in f]

for i in range(50):
    # pprint.pp(adv_data[i])
    # print('*'*100)
    # pprint.pp(data[str(i)])
    # exit()
    adv_data[i]['response'] = data[str(i)]['final_respond']
    with open('autodan.jsonl', 'a') as f:
        f.write(json.dumps(adv_data[i]) + '\n')