import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree


#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
video_list = glob("/home/data/aicity/u2net_frame_320/*/*")
video_list.sort()
result_path = "/home/data/aicity/u2net/"
print(video_list)
print("1")

for video_name in video_list:
    video_l = video_name.split('/')
    video_n = video_l[-1]
    video_n = video_n.split('.MP4')[0]
    dir_n = video_l[-2]
    video_name = video_name + '/'
    #print(dir_n)
    #print("ffmpeg -framerate 30 -i filename-{0}%06d.jpg {1}{2}.mp4".format(video_name,result_path,video_n))
    command = ("ffmpeg -framerate 30 -i {0}%06d.jpg {1}{2}.mp4".format(video_name,result_path,video_n))
    output = subprocess.call(command, shell=True, stdout=None)
