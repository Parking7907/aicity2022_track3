import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree
import pandas as pd
from PIL import Image

#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
label_list = glob("/home/data/aicity/*/*/*.csv")
#print(label_list)
label_list.sort()
#label_list = label_list[2:]
#print(label_list)
result_path = "/home/data/aicity/byvideo_224/"
frame_path = "/home/data/aicity/frame_224/"
output = pd.read_csv(label_list[0])
#User ID	Filename	Camera View	Activity Type	Start Time	End Time	Label/Class ID	Appearance Block
#File_list = output['Filename']

p = 0
#label_list = label_list[8:]
length = len(label_list)
print(label_list)

for label_path in label_list:
    print("Done : ", p, "/", length)
    p+= 1
    video_l = label_path.split('/')
    #video_n = video_l[-1]
    dir_n = video_l[-2]
    print(dir_n)
    
    #/home/data/aicity/frame/user_id_24026/Dashboard_User_id_24026_NoAudio_3/
    label = pd.read_csv(label_path)
    #print(label_path)
    File_list = label['Filename']
    #print(File_list)
    end_time = -1
    undis_id = '19'
    for i, filename in enumerate(File_list):
        print(label['Start Time'][i])
        print("len:", len(label['Start Time'][i].split(':')))
        
        if len(label['Start Time'][i].split(':')) == 3:
            time_st = int(label['Start Time'][i].split(':')[0]) * 3600 + int(label['Start Time'][i].split(':')[1]) * 60 + int(label['Start Time'][i].split(':')[2])
            time_en = int(label['End Time'][i].split(':')[0]) * 3600 + int(label['End Time'][i].split(':')[1]) * 60 + int(label['End Time'][i].split(':')[2])
        elif len(label['Start Time'][i].split(':')) ==2:
            time_st = int(label['Start Time'][i].split(':')[0]) * 60 + int(label['Start Time'][i].split(':')[1])
            time_en = int(label['End Time'][i].split(':')[0]) * 60 + int(label['End Time'][i].split(':')[1])
        
        filename = str(filename)
        if filename == ' ':
            print("Nan")
        elif filename == 'nan':
            print("Nan")
        else:
            print(filename)
            filename = filename.split(' ')[-1]
            frame_dir = frame_path + dir_n + '/' + filename + '/'
            print(frame_dir)
            if time_st == 0:
                print("Wow!", i)
                end_time = -1

        #None - distracted features
        if (end_time + 1) == time_st:
            print("No Undistracted :", end_time, time_st)
        elif (end_time + 1) == time_st:
            print("No Undistracted :", end_time, time_st)
        else:
            print("Undistracted :", end_time, time_st)
            if end_time - time_st > 1:
                pass
            else:
                frame_st = end_time * 30 + 1
                frame_en = (time_st-1) * 30 + 1
                out_dir = result_path + dir_n + '/' 
                os.makedirs(out_dir, exist_ok=True)
                frames = []
                for j in range(frame_st, frame_en): # Frame_en은 제외
                    frame_n = frame_dir + "%06d.jpg"%j
                    try:
                        fr = Image.open(frame_n)
                        fr = np.array(fr)
                    except:
                        print("Error on undistracted", frame_n, i)
                        continue
                    #print(fr.shape)
                    frames.append(fr)
                out_name = out_dir + str(i) + '_' + str(undis_id) + '_' + str(label['Appearance Block'][i]) + '_' + str(end_time) + '_' + str(time_st-1)
                np_frames = np.array(frames)
                if np_frames.shape[0] == 0:
                    print("Error on distracted :", frame_n)
                print("Producing 19 : ", out_name)
                print(np_frames.shape)
                
                #pdb.set_trace()
                np.save(out_name, np_frames)

        end_time = time_en
        frame_st = time_st * 30 + 1
        frame_en = time_en * 30 + 1
        out_dir = result_path + dir_n + '/' 
        os.makedirs(out_dir, exist_ok=True)
        if label['Label/Class ID'][i] == "NA":
            class_id = '18'
        else:
            class_id = str(label['Label/Class ID'][i])

        frames = []
        for j in range(frame_st, frame_en): # Frame_en은 제외
            
            frame_n = frame_dir + "%06d.jpg"%j
            try:
                fr = Image.open(frame_n)
                fr = np.array(fr)
            except:
                print("Error : ", frame_n, i)
                continue
            #print(fr.shape)
            frames.append(fr)
        #print(label['Appearance Block'][i])
        out_name = out_dir + str(i) + '_' + str(class_id) + '_' + str(label['Appearance Block'][i]) + '_' + str(time_st) + '_' + str(time_en)
        np_frames = np.array(frames)
        if np_frames.shape[0] == 0:
            print("Error :", frame_n)
            continue
        print(out_name)
        print(np_frames.shape)
        #pdb.set_trace()
        np.save(out_name, np_frames)
    
