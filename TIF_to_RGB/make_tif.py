import rasterio
from rasterio.windows import Window

# 매우 용량이 큰 TIF 이미지를 분리하여 저장하는 함수
def process_large_image(image_path, tile_size, name, folder_len):
    # 이미지 열기
    with rasterio.open(image_path) as src:
        # 이미지 크기 얻기
        width = src.width
        height = src.height
        
        tile_size_x = tile_size
        tile_size_y = tile_size

        # 타일로 나누기
        xx = 0
        for y in range(0, height, tile_size_y):
            for x in range(0, width, tile_size_x):
                # 타일 영역 설정
                window = Window(x, y, min(tile_size_x, width - x), min(tile_size_y, height - y))
                # 이미지 읽기
                data = src.read(window=window)
                # data는 타일에 해당하는 픽셀 데이터
                # 결과 이미지를 저장
                new_profile = src.profile
                new_profile.update(width=window.width, height=window.height, transform=src.window_transform(window))
                # folder_len 은 폴더 개수 19개, name은 R,G,B,N 중 하나, xx은 분리된 tif 개수 0부터 n
                with rasterio.open(f"./{str(folder_len)}/{name}/{xx}.tif", 'w', **new_profile) as dst:
                    dst.write(data)
                xx+=1

if __name__ == "__main__":
    import os
    # 폴더 경로 설정
    root_folder_path = './Full scene/'
    # 폴더 내의 모든 폴더와 파일 목록을 가져옴
    folders_and_files = os.listdir(root_folder_path)
    # 폴더만 필터링하여 리스트에 저장
    folders = [item for item in folders_and_files if os.path.isdir(os.path.join(root_folder_path, item))]

    folder_len = 13 # 폴더 시작 순서 (Clipping 은 13개니까 0부터, Full scene은 6개니까 13부터
    
    # 폴더 속 폴더 개수 만큼 반복 (주어진 폴더는 Clipping, Full scene 포함 19개)
    for folder in folders:
        folder_path = os.path.join(root_folder_path, folder)
        # 현재 폴더 내의 .tif 파일 목록을 가져옴
        tif_files = [file for file in os.listdir(folder_path) if file.endswith('.tif')]
        
        folder_len += 1
        
        # tif 파일 개수만큼 반복
        for i in range(len(tif_files)):
            ppath = folder_path + '/' + tif_files[i]
            # R,G,B,N 에 따라 name 결정
            # tile_size는 분리할 tif 이미지 사이즈 크기
            if 'PR' in tif_files[i]:
                name = 'R'
                tile_size = 1000
                process_large_image(ppath, tile_size, name, folder_len)
            if 'PG' in tif_files[i]:
                name = 'G'
                tile_size = 1000
                process_large_image(ppath, tile_size, name, folder_len)
            if 'PB' in tif_files[i]:
                name = 'B'
                tile_size = 1000
                process_large_image(ppath, tile_size, name, folder_len)
            if 'PN' in tif_files[i]:
                name = 'N'
                tile_size = 1000
                process_large_image(ppath, tile_size, name, folder_len)

