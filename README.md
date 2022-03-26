# aicity2022_track3  
aicity2022 challenge track3  

Preprocessing codes are updated  
**To Preprocess, follow next steps :**  
1) move "aicity" folder to /home/data  
2) run "extraction_224.py"  
3) run "namechange.py"  
4) run "preprocess_224.py"  

Data would be organized as below  
_224 folders stands for the  
**Raw Datas:**  
/home/data/aicity/A1  
/home/data/aicity/A2  

**Extracted Frames:**  
/home/data/aicity/frame  
/home/data/aicity/frame_224  

**Processed Data:**  
/home/data/aicity/byvideo  
/home/data/aicity/byvideo_224  

processed data's names are named by following rules:  
**out_name = out_dir + str(i) + '_' + class_id + '_' + label['Appearance Block'][i] + '_' + str(time_st) + '_' + str(time_en)**  
based on the labeling by aicity 2022 track3 dataset.  
