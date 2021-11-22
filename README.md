# 글자 검출 대회

## Project 개요
스마트폰으로 카드를 결제하거나, 카메라로 카드를 인식할 경우 자동으로 카드 번호가 입력되는 경우가 있습니다. 또 주차장에 들어가면 차량 번호가 자동으로 인식되는 경우도 흔히 있습니다. 이처럼 **OCR (Optimal Character Recognition)** 기술은 사람이 직접 쓰거나 이미지 속에 있는 문자를 얻은 다음 이를 컴퓨터가 인식할 수 있도록 하는 기술로, 컴퓨터 비전 분야에서 현재 널리 쓰이는 대표적인 기술 중 하나입니다.

OCR task는 글자 검출 (text detection), 글자 인식 (text recognition), 정렬기 (Serializer) 등의 모듈로 이루어져 있습니다. 
본 대회는 **데이터를 구성하고 활용**하는 방법에 집중하는 것을 장려하는 취지에서, 제공되는 베이스 코드 중 **모델과 관련한 부분을 변경하는 것이 금지**되어 있습니다. 

+ Input : 글자가 포함된 전체 이미지
+ Output : bbox 좌표가 포함된 UFO Format

## Data
성능 향상을 위해 공공 외부 데이터셋 사용 
시각화를 진행하여 Annotation이 올바르지 않은 데이터 제거
+ **ICDAR17_Korean**
    + [ICDAR17-MLT](https://rrc.cvc.uab.es/?ch=8) 데이터셋에서 언어가 한글인 샘플들만 모아서 재구성
    + 536장 
+  **추가 Annotation 실습 데이터**
    +  대회 참여자들과 함께 제작한 공통 데이터 셋
    + 1238장
+ **외부 데이터**
    + **[ICDAR19_ArT](https://rrc.cvc.uab.es/?ch=14)**
        + 4345장
    + **[야외 실제 촬영 한글 이미지](https://aihub.or.kr/aidata/33985)**
        + 일상에서 접할 수 있는 다양한 한글 이미지(간판, 책표지)를 이용하여 다양한 OCR 솔루션에 사용될 수 있는 text-in-the-wild 이미지 데이터
        + 2699장

## UFO(Upstage Format for OCR) Structure
- **ids**: paragraph, image, character 레벨 각각에서 모두 id 넘버를 매김
- **points**: 각 라벨의 위치 좌표. 글자를 읽는 방향의 왼쪽 위에서부터 시계방향으로 x, y좌표를 nested list 형태로 기록
- **language**: 사용된 언어
- **tags**: 성능에 영향을 주지만 별도로 기록하기 애매한 요소를 사전에 정의한 태그로 표시
- **confidence**: OCR모델이 예측한 pesudo-label의 경우 confidence score를 할께 표시
```
File Name
    ├── img_h
    ├── img_w
    └── words
        ├── points
        ├── transcription
        ├── language
        ├── illegibillity
        ├── orientation
        └── word_tags
```

## 평가 방법
+ **F1-score** 
    + Recall과 Precision의 **조화평균**
+ **Box의 정답 기준**
    + Area Recall **0.8 이상** and Area Precision **0.4 이상**
    + one-to-many match에 한해 **0.8**의 **penalty** 적용
+ **모든 이미지의 Recall, Precision 값 평균으로 F1-Score 측정**
## Baseline Structure
```
├─ code
│  │  model.py
│  │  loss.py
│  │  train.py
│  │  inference.py
│  │  dataset.py
│  │  detect.py
│  │  deteval.py
│  │  east_dataset.py
│  │  convert_mlt.py
│  │  requirements.txt
└─ input
    └─ data
        └─ ICDAR2017_Korean
            └─ ufo
            │    └─ train.json
            └─ images
                 │ img_1001.jpg
                 │ img_1002.jpg
                 │ img_1003.jpg
                 │ ...
                 └ img_4700.jpg
```

## Tools
```
├─ tools
│  ├─ ann_check_ocr      # 데이터 검수 툴 
│  │  │  ann_check_ocr.py
│  │  │  my_path.py
│  └─ make_json          # json 만드는 툴
│     │  StrangeImgList.txt
│     │  annotation.json
│     │  make_json.ipynb
│     │  train.json
└─ data_augmentation.ipynb 
```

### **데이터 검수 툴**
+ 이미지와 Bbox 시각화
+ 문제가 있는 데이터 삭제
+ F,B 키로 이미지를 조회할 수 있고 S,D로 저장 삭제 가능
+ 로컬에서 작업가능하며 쉽고 빠르게 검수 가능
### **json 만드는 툴**
+ 새로운 데이터 추가
+ 데이터 filtering

## 🏆Result
### Private Score
![](https://i.imgur.com/inF0jQ9.png)

### Public Score
![](https://i.imgur.com/tOsQFPI.png) 
> 💪 3 up!

<br/>
  
---
## Members

|   <div align="center">김주영 </div>	|  <div align="center">오현세 </div> 	|  <div align="center">채유리 </div> 	|  <div align="center">배상우 </div> 	|  <div align="center">최세화 </div>  | <div align="center">송정현 </div> |
|---	|---	|---	|---	|---	|---	|
| <img src="https://avatars.githubusercontent.com/u/61103343?s=120&v=4" alt="0" width="200"/>	|  <img src="https://avatars.githubusercontent.com/u/79178335?s=120&v=4" alt="1" width="200"/> 	|  <img src="https://avatars.githubusercontent.com/u/78344298?s=120&v=4" alt="1" width="200"/> 	|   <img src="https://avatars.githubusercontent.com/u/42166742?s=120&v=4" alt="1" width="200"/>	| <img src="https://avatars.githubusercontent.com/u/43446451?s=120&v=4" alt="1" width="200"/> | <img src="https://avatars.githubusercontent.com/u/68193636?v=4" alt="1" width="200"/> |
|   <div align="center">[Github](https://github.com/JadeKim042386)</div>	|   <div align="center">[Github](https://github.com/5Hyeons)</div>	|   <div align="center">[Github](https://github.com/yoorichae)</div>	|   <div align="center">[Github](https://github.com/wSangbae)</div>	| <div align="center">[Github](https://github.com/choisaywhy)</div> | <div align="center">[Github](https://github.com/pirate-turtle)</div>|
