import get_data as gd
import subprocess
import json 
import os
import time



num_list = open(f'{gd.data_attributes.dir_path}/_0.txt',mode = 'r',encoding = 'utf-8').read().split("\n") 
data_num = num_list[-1]
print()
try :
    raw = open(f'{gd.data_attributes.dir_path}/{data_num}.txt',mode = 'a+',encoding = 'utf-8')
    raw = json.loads(raw)
    
except:
    print("invalid data_name")
        
    

