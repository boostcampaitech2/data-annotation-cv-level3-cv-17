#annotation_check.py

import cv2
import os
import json
import numpy as np

img_path = 'ICDAR17_Korean/images/'             #
json_path = 'ICDAR17_Korean/ufo/train.json'     # 자신의 경로로 바꿔주세요!
# annotation data 읽기
with open(json_path, 'r') as f:
    json_data = json.load(f)
img_list = list(json_data['images'].keys())
# 이상한 이미지 목록 있다면 불러오기
Strange_img_set = set()
if os.path.exists('./StrangeImgList.txt'):
    with open('StrangeImgList.txt', 'r') as f:
        read_data = f.readline()
        if len(read_data) >= 1: # 저장된 요소가 있다면
            read_data = read_data.split(',')
            print('exist_datas', read_data) # 기존 데이터 출력
            Strange_img_set = set(map(int, read_data))\

end_idx = 535

# 필요에 따른 수정 부분
current_idx = 0 # 시작 인덱스
img_size = (800, 800) # 편의에 맞게 이미지 크기 조절
img_save = True # 이미지 저장 여부

if img_save:
    if not os.path.exists("./StrangeImage"):
        os.mkdir("./StrangeImage")

# txt 파일 업데이트
def save_txt(img_set):
    write_elements = ''
    if len(img_set) >= 1: # 저장할 요소가 있다면
        Strange_img_list = sorted(list(img_set)) # 정렬후, 저장
        write_elements = list(map(str, Strange_img_list))
        write_elements = ",".join(write_elements)
        print('save_datas', write_elements)
    with open('StrangeImgList.txt', 'w') as f:
        f.write(write_elements)

color = (100,255,0)

while True:
    current_img = img_list[current_idx]
    img = cv2.imread(img_path+current_img)
    words = json_data['images'][current_img]['words']

    # 글자 도형 그리기
    for word in words.values():
        points = np.array(word['points'], dtype=np.int32)
        points = points.reshape((-1,1,2))
        img = cv2.polylines(img, [points], True, color, 2)

    img = cv2.resize(img, img_size, interpolation = cv2.INTER_AREA)
    cv2.imshow("win", img)
    ret = cv2.waitKey(0)
    if (ret == 102 or ret == 70) and current_idx != end_idx: # 'F' or 'f' 입력한 경우, Foward
        current_idx += 1
        print('current_idx', current_idx)
    elif (ret == 98 or ret == 66) and current_idx != 0: # 'B' or 'b' 입력한 경우, Backward
        current_idx -= 1
        print('current_idx', current_idx)
    elif ret == 83 or ret == 115: # 'S' or 's' 입력한 경우, Save
        if img_save: # 이미지 저장
            if not os.path.exists("./StrangeImage/{}.jpg".format(current_img)):
                cv2.imwrite("./StrangeImage/{}.jpg".format(current_img), img)
        Strange_img_set.add(current_img)
        save_txt(Strange_img_set) # 텍스트 파일 업데이트
        print('add', current_img)
    elif ret == 68 or ret == 100: # 'D' or 'd' 입력한 경우, Delete
        try:
            Strange_img_set.remove(current_img)
            print('del', current_img)
            save_txt(Strange_img_set) # 텍스트 파일 업데이트
        except:
            pass
        if img_save: # 이미지 제거
            if os.path.exists("./StrangeImage/{}.jpg".format(current_img)):
                os.remove("./StrangeImage/{}.jpg".format(current_img))
    elif ret == 27: # 'ESC' 입력시 종료
        break