datas = glob("./OD/*")
datas.sort()
one_length = 1800
class_num = 20
final_data = {}

for i in range(len(sorted_data)):
    final_data[sorted_data[i][0]] = sorted_data[i][1]
    #print(sorted_data[i][0])
video_list = list(final_data.keys())
for vid in datas:
    print(vid)
    with open(vid, "r",encoding='UTF8') as json_file:
        a = json.load(json_file)
    #print(a[0]) {'frame': 1, 'drink': 0, 'call_right': 0, 'call_left': 0, 'text_right': 0, 'text_left': 0},
    
    names = vid.split(".json")[0]
    vv = vid
    data_name = []
    names
    names_list = names.split('_')
    print(names_list)
    if names_list[-2] == '42271':
        if names_list[-1] == '3':
            video_id = 1
            print(video_id)
        elif names_list[-1] =='4':
            video_id = 2
            print(video_id)
        else:
            print("Error")
    elif names_list[-2] == '56306':
        if names_list[-1] == '2':
            video_id = 3
            print(video_id)
        elif names_list[-1] =='3':
            video_id = 4
            print(video_id)
        else:
            print("Error")
    elif names_list[-2] == '65818':
        if names_list[-1] == '1':
            video_id = 5
            print(video_id)
        elif names_list[-1] =='2':
            video_id = 6
            print(video_id)
        else:
            print("Error")
    elif names_list[-2] == '72519':
        if names_list[-1] == '2':
            video_id = 7
            print(video_id)
        elif names_list[-1] =='3':
            video_id = 8
            print(video_id)
        else:
            print("Error")
        
    elif names_list[-2] == '79336':
        if names_list[-1] == '0':
            video_id = 9
            print(video_id)
        elif names_list[-1] =='2':
            video_id = 10
            print(video_id)
        else:
            print("Error")
    else:
        continue
    classes = [2,3,5,6]
    scores = {i:[] for i in classes}
    max_length = {i: 0 for i in classes}
    frequency = {i: 0 for i in classes}
    longest_length = {i: 0 for i in classes}
    longest_first_frame = {i: 0 for i in classes}
    max_frame = [0 for _ in range(class_num)]
    score_board = {i: 0 for i in range(class_num)}
    return_length = 0
    print(len(a))
    for i in range(len(a)):
        #print(a[0]) {'frame': 1, 'drink': 0, 'call_right': 0, 'call_left': 0, 'text_right': 0, 'text_left': 0},
        scores[2].append(a[i]['call_right'])
        scores[3].append(a[i]['call_left'])
        scores[5].append(a[i]['text_right'])
        scores[6].append(a[i]['text_left'])
    
    for i in classes:
        count = 0
        max_count = 0
        for j in range(len(a)):
            if scores[i][j] == 1:
                score_now = 1
            else:
                score_now = 0
            if score_now == 1:
                    count += 1
            else:
                max_count = count
                max_frame[i] = j
                
                if max_count > max_length[i]:
                    max_length[i] = max_count
                count = 0
        #print(max_length)
    #〈video_id〉 〈activity_id〉 〈start_time〉 〈end_time〉 
    # max_frame - max_length ~ max_frame까지
    f = open("final_result_orig.txt", 'a')
    #〈video_id〉 〈activity_id〉 〈start_time〉 〈end_time〉 
    for j in classes:
        #print(j)
        if max_length[j] == 0:
            print("j - 0")
            if first_frame[j] != -1:
                print(first_frame[j], max_frame[j])
                start_frame = first_frame[j]
                end_frame = last_frame[j]
                start_time = start_frame // 30
                end_time = end_frame // 30
                if start_time == end_time:
                    end_time = start_time + 1
                print("noseq : start frame :",j, start_frame, (start_frame//one_length) * 60, (start_frame%one_length)//30, start_time)
                print("noseq : end frame :",j, end_frame, (end_frame//one_length) * 60, (end_frame%one_length)//30, end_time )

                writedown = 'no sequence : {0} {1} {2} {3}\n'.format(video_id, j, start_time, end_time)
                f.write(writedown)
        else:
            print("j - 1")
            start_frame = max_frame[j] - max_length[j]
            end_frame = max_frame[j]
            start_time = start_frame // 30
            end_time = end_frame // 30
            #if start_time_1 == end_time_1:
                #end_time_1 = start_time + 1
                #continue
            if start_time == end_time:
                end_time = start_time + 1
                
            
            print("start frame :",j, start_frame, (start_frame//one_length) * 60, (start_frame%one_length)//30, start_time)
            print("end frame :",j, end_frame, (end_frame//one_length) * 60, (end_frame%one_length)//30, end_time )
            writedown = '{0} {1} {2} {3}\n'.format(video_id, j, start_time, end_time)#(video_id, j,start_time_1, end_time_1)
            f.write(writedown)
    f.close() 
