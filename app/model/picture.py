from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSON
from app.db.session import Base

class Picture(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True) # 생성된 사진 id
    path = Column(String, nullable=False) # 실제 사진 경로 (사진을 db에 깡으로 저장하면 호율이 떨어진다고 함)
    embedding = Column(JSON, nullable=True) # 모든 이미지와 임베딩 값 비교하는 게 너무 오래걸릴 것 같아서 미리 저장