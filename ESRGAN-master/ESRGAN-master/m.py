import cv2

img = cv2.imread("/home/a/Desktop/Deep_Learning/Super_Resolution/ESRGAN-master/LR/319.tif")

img = cv2.resize(img,(1000,1000))

cv2.imwrite("/home/a/Desktop/Deep_Learning/Super_Resolution/ESRGAN-master/LR/319_res.tif",img)
