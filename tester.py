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


class ModelTester:
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
        label_list = []
        wrong_list = []
        F1_score = 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        
        with torch.no_grad():
            for b, batch in tqdm(enumerate(self.test_loader), total=len(self.test_loader)):
                
                images, labels, names = batch

                    
                images = images.to(self.device)
                labels = labels.to(self.device)
                outputs = self.model(images)
                
                # [B x Class]
                
                _, output = torch.max(outputs, 1)
                #pdb.set_trace()
                output_list.extend(output)
                label_list.extend(labels)

                        
                batch_acc = float(len(output) - sum(abs(output-labels)))/len(output)
                

                #frame per video...
                names_l = list(names)
                video_n = ['a' for _ in range(len(names_l))]
                for i, name in enumerate(names_l):
                    vid_ = os.path.basename(name)
                    vid_ = vid_.split('_')[0] + vid_.split('_')[2]
                    video_n[i] = vid_
                    if vid_ not in video_dict:
                        video_dict[vid_] = []
                        GT_dict[vid_] = int(labels[i])
                    video_dict[vid_].append(int(output[i]))
                #pdb.set_trace()
                wrong = np.array(abs(output-labels).cpu())
                false_index = np.where(wrong == 1)[0]
                self.logger.info(f"Batch_Accuracy : {batch_acc}")
            
        #print("length : ", str(len(output_list)))
        #pdb.set_trace()
        for vid in video_dict:
            vid_l = len(video_dict[vid])
            score = 0.0
            
            for out_ in video_dict[vid]:
                score = score + out_
            score = score / vid_l
            if score > 0.5:
                out_ = 1
            else:
                out_ = 0
            print(vid, GT_dict[vid], video_dict[vid], out_)
            if GT_dict[vid] ==1:
                if out_==1:
                    TP += 1
                    print("TP")
                elif out_==0:
                    FP +=1
                    print("FP")
            elif GT_dict[vid]==0:
                if out_==1:
                    FN += 1
                    print("FN")
                elif out_ ==0:
                    TN +=1
                    print("TN")
        
        #old code = frame별
        '''
        for i in range(len(output_list)):
            if label_list[i] ==1:
                if output_list[i]==1:
                    TP += 1
                elif output_list[i] ==0:
                    FP += 1
            elif label_list[i] ==0:
                if output_list[i]==1:
                    FN += 1
                elif output_list[i] ==0:
                    TN += 1
        '''
        #print(video_dict)
        accuracy_ = (TP + TN) / (TP+TN+FP+FN)
        recall_ = TP / (TP + FN)
        precision_ = TP / (TP+ FP)
        F1_score = 2 * precision_ * recall_ / (precision_ + recall_)
        print("Positive / TP / FP  Negative / TN / FN:",str(TP + FP), str(TP),str(FP),str(TN + FN),str(TN),str(FN))
        self.logger.info(f"Final Accuracy : {accuracy_}")
        self.logger.info(f"Final Recall : {recall_}")
        self.logger.info(f"Final Precision : {precision_}")
        self.logger.info(f"Final F1score : {F1_score}")
        output_list = torch.tensor(output_list)
        label_list = torch.tensor(label_list)
        tot_acc = float(len(output_list) - sum(abs(output_list-label_list)))/len(output_list)
        self.logger.info(f"Final Accuracy : {tot_acc}")
        return output_list, wrong_list

    def demo(self):
        """
        images : [B x T x C x H x W]
        labels : [B x T]
        """
        self.model.eval()
        total_loss = 0.0
        
        output_list = []
        wrong_list = []
        
        with torch.no_grad():
            for b, batch in tqdm(enumerate(self.test_loader), total=len(self.test_loader)):
                images = batch
                images = images.to(self.device)
                outputs = self.model(images)
                _, output = torch.max(outputs, 1)

                if output.item() == 1:
                    output = 1
                else:
                    output = 0

                output_list.append(output)

        return output_list, wrong_list

    def visualizaition(self):
        # to be updated
        pass

