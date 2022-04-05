import os
import sys
import time
import numpy as np
import datetime
import pickle as pkl
from pathlib import Path
import torch
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
import pdb
from tqdm import tqdm
from datetime import datetime
import shutil
import torch
import logging
import json
import time
import pickle


class Postprocess:
    def __init__(self, model, test_loader, ckpt_path, device):

        # Essential parts
        self.device = torch.device('cuda:{}'.format(device))
        self.model = model.to(self.device)
        self.test_loader = test_loader
        # Set logger
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(sh)

        self.load_checkpoint(ckpt_path)


    def load_checkpoint(self, ckpt):
        self.logger.info(f"Loading checkpoint from {ckpt}")
        # print('Loading checkpoint : {}'.format(ckpt))
        checkpoint = torch.load(ckpt, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'], strict=False)
        


    def test(self):
        self.model.eval()
        video_dict = {}
        GT_dict = {}
        output_list = []
        wrong_list = []
        F1_score = 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        output_dir = "/home/data/aicity/infer/"
        with torch.no_grad():
            for b, batch in tqdm(enumerate(self.test_loader), total=len(self.test_loader)):
                
                images, names = batch
                images = images.to(self.device)
                names = names[0]
                #print(images.shape) #2, 1800, 3, 224, 224
                output_list = []
                for i in range(int(images.shape[1])-31):
                    data = images[:,i:i+31,:,:]
                    #print(data.shape) # 2, 31, 3, 224, 224
                    outputs = self.model(data)
                    #print(outputs.shape) # 2, 19
                    _, output = torch.max(outputs, 1)
                    #print(output.shape, output) #2
                    output_list.extend(output.cpu())
                    if i % 500 == 0:
                        print("Done:", i, "/", str(int(images.shape[1])-31))
                    
                print(len(output_list))
                print(output_list)
                output = np.array(output_list)
                output = output.astype(np.float64)
                np_name = output_dir + names + '.npy'
                print(np_name)
                with open(np_name, 'wb') as f:
                    np.save(f, output)
                
        return output_list, names


