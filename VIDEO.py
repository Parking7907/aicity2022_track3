import torch
import cv2
import copy
import numpy as np
from timeit import default_timer as timer
import pdb
from pathlib import Path
import numpy as np
import json

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
        # self.model = MYNET(30)
        # pdb.set_trace()
        # checkpoint = torch.load('./best.pt', map_location=self.device)
        # self.model.load_state_dict(checkpoint['model_state_dict'])
        # self.model = self.model.to(self.device)
        # self.model.eval()
        self.video = []
        # print(self.device)
        


    def resize(self):
        resized_img = []
        for img_ in self.video:
            resized_img.append(self.normalize(torch.from_numpy(cv2.resize(img_, (224, 224))).permute(2,0,1)))
        return torch.stack(resized_img)
        # return torch.from_numpy(image)

    def normalize(self, data):
        data = data.float()
        mean = torch.mean(data)
        std = torch.std(data)
        return (data-mean) / std



    
    # def stack_buffer(self):

    def demo(self):
        # video2 = np.load(pathIn2)
        #pathIn = '../UCF/Fighting/Fighting033_x264.npy'
        #pathIn = '../UCF/Assault/Assault006_x264.npy'
        pathIn = 'assault_final.npy'
        #label = range(1185, 8096)

        with open('assault_final_prob.json', 'r') as f:
            result = json.load(f)
        with open('assault_final_label.json', 'r') as f:
            label = json.load(f)
        #print(label, result)
        #pdb.set_trace()
        
        video = np.load(pathIn) # 0 ~ 255
        image = []
        #print(len(image))
        for img_ in video:
            #print(img_)
            image.append(cv2.imread('./Demo/%s'%img_, cv2.IMREAD_COLOR)) #.astype(np.float32) 
            
        print("image : %i개"%len(image))
        #pdb.set_trace()
        



        #video = video[...,::-1].copy()
        #print(len(video))
        #pdb.set_trace()
        print("Video Writer Start!")
        out = cv2.VideoWriter('total_result.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (1280,720))
        
        for i in range(30, len(video)-1):
            if i in label:
                cv2.putText(image[i], "Fight", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255, 255), 3)

            if result[i-30] > 0.3:
                cv2.putText(image[i], "Fight", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0, 255), 3)

    
        for i in range(len(video)):
            out.write(image[i])

if __name__ == '__main__':
    detect = Detect()
    detect.demo()
    