import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree

'''
#ffmpeg -ss [시작시간] -t [길이] -i [동영상이름] -r [프레임레이트] -s [출력해상도] -qscale:v 2 -an(오디오부분 제거) -f image2 [이미지이름]
video_list = glob("/home/data/aicity/u2net_frame_320/*/*")
result_path = "/home/data/aicity/u2net_frame_320/"
for video_name in video_list:
    video_l = video_name.split('/')
    video_n = video_l[-1]
    video_true = ('/').join(video_l[:-1])
    aa= video_n.split('NoAudio_')
    bb= aa[0] + aa[1]
    cc = video_true + '/' + bb
    print(cc)
    #pdb.set_trace()
    command = ("mv {0} {1}".format(video_name, cc))
    output = subprocess.call(command, shell=True, stdout=None)
'''
video_list = glob("/home/data/aicity/frame_320/*/*")
result_path = "/home/data/aicity/frame_320/"
for video_name in video_list:
    video_l = video_name.split('/')
    video_n = video_l[-1]
    video_true = ('/').join(video_l[:-1])
    aa= video_n.split('NoAudio_')
    bb= aa[0] + aa[1]
    cc = video_true + '/' + bb
    print(cc)
    #pdb.set_trace()
    command = ("mv {0} {1}".format(video_name, cc))
    output = subprocess.call(command, shell=True, stdout=None)