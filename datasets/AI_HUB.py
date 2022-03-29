import sys
sys.path.append('..')
import torch
from torch.utils.data.dataset import Dataset
from pathlib import Path
import pickle
import pdb
import cv2
import numpy as np
import torchvision
# import albumentations as A


class AI_HUB(Dataset):

    def __init__(self, data_dir, data_partition, clip_len=16, sample_stride=1, num_workers=None, image_size=224, norm_value=255,
                multiscale_crop=4, temporal_stride=1):

        super(AI_HUB, self).__init__()
        self.video_path = Path(data_dir)
        self.data_partition = data_partition    
        self.clip_len = clip_len
        self.image_size = image_size
        self.norm_value = norm_value
        self.multiscale_crop = multiscale_crop
        self.temporal_stride = temporal_stride
        
        self.video_list = []
        self.labels = []

        i = 0
        #Read data path
        for label in ['False', 'True']:    
            type_list = [x for x in self.video_path.joinpath(label).iterdir() if x.is_dir()]
            for type_ in type_list:
                num_list = [x for x in type_.iterdir() if x.is_dir()]
                for num_ in num_list:
                    vid_list = [x for x in num_.iterdir() if x.is_dir()]
                    for vid_ in vid_list:
                        pkl_list = [x for x in vid_.iterdir() if x.suffix=='.pkl']    
                        self.video_list.extend(pkl_list)
                        self.labels.extend([i]*len(pkl_list))
            i += 1
        print('complete {}'.format(clip_len))
        
        

    def __len__(self):
        return len(self.video_list)

    def __getitem__(self, idx):

        image_list = []
        
        with open(str(self.video_list[idx]), 'rb') as f:
            video = pickle.load(f)

        data = self.stride_sampling(video, self.clip_len, self.temporal_stride)
        # data = video[start_idx:start_idx + self.clip_len]
        data = self.color_jitter(data)
        data = self.random_flip(data, prob=0.5)

        for image_ in data:
            image_list.append(torch.from_numpy(image_.transpose(-1,0,1).copy()))

        return self.normalize(torch.stack(image_list)), self.labels[idx]


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
        mean = torch.mean(data.float())
        std = torch.std(data.float())
        return (data-mean) / std
