import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree
import pandas as pd
from PIL import Image

#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
result_path = "/home/data/aicity/test_320/"
frame_path = "/home/data/aicity/frame_320/"

video_list = glob("/home/data/aicity/frame_320/Validation/*/*")
#print(label_list)
video_list.sort()
print(video_list)
print(len(video_list))
#print(label_list)
#User ID	Filename	Camera View	Activity Type	Start Time	End Time	Label/Class ID	Appearance Block
#File_list = output['Filename']
#pdb.set_trace()


for video_name in video_list:
    video_name_list = video_name.split('/')
    video_nn = video_name_list[-1]
    
    
    frames = glob(video_name + '/*')
    frames.sort()
    print(video_nn, len(frames))
    i = 0
    out_num = len(frames) // 1800 + 1
    for j in range(out_num):
        frame_list = []
        for frame_n in frames[j * 1800:(j+1)*1800]:
            #print(frame_n)
            fr = Image.open(frame_n)
            fr = np.array(fr)
            frame_list.append(fr)
            i+=1
            #if i % 1000 == 0:
            #    print("Done :", i, "/", len(frames))
        print("Done :", j, "/", out_num)
        out_name = result_path + video_nn + '_' + str(j) + '.npy'
        np_frames = np.array(frame_list)
        print(np_frames.shape)
        np.save(out_name, np_frames)
