from sqlalchemy.orm import Session
from app.model.picture import Picture

from app.service.models.mtcnn import MTCNN
from app.service.models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def cos_sim(A, B):
    return torch.dot(A, B) / (torch.norm(A) * torch.norm(B))

# def similarity(id1, id2, db):
#     pic1 = db.query(picture).filter(picture.id == id1).first()
#     pic2 = db.query(picture).filter(picture.id == id2).first()
    
#     img1 = Image.open(pic1.path)
#     img2 = Image.open(pic2.path)

#     width, height = img1.size

#     mtcnn = MTCNN(image_size=width, margin=0, device=device)
#     resnet = InceptionResnetV1(pretrained='vggface2').eval()

#     img_cropped1 = mtcnn(img1)
#     img_cropped2 = mtcnn(img2)

#     img_embedding1 = resnet(img_cropped1.unsqueeze(0)).squeeze(0)
#     img_embedding2 = resnet(img_cropped2.unsqueeze(0)).squeeze(0)

#     sim = cos_sim(img_embedding1, img_embedding2).item()

#     return sim

def similarity(id1, id2, db):
    pic1 = db.query(Picture).filter(Picture.id == id1).first()
    pic2 = db.query(Picture).filter(Picture.id == id2).first()
    # print(pic1.id)
    # print(pic2.id)

    img_embedding1 = torch.tensor(pic1.embedding, device=device)
    img_embedding2 = torch.tensor(pic2.embedding, device=device)

    sim = cos_sim(img_embedding1, img_embedding2).item()

    return sim

def search(id1, thershold, db):
    sim_list = []
    
    pic1 = db.query(Picture).filter(Picture.id == id1).first()    
    img_embedding1 = torch.tensor(pic1.embedding)

    for pic in db.query(Picture).all():
        if pic.id == int(id1) or not pic.embedding:
            continue  # 자신과 비교하거나 임베딩이 없는 이미지는 제외

        img_embedding2 = torch.tensor(pic.embedding)
        sim = cos_sim(img_embedding1, img_embedding2).item()
        temp = [pic.id, sim]
        sim_list.append(temp)
    
    sim_list.sort(reverse=True)

    # return sim_list[:thershold]
    return [item[0] for item in sim_list[:thershold]]