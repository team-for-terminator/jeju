from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import file

app = FastAPI()

##########################################################
# CORS 설정 #
origins = ["http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
##########################################################

# 이미지/파일 staticFiles 마운트
app.mount("/images", StaticFiles(directory="images"), name="images")

###################################
def parse_rpc_file(rpc_file_path):
    """
    RPC 파일에서 매개변수를 파싱하는 함수.
    파일에서 각 줄을 읽고 ':'로 분리하여 매개변수의 이름과 값을 추출한다.
    값에서 숫자 부분만 추출하여 부동 소수점 수로 변환한다.
    """
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

def rpc_transform(rpc_params, pixel_x, pixel_y):
    """
    픽셀 좌표를 위도와 경도로 변환하는 함수.
    간단한 선형 변환을 적용하여 위도와 경도를 계산한다.
    """
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
rpc_file_path = 'K3A_20230501045032_44707_00075369_L1R_P_rpc.txt'

# RPC 파일 파싱
rpc_params = parse_rpc_file(rpc_file_path)
###################################
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    # 지구 반지름 (단위: km)
    R = 6371.0

    # 위도 및 경도를 라디안으로 변환
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine 공식 계산
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 반환 (단위: km)
    distance = R * c
    return distance
###################################

app.include_router(file.router)

@app.get("/")
async def home():
    return {"message": "hello world !"}

@app.get("/api/position")
async def get_position(x: int, y: int):
    # 위도, 경도 변환
    latitude, longitude = rpc_transform(rpc_params, y, x)
    return { "latitude": latitude, "longitude": longitude}

@app.get("/api/distance")
async def get_position(x1: int, y1: int, x2: int, y2: int):
    # 위도, 경도 변환
    latitude1, longitude1 = rpc_transform(rpc_params, y1, x1)
    latitude2, longitude2 = rpc_transform(rpc_params, y2, x2)

    print(latitude1, longitude1)
    print(latitude2, longitude2)

    distance = haversine_distance(latitude1,longitude1,latitude2, longitude2)
    return { "distance" : distance}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port=8000)
