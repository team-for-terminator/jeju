import os
HOME = os.getcwd()
from ultralytics import YOLO

# 사전 학습된 yolo 모델을 불러옵니다. 
# 저희는 segmentation 이 가능하고, 가장 큰 모델을 사용하였기에 yolov8x-seg.pt 모델을 불러옵니다.
model = YOLO('yolov8x-seg.pt')
# GPU 사용을 위한 cuda 할당
model.to('cuda')
# epochs : 학습 횟수는 정확도의 향상이 없다면 자연스레 종료되니 높은 값으로 지정
# imgsz : 이미지 크기는 1000x1000 으로 입력
# data : roboflow 에서 받은 데이터 폴더 속 yaml 파일 경로
# 학습 결과 학습된 모델 파일이 저장됩니다.
model.train(data='./project-segmentation-2-1/data.yaml', epochs=10000, imgsz=1000)
