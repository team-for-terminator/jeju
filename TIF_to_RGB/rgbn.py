import imageio
import numpy as np
import os

# TIF 이미지의 RGB 혹은 RGBN 채널 합성 함수
def merge_channels_to_tif(red_path, green_path, blue_path, nir_path, output_tif):
    # 각각의 채널을 imageio 로 읽어들임
    red_channel = imageio.imread(red_path)
    green_channel = imageio.imread(green_path)
    blue_channel = imageio.imread(blue_path)
    nir_channel = imageio.imread(nir_path)

    # 16비트 이미지를 8비트 이미지로 변환
    red_channel = (red_channel / np.max(red_channel) * 255).astype(np.uint8)
    green_channel = (green_channel / np.max(green_channel) * 255).astype(np.uint8)
    blue_channel = (blue_channel / np.max(blue_channel) * 255).astype(np.uint8)
    nir_channel = (nir_channel / np.max(nir_channel) * 255).astype(np.uint8)

    # 채널을 4채널 혹은 3채널로 합치기
    #merged_image = np.stack([red_channel, green_channel, blue_channel, nir_channel], axis=-1)
    merged_image = np.stack([red_channel, green_channel, blue_channel], axis=-1)
    
    # 알파 채널이 있는지 확인하고 모든 알파 값을 255로 설정
    has_alpha = merged_image.shape[2] == 4
    if has_alpha:
        merged_image[:, :, 3] = 255

    # 이미지 저장
    imageio.imwrite(output_tif, merged_image)


# 폴더 경로 설정
root_folder_path = './Clipping/'


# 폴더 내의 모든 폴더와 파일 목록
folders_and_files = os.listdir(root_folder_path)

# 폴더만 필터링하여 리스트에 저장
folders = [item for item in folders_and_files if os.path.isdir(os.path.join(root_folder_path, item))]

folder_len = 0
    
# 폴더 속 폴더 수만큼 반복
for folder in folders:
    folder_len += 1
    folder_path = os.path.join(root_folder_path, folder)
    # 분리된 TIF 파일 개수를 알기위함
    nom_folder_path = f'/home/a/Desktop/창업팀/공모전/RGBN2/{folder_len}/R'
    folders_and_files = os.listdir(nom_folder_path)
    
    # TIF 파일 개수만큼 반복
    for i in range(len(folders_and_files)):
        # 각 채널 R, G, B, N 파일을 불러오고, 출력 파일 경로도 설정
        red_channel_path = f'./{folder_len}/R/{i}.tif'
        green_channel_path = f'./{folder_len}/G/{i}.tif'
        blue_channel_path = f'./{folder_len}/B/{i}.tif'
        nir_channel_path = f'./{folder_len}/N/{i}.tif'
        output_tif_path = f'./{folder_len}/RGBN/{i}.tif'

        # tif 이미지 채널 합치고 저장
        merge_channels_to_tif(red_channel_path, green_channel_path, blue_channel_path, nir_channel_path, output_tif_path)

