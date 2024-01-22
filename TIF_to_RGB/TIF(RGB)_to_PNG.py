from PIL import Image

def convert_tiff_to_png(tiff_file_path, png_file_path):
    # TIFF 파일을 불러옴
    with Image.open(tiff_file_path) as img:
        # PNG 형식으로 저장
        img.save(png_file_path, 'PNG')

# 제주도 19조각 이미지 중 1조각의 이미지를 지정하여 학습을 진행하였고,
# 1조각의 이미지를 1000x1000 크기로 자른 결과 총 475 장의 이미지가 나왔습니다.
# 총 475장의 이미지에 대해 모드 png로 바꾸는 과정입니다.
for i in range(475):
	
	# 1000x1000 크기로 저장된 tif 파일 경로
	tiff_file = './'+str(i)+'.tif'

	# 저장할 PNG 파일 경로
	png_file = './'+str(i)+'.png'

	# 함수를 호출하여 변환 수행
	convert_tiff_to_png(tiff_file, png_file)
