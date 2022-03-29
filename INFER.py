import torch
import cv2
import copy
import numpy as np
from timeit import default_timer as timer
import pdb
from pathlib import Path
from model_no_att import MYNET
import numpy as np
import json
import sys
from glob import glob
import os
sys.path.append('.')



class Resizer(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample, common_size=512):
        image, annots = sample['img'], sample['annot']
        height, width, _ = image.shape
        if height > width:
            scale = common_size / height
            resized_height = common_size
            resized_width = int(width * scale)
        else:
            scale = common_size / width
            resized_height = int(height * scale)
            resized_width = common_size

        image = cv2.resize(image, (resized_width, resized_height))

        new_image = np.zeros((common_size, common_size, 3))
        new_image[0:resized_height, 0:resized_width] = image
        annots[:, :4] *= scale

        return {'img': torch.from_numpy(new_image), 'annot': torch.from_numpy(annots), 'scale': scale}




class Detect(object):
    def __init__(self, save_path=None):
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else 'cpu')
        self.save_path = save_path
        self.model = MYNET(30)
        # pdb.set_trace()
        checkpoint = torch.load('./best.pt', map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        self.video = glob("./Demo/*.jpg")
        # print(self.device)
        


    def resize(self):
        resized_img = []
        #print("Hello!")
        #print(self.video)
        #print(len(self.video))
        for img_ in self.video:
            image = cv2.imread('./Demo/%s'%img_, cv2.IMREAD_COLOR)
            resized_img.append(self.normalize(torch.from_numpy(cv2.resize(image, dsize = (224, 224))).permute(2,0,1)))
        return torch.stack(resized_img)
        # return torch.from_numpy(image)

    def normalize(self, data):
        data = data.float()
        mean = torch.mean(data)
        std = torch.std(data)
        return (data-mean) / std


    def process(self):
        img = self.resize()

        img = img.to(self.device)
        img = img.unsqueeze(0)
        
        with torch.no_grad():
            label = self.model(img).argmax().item()
            prob = torch.nn.functional.softmax(self.model(img))[0][1].item()
            return label, prob
    
    # def stack_buffer(self):

    def demo(self):
        # video2 = np.load(pathIn2)
        # pathIn = '../UCF/Assault/Assault006_x264.npy'
        # pathIn = '../UCF/Fighting/Fighting033_x264.npy'
        
        #여기는 assault_final.npy = frame name 주는 설정하는부분, 처음에 한번만 돌리면 다시 안해도 됨.
        file_list = []
        for file_name in glob("./Demo/*.jpg"):
            loca = os.path.basename(file_name)
            file_list.append(loca)
            video_name = os.path.splitext(loca)[0]
        file_list.sort()
        print(file_list)
        print(len(file_list))
        list = np.array(file_list)
        np.save("assault_final.npy", list)
        

        pathIn = 'assault_final.npy'
        video = np.load(pathIn) # 0 ~ 255
        print(video)
        print(len(video))
        # video = video[...,::-1].copy()

        indices = [range(x, x+30) for x in range(len(video))][:-30]
        print("indice done")
        labels = []
        probs = []
        for idx in indices:
            self.video = video[idx]
            label, prob = self.process()
            labels.append(label)
            probs.append(prob)
        print("label/prob done")
        
        with open('assault_final_label.json', 'w') as f:
            json.dump(labels, f)
        with open('assault_final_prob.json', 'w') as f:
            json.dump(probs, f)

if __name__ == '__main__':
    detect = Detect()
    #label, prob = detect.process()
    #print(label, prob)
    #pdb.set_trace()
    detect.demo()
    