import numpy as np, cv2
import matplotlib.pyplot as plt

# 위/아래 이미지 불러오기
imgU = cv2.imread("./위 이미지.jpg")
imgD = cv2.imread("./아래 이미지.png")

hl, wl = imgU.shape[:2]     # 위 사진 높이, 넓이
hr, wr = imgD.shape[:2]     # 아래 사진 높이, 넓이

grayU = cv2.cvtColor(imgU, cv2.COLOR_BGR2GRAY)  # 위 이미지 그레이 스케일 변환
grayD = cv2.cvtColor(imgD, cv2.COLOR_BGR2GRAY)  # 아래 이미지 그레이 스케일 변환

# SIFT 특징점 찾기 & 매칭
descriptor = cv2.xfeatures2d.SIFT_create()  
 # 키포인트, 디스크립터 
(kpsL, featuresL) = descriptor.detectAndCompute(grayU, None)
(kpsR, featuresR) = descriptor.detectAndCompute(grayD, None)

# BF matcher & knn 매칭
matcher = cv2.DescriptorMatcher_create("BruteForce")    # BF 매칭기 생성
matches = matcher.knnMatch(featuresR, featuresL, 2)     # knn 매칭

# 좋은 매칭점 선별
good_matches = []
for m in matches:
    if len(m) == 2 and m[0].distance < m[1].distance * 0.75:  
        good_matches.append((m[0].trainIdx, m[0].queryIdx))

# 좋은 매칭점이 5개 이상인 원근 변환행렬 구하기
if len(good_matches) > 4:
    ptsL = np.float32([kpsL[i].pt for (i,_) in good_matches])   
    ptsR = np.float32([kpsR[i].pt for (_,i) in good_matches])  
    mtrx, status = cv2.findHomography(ptsR, ptsL, cv2.RANSAC, 4.0)
    # 원근 변환행렬로 오른쪽 사진을 원근 변환, 결과 이미지 크기는 사진 2장 크기
    panorama = cv2.warpPerspective(imgD, mtrx, (wl, hl + hr))
   
    # 위쪽 사진을 아래쪽에 붙이는 과정
    c = 0
    ii = 0
    for i in range(int(len(imgU)/2),len(imgU)):
    	for j in range(len(imgU[0])):
    		if (imgU[i][j] != 0).all():
    			break
    		if j == len(imgU[0]) -1:
    			imgU = imgU[0:i, 0:len(imgU[0])]
    			ii = i
    			c = 1
    	if c == 1:
    		break
    
    if ii != 0:
        panorama[0:ii, 0:wl] = imgU
    else:
        panorama[0:hl, 0:wl] = imgU
# 좋은 매칭점이 4개가 안되는 경우
else:   
    panorama = imgU


#################### 만약 이미지의 겹치는 점이 적다면 해당 주석을 풀고 이미지를 이어붙임 ########################
#merged_image = np.zeros((hl+hr, wl, 3), dtype=np.uint8)
#merged_image[:hl, :] = imgU
#merged_image[hl-20:hl+hr-20, :] = imgD

# 결과 출력
cv2.imshow('Up Image', imgU)
cv2.imshow('Down Image', imgD)
cv2.imshow('Panorama', panorama)
#cv2.imshow('merged_image', merged_image) # 이미지를 이어붙이는 경우 주석해제
cv2.waitKey(0)
cv2.destroyAllWindows()

