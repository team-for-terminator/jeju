from roboflow import Roboflow
rf = Roboflow(api_key="기록의미학 roboflow api")
project = rf.workspace("ai-hssax").project("project-segmentation-2")
dataset = project.version(1).download("yolov8")
# 위의 과정을 통해 roboflow 에서 segmentation 및 augmentation 한 데이터를 가져옵니다.
# 폴더의 이름은 project-segmentation-2 입니다.