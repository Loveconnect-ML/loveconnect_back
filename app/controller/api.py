from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from app.db.connection import get_db

from app.service.generate import generate
from app.service.similarity import similarity, search
from app.model.picture import Picture

import torch
import os

router = APIRouter()

@router.get("/")
def root():
    return {"generate image" : "/generate + prompt",
            "calculation similarity" : "/similairty + id1,id2",
            "search most similar image id" : "/search + id, thershold",
            "get image" : "image/id"}

@router.get("/generate")
def generate_api(prompt: str = "portrait photo of 20 y.o cute korean woman", db: Session = Depends(get_db)):
    """
    prompt에 맞는 이미지 생성 후 리턴
    """
    pic = generate(prompt, db)

    # return FileResponse(pic['path'])
    return pic['id']

@router.get("/similarity")
def similarity_api(id1:str, id2:str, db: Session = Depends(get_db)):
    """
    2개의 이미지 유사도 계산 후 리턴
    """
    return similarity(id1, id2, db)

@router.get("/search")
def search_api(id:str, thershold:int = 4, db: Session = Depends(get_db)):
    """
    입력받은 id의 이미지와 db속 가장 비슷한 이미지 리턴
    """
    sim_list = search(id, thershold, db)
    return sim_list

@router.get("/image/{id}")
def get_image(id: int, db: Session = Depends(get_db)):
    """
    입력받은 id를 통해 해당 이미지를 반환
    """
    # 데이터베이스에서 이미지 정보를 가져옴
    pic = db.query(Picture).filter(Picture.id == id).first()
    if not pic:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = pic.path
    print("file path:", file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path=file_path)