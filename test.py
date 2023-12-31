import random
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import numpy as np
import cv2
import torchvision.models.segmentation
import torch
imageSize=[600,600]
imgPath="Image.jpg"

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')   # train on the GPU or on the CPU, if a GPU is not available

model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)  # load an instance segmentation model pre-trained pre-trained on COCO
model.to(device)# move model to the right devic
model.eval()

images= cv2.imread(imgPath)
images = cv2.resize(images, (imageSize[1], imageSize[0]), cv2.INTER_LINEAR)
images = torch.as_tensor(images, dtype=torch.float32).permute(2,0,1).unsqueeze(0).to(device)

with torch.no_grad():
    pred = model(images)

im= images[0].permute(1, 2, 0).cpu().numpy().astype(np.uint8)
im2 = im.copy()
for i in range(len(pred[0]['masks'])):
    msk=pred[0]['masks'][i,0].detach().cpu().numpy()
    scr=pred[0]['scores'][i].detach().cpu().numpy()
    if scr>0.8 :
        im2[:,:,0][msk>0.5] = random.randint(0,255)
        im2[:, :, 1][msk > 0.5] = random.randint(0,255)
        im2[:, :, 2][msk > 0.5] = random.randint(0, 255)
cv2.imshow(str(scr), np.hstack([im,im2]))
cv2.waitKey()
