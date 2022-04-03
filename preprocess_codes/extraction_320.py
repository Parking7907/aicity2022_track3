import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree


#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
video_list = glob("/home/data/aicity/*/*/*.MP4")
video_list.sort()
result_path = "/home/data/aicity/frame_320/"
os.makedirs(result_path, exist_ok=True)
for video_name in video_list:
    video_l = video_name.split('/')
    video_n = video_l[-1]
    video_n = video_n.split('.MP4')[0]
    dir_n = video_l[-2]
    print(dir_n)
    result_n = result_path + dir_n + '/' + video_n
    os.makedirs(result_n, exist_ok = True)
    print(result_n)
    command = ("ffmpeg -ss 00:00:00 -t 3600 -i {0} -an -y -s 320X320 -qscale:v 2 -f image2 {1}/%06d.jpg".format(video_name,result_n))
    output = subprocess.call(command, shell=True, stdout=None)