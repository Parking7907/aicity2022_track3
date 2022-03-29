# aicity2022_track3  
aicity2022 challenge track3  

Preprocessing codes are updated  
**To Preprocess, follow next steps :**  
Before you run preprocess codes, label of aicity 2022 track 3 has different forms, so they should be refined. after the challenge, we'll upload some label that we edited.  
All preprocessing codes are at the preprocess_codes file:  
1) move data "aicity" folder to /home/data  
2) run "extraction_224.py"  
3) run "namechange.py"  
4) run "preprocess_224.py"  
5) move video files on Train / Validation Split.
6) in case of linux env, space on the npy file, like 1_NP _234 has some issue on codes, therefore run:  
rename 's/ //g' ./*  on
7) run "video_to_class.py"


Data would be organized as below  
_224 folders stands for the  
**Raw Datas:**  
/home/data/aicity/A1/user_id_24026/~_3.MP4  
/home/data/aicity/A2/user_id_42271/~_3.MP4  

**Extracted Frames:**  
/home/data/aicity/frame/user_id_24026/Dashboard_User_id_24026_3  
/home/data/aicity/frame_224user_id_24026/Dashboard_User_id_24026_3  

**Processed Data:**  
/home/data/aicity/byvideo/Train/user_id_24026/  
/home/data/aicity/byvideo_224/Validation/user_id_42271/  

processed data's names are named by following rules:  
**out_name = out_dir + str(i) + '_' + class_id + '_' + label['Appearance Block'][i] + '_' + str(time_st) + '_' + str(time_en)**  
based on the labeling by aicity 2022 track3 dataset.  
