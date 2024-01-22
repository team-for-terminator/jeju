1. Dataset_roboflow.py
- Segmentation 및 Augmentation 을 통해 총 105장의 이미지데이터를 불러와 폴더에 저장
2. Predict_yolo8x-seg.py
- 학습이 완료된 모델을 가지고 475장의 png 이미지를 segmentation
3. Train_yolov8-seg.py
- yolov8 의 segmentation 모델 중 크기가 가장 큰 x 모델로 학습 진행
