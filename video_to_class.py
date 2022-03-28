import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree
#/home/data/aicity/byclass_224/
#/home/data/aicity/byframe_224/
#/home/data/aicity/aicity_frame_224/

npy_list = glob("/home/data/aicity/aicity_frame_224/*/*")
npy_list.sort()
result_path = "/home/data/aicity/byclass_224/"
for i in range(19):
    os.makedirs(result_path + str(i), exist_ok=True)
#pdb.set_trace()
print(len(npy_list))
for npy_n in npy_list:
    filename = os.path.basename(npy_n)
    file_l = filename.split('_')
    classname = file_l[1]
    try:
        classname = float(classname)
        classname = int(classname)
        print(filename, classname)

    except:
        classname = 18
        print(filename, classname)
        print("NA")
    print("cp {0} {1}{2}.jpg".format(npy_n, result_path, classname))
    command = ("cp {0} {1}{2}".format(npy_n, result_path, classname))
    output = subprocess.call(command, shell=True, stdout=None)
    #pdb.set_trace()