import json
import os

json_path = 'annotation.json'
json_path2 = 'train.json'

with open(json_path, 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

with open(json_path2, 'r', encoding='UTF-8') as f:
    json_data2 = json.load(f)

if os.path.exists('StrangeImgList.txt'):
    with open('StrangeImgList.txt', 'r', encoding='UTF-8') as f:
        strange_data = f.readline()
        if len(strange_data) >= 1: # 저장된 요소가 있다면
            read_data = strange_data.split(',')

print(len(json_data['images']))
for fname in read_data:
    try:
        json_data['images'].pop(fname)
    except:
        pass
print(len(json_data['images']))

json_data['images'].update(json_data2['images'])
print(len(json_data['images']))

with open('new_ann.json', 'w', encoding='UTF-8') as f:
    json.dump(json_data,f,indent=2)