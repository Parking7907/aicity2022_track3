import json
import sys, time, os, pdb, argparse, pickle, subprocess
from glob import glob
import numpy as np
from shutil import rmtree
import pandas as pd
from PIL import Image

video_path = "/home/data/aicity/frame_320/"

driver_list = glob(video_path + "*")
driver_list.sort()
Train_dir = video_path + "Train"
Validation_dir = video_path + "Validation"
Train_driver = driver_list[0:4]
Train_driver.append(driver_list[5])
Validation_driver = []
for driver in driver_list:
    if driver not in Train_driver:
        Validation_driver.append(driver)
print("Train :", Train_driver)
print("Validation :", Validation_driver)

os.makedirs(Train_dir, exist_ok=True)
os.makedirs(Validation_dir, exist_ok=True)
for driver_name in Train_driver:
    print("mv {0} {1}".format(driver_name,Train_dir))
    command = ("mv {0} {1}".format(driver_name,Train_dir))
    output = subprocess.call(command, shell=True, stdout=None)
for driver_name in Validation_driver:
    print("mv {0} {1}".format(driver_name,Validation_dir))
    command = ("mv {0} {1}".format(driver_name,Validation_dir))
    output = subprocess.call(command, shell=True, stdout=None) 
