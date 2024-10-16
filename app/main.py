from fastapi import FastAPI
from app.controller import api
from app.db.session import Base, engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "go to /api/"}

app.include_router(api.router, prefix='/api')

# the following code should be included when server runs for the first time
# Base.metadata.create_all(bind=engine)
