# RPC 파일에서 매개변수를 파싱하는 함수
def parse_rpc_file(rpc_file_path):
    # 파일에서 각 줄을 읽고 ':'로 분리하여 매개변수의 이름과 값을 추출합니다.
    # 값에서 숫자 부분만 추출하여 부동 소수점 수로 변환합니다.
    rpc_params = {}
    with open(rpc_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(':\t')
            # 숫자만 추출 (단위 제거)
            value = value.split()[0]
            try:
                # 숫자로 변환
                rpc_params[key] = float(value)
            except ValueError:
                print(f"Error converting {value} to float in line: {line}")
                continue
    return rpc_params

# 픽셀 좌표를 위도와 경도로 변환하는 함수
def rpc_transform(rpc_params, pixel_x, pixel_y):
    # 간단한 선형 변환을 적용하여 위도와 경도를 계산합니다.
    # if 조건문을 통해 좀 더 정확한 좌표를 나타내고자 하였습니다.
    
    if(pixel_x > rpc_params['LINE_OFF']):
    
        if(pixel_y>rpc_params['SAMP_OFF']):
        
            lat = rpc_params['LAT_OFF'] - (pixel_x - rpc_params['LINE_OFF']) / rpc_params['LINE_SCALE'] * rpc_params['LAT_SCALE']
            lon = rpc_params['LONG_OFF'] - (pixel_y - rpc_params['SAMP_OFF']) / rpc_params['SAMP_SCALE'] * rpc_params['LONG_SCALE']
        
        else:
        
            lat = rpc_params['LAT_OFF'] - (pixel_x - rpc_params['LINE_OFF']) / rpc_params['LINE_SCALE'] * rpc_params['LAT_SCALE']
            lon = rpc_params['LONG_OFF'] + (pixel_y - rpc_params['SAMP_OFF']) / rpc_params['SAMP_SCALE'] * rpc_params['LONG_SCALE']
    
        
    else:
        if(pixel_y>rpc_params['SAMP_OFF']):
        
            lat = rpc_params['LAT_OFF'] + (pixel_x - rpc_params['LINE_OFF']) / rpc_params['LINE_SCALE'] * rpc_params['LAT_SCALE']
            lon = rpc_params['LONG_OFF'] - (pixel_y - rpc_params['SAMP_OFF']) / rpc_params['SAMP_SCALE'] * rpc_params['LONG_SCALE']
        
        else:
        
            lat = rpc_params['LAT_OFF'] + (pixel_x - rpc_params['LINE_OFF']) / rpc_params['LINE_SCALE'] * rpc_params['LAT_SCALE']
            lon = rpc_params['LONG_OFF'] + (pixel_y - rpc_params['SAMP_OFF']) / rpc_params['SAMP_SCALE'] * rpc_params['LONG_SCALE']
    return lat, lon

# RPC 파일 경로 (사용자에게서 받거나 지정)
rpc_file_path = './K3A_20230501045032_44707_00075369_L1R_PS/K3A_20230501045032_44707_00075369_L1R_P_rpc.txt'

# RPC 파일 파싱
rpc_params = parse_rpc_file(rpc_file_path)

# 사용자가 입력하는 픽셀 좌표
# 웹에서 마우스로 입력받는 것을 고려하여 mouse_x, mouse_y, index(이미지 인덱스 0~475) 를 입력받는다고 가정합니다.

mouse_x = 500
mouse_y = 300
index = 440
# 0 ~ 449
# 가로 24
# 세로 18

# 실제 픽셀로 바꾸기 위해 인덱스를 통한 가로 세로 픽셀값을 얻어줍니다.
row = int(index%24)
col = int(index/24)

# 마우스로 입력받은 데이터를 가지고 실제 픽셀값 pixel_x, pixel_y 를 계산합니다.
pixel_y = col*1000 + mouse_y
pixel_x = row*1000 + mouse_x

# 위도, 경도 변환
latitude, longitude = rpc_transform(rpc_params, pixel_y, pixel_x)

# 결과 출력
print(f"{latitude}, {longitude}")

