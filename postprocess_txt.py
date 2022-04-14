from matplotlib import pyplot as plt
import pandas as pd
import json 
import sys, time, os, pdb, argparse, pickle, subprocess, math
from glob import glob
import numpy as np
from shutil import rmtree

with open('output_320.pkl', 'rb') as f: 
    data= pickle.load(f)
sorted_data = sorted(data.items())
one_length = 1739
class_num = 20
final_data = {}

for i in range(len(sorted_data)):
    final_data[sorted_data[i][0]] = sorted_data[i][1]
    #print(sorted_data[i][0])
video_list = list(final_data.keys())
for vid in video_list:    
    names = vid
    vv = vid
    data_name = []
    for video_n in video_list:
        vn_list = video_n.split('_')
        vn_list2 = vid.split('_')
        if (vn_list2[0] ==vn_list[0]) & (vn_list2[2] ==vn_list[2]):
            data_name.append(video_n)
            video_list.remove(video_n)
    data2_name = data_name[0]
    data3_name = data_name[1]
    print(vid, data2_name, data3_name)
    names_list = names.split('_')
    if names_list[0] == '42271':
        if names_list[2] == '3':
            video_id = 1
            print(video_id)
        elif names_list[2] =='4':
            video_id = 2
            print(video_id)
        else:
            print("Error")
    elif names_list[0] == '56306':
        if names_list[2] == '2':
            video_id = 3
            print(video_id)
        elif names_list[2] =='3':
            video_id = 4
            print(video_id)
        else:
            print("Error")
    elif names_list[0] == '65818':
        if names_list[2] == '1':
            video_id = 5
            print(video_id)
        elif names_list[2] =='2':
            video_id = 6
            print(video_id)
        else:
            print("Error")
    elif names_list[0] == '72519':
        if names_list[2] == '2':
            video_id = 7
            print(video_id)
        elif names_list[2] =='3':
            video_id = 8
            print(video_id)
        else:
            print("Error")
        
    elif names_list[0] == '79336':
        if names_list[2] == '0':
            video_id = 9
            print(video_id)
        elif names_list[2] =='2':
            video_id = 10
            print(video_id)
        else:
            print("Error")
    else:
        continue
    
    max_label = []
    max_score = []
    first_frame = [-1 for i in range(class_num)]
    last_frame = [-1 for i in range(class_num)]
    max_length = {i: 0 for i in range(class_num)}
    frequency = {i: 0 for i in range(class_num)}
    longest_length = {i: 0 for i in range(class_num)}
    longest_first_frame = {i: 0 for i in range(class_num)}
    max_frame = [0 for _ in range(class_num)]
    score_board = {i: 0 for i in range(class_num)}
    a = data[names]
    b = data[data2_name]
    c = data[data3_name]
    return_length = 0
    for i in range(len(a['score'])):
        return_length += len(a['score'][i])
        
        #print(return_length)
        score = a['score'][i]
        label = a['label'][i]
        try:
            score_2 = b['score'][i]
            label_2 = b['label'][i]
        except:
            pass
        try:
            score_3 = c['score'][i]
            label_3 = c['label'][i]
        except:
            pass
        for k in range(30):
            score_board[label[k]] += score[k]
            score_board[label[k]] += score_2[k]
            score_board[label[k]] += score_3[k]
            
        for j in range(len(score)-30):
            score_board[label[j]] -= score[k]
            score_board[label[j+30]] += score[k]
            try:
                score_board[label[j]] -= score_2[k]
            except:
                pass
            try:
                score_board[label[j]] -= score_3[k]
            except:
                pass
            try:
                score_board[label[j+30]] += score_2[k]
            except:
                score_board[label[j+30]] += score_3[k]
            list_ = list(score_board.values())
            max_ = max(list_)
            index = list_.index(max_)
            #print(list_, index)
            
            max_label.append(index)
            max_score.append(max_)
        #print(max_label)
    
    
    for i in range(17):
        count = 0
        max_count = 0
        for j in range(len(max_label) -1):
            if max_label[j] == i:
                
                if first_frame[i] == -1:
                    #print(first_frame[i], j)
                    first_frame[i] = j
                elif first_frame[i] + 150 < j:
                    #print("Elif", first_frame[i], j)
                    if (last_frame[i] - first_frame[i]) > longest_length[i]:
                        longest_length[i] = last_frame[i] - first_frame[i]
                        longest_first_frame[i] = last_frame[i]
                        
                    first_frame[i] = j
                    last_frame[i] = j
                    
                else:
                    last_frame[i] = j
                    
                    #print("Else",first_frame[i], j)
                if max_label[j+1] ==i:
                    count += 1
                    
                    #if i ==0:
                    #    print(i,j)
                else:
                    max_count = count
                    max_frame[i] = j
                    count = 0
            
            max_length[i] = max_count

    #〈video_id〉 〈activity_id〉 〈start_time〉 〈end_time〉 
    # max_frame - max_length ~ max_frame까지
    f = open("final_result_orig.txt", 'a')
    #〈video_id〉 〈activity_id〉 〈start_time〉 〈end_time〉 
    for j in range(17):
        if max_length[j] == 0:
            if first_frame[j] != -1:
                print(first_frame[j], max_frame[j])
                start_frame = first_frame[j]
                end_frame = last_frame[j]
                start_time = (start_frame//one_length) * 60 + (start_frame%one_length)//30 + 1
                end_time = (end_frame//one_length) * 60 + (end_frame%one_length)//30 + 1
                if start_time == end_time:
                    end_time = start_time + 1
                print("start frame :",j, start_frame, (start_frame//one_length) * 60, (start_frame%one_length)//30, start_time)
                print("end frame :",j, end_frame, (end_frame//one_length) * 60, (end_frame%one_length)//30, end_time )

                writedown = 'no sequence : {0} {1} {2} {3}\n'.format(video_id, j, start_time, end_time)
                f.write(writedown)
        else:
            start_frame = max_frame[j] - max_length[j]
            end_frame = max_frame[j]
            start_time = (start_frame//one_length) * 60 + (start_frame%one_length)//30 + 1
            end_time = (end_frame//one_length) * 60 + (end_frame%one_length)//30 + 1
            
            start_frame_1 = longest_first_frame[j]
            end_frame_1 = longest_first_frame[j] + longest_length[j]
            start_time_1 = (start_frame_1//one_length) * 60 + (start_frame_1%one_length)//30 + 1
            end_time_1 = (end_frame_1//one_length) * 60 + (end_frame_1%one_length)//30 + 1
            
            if start_time_1 == end_time_1:
                end_time_1 = start_time + 1
                continue
            if start_time == end_time:
                end_time = start_time + 1
                
            
            print("start frame :",j, start_frame, (start_frame//one_length) * 60, (start_frame%one_length)//30, start_time)
            print("end frame :",j, end_frame, (end_frame//one_length) * 60, (end_frame%one_length)//30, end_time )
            
            writedown = '{0} {1} {2} {3}\n'.format(video_id, j, start_time_1, end_time_1)#(video_id, j,start_time_1, end_time_1)
            f.write(writedown)
    f.close() 