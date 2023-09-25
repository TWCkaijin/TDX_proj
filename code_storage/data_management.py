import get_data as gd
import subprocess
import json 
import os
import time



num_list = open(f'{gd.data_attributes.dir_path}/_0.txt',mode = 'r',encoding = 'utf-8').read().split("\n") 
data_num = num_list[-1]
print(data_num)

try :
    raw = open(f'{gd.data_attributes.dir_path}/{data_num}',mode = 'r',encoding = 'utf-8').read()
    raw = json.loads(raw)
    print("data successfully loaded")
    for park_lot in raw['ParkingSpaces']:
        print(f'{park_lot["CarParkName"]["Zh_tw"]}-剩餘停車位 : {str(park_lot["TotalSpaces"])}')
except:
    print("Error with finding the data with data_name int the '_0.txt'")


    
    
    

