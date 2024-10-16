from sqlalchemy.orm import Session
from app.model.picture import Picture
from diffusers import DiffusionPipeline
import torch
from safetensors.torch import load_file

from app.service.models.mtcnn import MTCNN
from app.service.models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_id = "SG161222/RealVisXL_V5.0_Lightning"
# pipe = DiffusionPipeline.from_pretrained(model_id)

prompt_prefix = "instagram photo, "
prompt_surffix = ", "
negative_prompt = "(octane render, render, drawing, anime, bad photo, bad photography:1.3), (worst quality, low quality, blurry:1.2), (bad teeth, deformed teeth, deformed lips), (bad anatomy, bad proportions:1.1), (deformed iris, deformed pupils), (deformed eyes, bad eyes), (deformed face, ugly face, bad face), (deformed hands, bad hands, fused fingers), morbid, mutilated, mutation, disfigured"

save_path = "/home/jin/Desktop/Challenge/AIX/back/app/images"

pipe = DiffusionPipeline.from_pretrained(model_id)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def generate(prompt, db):
    global pipe
    pipe = pipe.to(device)
    image = pipe(prompt_prefix + prompt + prompt_surffix, negative_prompt=negative_prompt, num_inference_steps=5, guidance_scale=1.5, sampler="dpm++").images[0]
    
    temp = Picture(path="", embedding=None)
    db.add(temp)
    db.commit()
    db.refresh(temp)
    
    path = save_path + f"/{temp.id}.png"
    image.save(path)
    
    image = Image.open(path)
    width, height = image.size
    
    #  mtcnn = MTCNN(image_size=width, margin=0, device=device)
    mtcnn = MTCNN(image_size=width, margin=0)
    img_cropped = mtcnn(image)
    # resnet = InceptionResnetV1(pretrained='vggface2').eval()
    global resnet
    img_embedding = resnet(img_cropped.unsqueeze(0)).squeeze(0)

    temp.embedding = img_embedding.tolist() # 텐서틑 입력 불가
    temp.path = path
    db.commit()

    return {'id':temp.id, 'path':temp.path}