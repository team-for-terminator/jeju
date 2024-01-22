import string
import random
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
import time
from fastapi import HTTPException
import shutil
import os

router = APIRouter(
    tags=['files']
)


@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    now = time.time()

    new = f'_{rand_str}_{now}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    print(filename)

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'image_url': path, 'image_name': filename}


@router.post('/file')
def upload_file(file: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    now = time.time()

    new = f'_{rand_str}_{now}.'
    filename = new.join(file.filename.rsplit('.', 1))
    path = f'files/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {'file_url': path, 'file_name': filename}


@router.get('/file/list')
def file_list():
    # 해당 경로의 파일 목록을 불러옴
    files = os.listdir('files/')
    return files
