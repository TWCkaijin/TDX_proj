import get_data as gd
import json 
import os
import time


proceeded_data = []
num_list = open(f'{gd.data_attributes.dir_path}/_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')
'''
for data_num in num_list:
    try :
        raw = open(f'{gd.data_attributes.dir_path}/{data_num}',mode = 'r',encoding = 'utf-8').read()
        #print(raw)
        raw = json.loads(raw)
        for park_lot in raw['ParkingAvailabilities']:
            #print(f'{park_lot["CarParkName"]["Zh_tw"]}-剩餘停車位 : {str(park_lot["TotalSpaces"])}')  #Printing all the proceeded data on the prompt
            proceeded_data.append([f'{park_lot["CarParkName"]["Zh_tw"]}',f'Total space :{str(park_lot["TotalSpaces"])}',])
    
        #print(proceeded_data)
        open(f'{gd.data_attributes.dir_path}/proceeded_data/{data_num}',mode = 'w',encoding = 'utf-8').write(str(proceeded_data))
        print(f'data {data_num} successfully loaded')
    except:
        
    
    
        print("Error with finding the data with data_name in the '_0.txt'")
        
        
        '''