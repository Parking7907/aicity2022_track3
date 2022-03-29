#/home/data/aicity/byclass_224/1/
import sys
sys.path.append('..')
import torch
import yaml
from torch.utils.data.dataset import Dataset
#from torchvision.transforms import Normalize
from pathlib import Path
import pickle
import pdb
import cv2
import numpy as np
import torchvision
import os
from glob import glob
# import albumentations as A
class AICity(Dataset):
    def __init__(self, data_dir, data_partition, clip_len = 30, sample_stride=1, num_workers=24, image_size=224, norm_value=255,
                multiscale_crop=4, temporal_stride=1):
        super(AICity, self).__init__()
        self.video_path = Path(data_dir)
        self.data_partition = data_partition    
        self.clip_len = clip_len
        self.image_size = image_size
        self.norm_value = norm_value
        self.multiscale_crop = multiscale_crop
        self.temporal_stride = temporal_stride
        self.video_name_list = []
        self.video_list = []
        self.labels = []
        i = 0
        #Read data path
        class_list = [str(j) for j in range(19)]
        for label in class_list:
            vid_list = os.path.join(self.video_path, label)
            print(vid_list + '/*')
            pkl_list = glob(vid_list + '/*')
               
            self.video_list.extend(pkl_list)
            self.labels.extend([i]*len(pkl_list))
         
            print('%s = %i complete %i'%(label, i, len(pkl_list)))
            i += 1
            #pdb.set_trace()
        
        #pdb.set_trace()
    def __len__(self):
        return len(self.video_list)

    def __getitem__(self, idx):
        image_list = []
        
        with open(str(self.video_list[idx]), 'rb') as f:
            #print(self.video_list[idx])
            #self.video_name_list.append(self.video_list[idx])
            video = np.load(f)
        data = self.stride_sampling(video, self.clip_len, self.temporal_stride)
        #data = video[start_idx:start_idx + self.clip_len]
        
        data = self.color_jitter(data)
        #if self.data_partition == 'train':
        data = self.random_flip(data, prob=0.5)
        for image_ in data:
            image_list.append(torch.from_numpy(image_.transpose(-1,0,1).copy()))

        output = self.normalize(torch.stack(image_list)) # 31,3,224,224
        #print(torch.max(output))
        #print(output.type()) # torch. DoubleTensor, 이전꺼는 torch.ByteTensor
        
        return output, self.labels[idx], self.video_list[idx]


    def random_flip(self, video, prob):
        s = np.random.rand()
        if s < prob:
            video = np.flip(m=video, axis=2)
        return video    

    def stride_sampling(self, video, target_frames, stride):
        vid_len = len(video)

        if vid_len >= (target_frames-1)*stride + 1:
            start_idx = np.random.randint(vid_len - (target_frames-1)*stride)
            data = video[start_idx:start_idx+(target_frames-1)*stride+1:stride]
            

        elif vid_len >= target_frames:
            start_idx = np.random.randint(len(video) - target_frames)
            data = video[start_idx:start_idx + target_frames + 1]

        # Need Zero-pad
        else:
            sampled_video = []
            for i in range(0, vid_len):
                sampled_video.append(video[i])

            num_pad = target_frames - len(sampled_video)
            if num_pad>0:
                while num_pad > 0:
                    if num_pad > len(video):
                        padding = [video[i] for i in range(len(video)-1, -1, -1)]
                        sampled_video += padding
                        num_pad -= len(video)
                    else:
                        padding = [video[i] for i in range(num_pad-1, -1, -1)]
                        sampled_video += padding
                        num_pad = 0
            data = np.array(sampled_video, dtype=np.float32)
        
        return data
            
    def color_jitter(self,video):
        # range of s-component: 0-1
        # range of v component: 0-255
        s_jitter = np.random.uniform(-0.2,0.2)
        v_jitter = np.random.uniform(-30,30)
        for i in range(len(video)):
            hsv = cv2.cvtColor(video[i], cv2.COLOR_RGB2HSV)
            s = hsv[...,1] + s_jitter
            v = hsv[...,2] + v_jitter
            s[s<0] = 0
            s[s>1] = 1
            v[v<0] = 0
            v[v>255] = 255
            hsv[...,1] = s
            hsv[...,2] = v
            video[i] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return video


    def normalize(self, data):
        max_ = 255
        data = data.float()
        data = data/max_
        #print(data.shape, torch.max(data), torch.min(data))
        mean = torch.mean(data.float())
        std = torch.std(data.float())
        #print(mean, std)
        return data

#with open('../config/AICity.yml', mode='r') as f:
    #config = yaml.load(f,Loader=yaml.FullLoader)
#train_dataset = AICity(config['datasets']['train'], 'train', config['MYNET']['sequence_size'], temporal_stride=config['datasets']['stride'])
#pdb.set_trace()