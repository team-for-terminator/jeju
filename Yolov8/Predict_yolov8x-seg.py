from ultralytics import YOLO
import cv2
from PIL import Image

# 학습시킨 yolov8x-seg 모델의 결과 파일을 불러옵니다.
model = YOLO(f'./best_x.pt')

# segmentation 의 경우 지정한 제주도 1조각에 대한 1000x1000 이미지 이므로 475 장의 이미지를 전부 학습된 모델로 segmentation 해줍니다.
for i in range(475):
    results = model.predict(f'./{i}.png',conf=0.25,classes=[4,5,6])	
    # conf 의 경우 labeling과는 달리 segmentation 의 특성상 높지 않게 하였습니다.

    for r in results:
        # 모델로 예측한 결과에서 시각화하는 과정에서 labeling 한 정보를 제외한 segmentation 정보만 저장하도록합니다.
        im_array = r.plot(boxes=False)  
        # 결과를 이미지로 저장하기 위한 변환 과정
        im = Image.fromarray(im_array[..., ::-1]) 
        # 이미지 저장 
        im.save(f'{i}.png')  
    
