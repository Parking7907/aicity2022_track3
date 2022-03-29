from matplotlib import pyplot as plt
import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree
import csv

#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
command = ("ffmpeg -ss 00:00:00 -t 339 -i ./total.mp4 -an -y -s 1280X720 -qscale:v 2 -f image2 Demo/%06d.jpg")
output = subprocess.call(command, shell=True, stdout=None)
#command = ("cp -r preprocess/new_blackbox/ /home/jinyoung/share/sort/blackbox")
#output = subprocess.call(command, shell=True, stdout=None)
'''
file_list = []
for file_name in glob("./Demo/*.jpg"):
    loca = os.path.basename(file_name)
    file_list.append(loca)
    video_name = os.path.splitext(loca)[0]
list = np.array(file_list)
np.save("assault_final.npy", list)



for file_name in glob("./sk/*"):
    loca = os.path.basename(file_name)
    video_name = os.path.splitext(loca)[0]
    file_n = os.path.join(file_name,"alphapose-results.json")
    print(video_name)
    with open(file_n,"r") as alpha:
        data = json.load(alpha)
    #data = np.array(data)
    data_len = len(data)
    #print(data_len)
    tmp_box = [[0 for col in range(1)] for row in range(150)]
    tmp_list = [[0 for col in range(1)] for row in range(150)]
    tmp_1 = {}


    #print(data_len)
    for i in range(data_len):
        image_id = int(os.path.splitext(data[i]['image_id'])[0])
        keypoints = data[i]['keypoints']
        box = data[i]['box']
        #print(box)
        #print(image_id)
        #print(keypoints)
        #tmp_list = np.append([tmp_list,keypoints], axis=0)
        #print(tmp_list[image_id])
        if tmp_list[image_id] == [0]:
            tmp_list[image_id][0]=keypoints
        elif tmp_list[image_id] != [0]:
            tmp_list[image_id].append(keypoints)
        if tmp_box[image_id] == [0]:
            tmp_box[image_id][0]=box
        elif tmp_box[image_id] != [0]:
            tmp_box[image_id].append(box)
    #print(tmp_list)
    #print(len(tmp_box))
    #print(tmp_list)
#         tmp_1 = {'name':video_name, 'keypoints':tmp_list, 'box':tmp_box}
    tmp_1 = {'keypoints':tmp_list, 'box':tmp_box}
    #pickle.dump
    with open('train/Fight/'+video_name+'.pkl', 'wb') as f:  
        pickle.dump(tmp_1, f)

    print(tmp_1)
    print(len(tmp_1['box']))
    #print(len(tmp_1['keypoints'][0]))
'''
