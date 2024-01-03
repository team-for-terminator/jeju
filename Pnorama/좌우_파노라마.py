import numpy as np
import cv2
import matplotlib.pyplot as plt

def find_zero_columns(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 각 열의 합 구하기
    column_sums = np.sum(gray, axis=0)
    # 0으로 채워진 열 찾기
    zero_columns = np.where(column_sums == 0)[0]
    return zero_columns

def vertical_cut(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path)
    # 0으로 채워진 열 찾기
    zero_columns = find_zero_columns(image)
    if len(zero_columns) > 0:
        # 가장 첫 번째 0으로 채워진 열을 기준으로 이미지 자르기
        cut_column = zero_columns[0]
        left_part = image[:, :cut_column]
        right_part = image[:, cut_column:]
        return left_part, right_part
    else:
        # 0으로 채워진 열이 없으면 전체 이미지 반환
        return image, None

# 파노라마로 합칠 좌/우 이미지 불러오기
imgL = cv2.imread("./왼쪽이미지.jpg")
imgR = cv2.imread("./오른쪽이미지.jpg")

# 왼쪽 이미지의 경우 파노라마 결과 0픽셀의 검은 영역이 존재할 수 있어 검은 영역 제거
left_part, right_part = vertical_cut("./왼쪽이미지.png")
imgL = left_part

# 이미지를 그레이스케일로 변환
grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

# SIFT 특징점 찾기 & 매칭
sift = cv2.xfeatures2d.SIFT_create()
kpsL, featuresL = sift.detectAndCompute(grayL, None)
kpsR, featuresR = sift.detectAndCompute(grayR, None)

# BF matcher & knn 매칭
matcher = cv2.BFMatcher()
matches = matcher.knnMatch(featuresR, featuresL, k=2)

# Ratio test 좋은 매칭점 찾기위함
good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

# 좋은 매칭점이 5개 이상이면
if len(good_matches) > 4:
    src_pts = np.float32([kpsR[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kpsL[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Homography 를 통한 두 이미지 사이의 관계 찾기
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)
    
    # 왼쪽 이미지에 맞게 오른쪽 이미지를 비틀기
    imgR_aligned = cv2.warpPerspective(imgR, M, (imgL.shape[1] + imgR.shape[1], imgL.shape[0]))
    
    # 특정 알파값을 설정하며 왼쪽 이미지와 오른쪽 이미지를 겹치는 부분과 함께 합성
    alpha = 100
    for i in range(len(imgR_aligned)):
    	for j in range(0, imgL.shape[1]-alpha):
    		imgR_aligned[i][j] = 0
   
    # 파노라마 이미지를 생성
    panorama = np.zeros_like(imgR_aligned)
    panorama[0:imgL.shape[0], 0:imgL.shape[1]] = imgL
    panorama = cv2.addWeighted(panorama, 1, imgR_aligned, 1, 0)
else:
    panorama = imgL

# 결과 시각화

cv2.imshow('panorama',panorama) # 파노라마 된 이미지
cv2.waitKey(0)
cv2.destroyAllWindows()

