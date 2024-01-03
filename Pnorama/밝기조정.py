from PIL import Image, ImageEnhance
import numpy as np

# 밝은 영역이 존재하는 이미지 불러오기
image_path = './bright.png'
image = Image.open(image_path)

# 이미지를 numpy 배열로 변환
image_np = np.array(image)

# 밝기가 지나치게 높은 세로 영역을 찾기 위해 각 열의 밝기를 계산
column_brightness = image_np.mean(axis=(0, 2))

# 평균과 표준편차를 기반으로 밝은 열을 식별
mean_brightness = column_brightness.mean()
std_brightness = column_brightness.std()
bright_columns = np.where(column_brightness > mean_brightness + std_brightness)[0]

# 밝기를 조정하는 함수를 정의
def adjust_brightness(img_np, factor):
    enhancer = ImageEnhance.Brightness(Image.fromarray(img_np))
    return enhancer.enhance(factor)

# 밝은 열의 밝기를 조정
for column in bright_columns:
    image_np[:, column, :3] = adjust_brightness(image_np[:, column, :3], 0.5)  

# 알파 채널이 있는지 확인하고 모든 알파 값을 255로 설정
has_alpha = image_np.shape[2] == 4
if has_alpha:
    image_np[:, :, 3] = 255

# 조정된 이미지를 PIL 이미지로 변환
adjusted_image = Image.fromarray(image_np)

# 조정된 이미지를 저장
adjusted_image_path = './adjusted_bright.png'
adjusted_image.save(adjusted_image_path)

