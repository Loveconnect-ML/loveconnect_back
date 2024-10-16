# loveconnect_back

## **Required packages installation**
install by conda & env.yaml

```
conda env create -f env.yaml
```

install by pip & requirements.txt

```
# Create env and Install python
conda create -n loveconnect_back python=3.10

# pytorch and torchvision
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other requirements
pip install -r requirements.txt
```

## Run server

you should migration db by main.py

```python
from fastapi import FastAPI
from app.controller import api
from app.db.session import Base, engine

app = FastAPI()

@app.get("/")
def root():
    return {"message": "go to /api/"}

app.include_router(api.router, prefix='/api')

# the following code should be included when server runs for the first time
Base.metadata.create_all(bind=engine)

```

run fastapi server

```
# for test
fastapi dev

# for release
fastapi run
```