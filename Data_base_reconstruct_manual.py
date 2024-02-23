import json 
import os
import time
import pandas as pd
import re
from firebase import firebase
import datetime

class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


num_list = open(f'{os.getcwd()}//data//data_storage//Parklot_Available//raw_data//_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')
firebase = firebase.FirebaseApplication('https://potent-result-406711.firebaseio.com', None)
def restruct(file_num):
    df = pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//raw_data//{file_num}.json')
    name = []
    spaces = []

    for i in range(len(df['ParkingAvailabilities'])):
            name.append(df['ParkingAvailabilities'][i]['CarParkName']['Zh_tw'].strip())
            spaces.append(df['ParkingAvailabilities'][i]['AvailableSpaces'])

    date = re.split('[T/+]',df.loc[i,'UpdateTime'])[0]
    week = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()+1
    clock = file_num.split('_')[3]
    #print(date)
    
    ############################################################################################################
    

    for location,lot_num in zip(name,spaces):
        #print(f"{location}:{week}_{clock}")
        #print(f"{location} {lot_num}")
        if(lot_num==-1):
            try: 
                base_file = pd.DataFrame(pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json'))
                base_file[f'{week}-{clock}']['current_space']= -1
                base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
            except Exception as e:
                print(f"{Colorfill.OK}New file_tick added{Colorfill.RESET}")
                try:
                    base_file = pd.DataFrame(pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json'))
                    base_file[f'{week}-{clock}'] = {'current_space': -1, 'avg_space': 0, 'dataset_quantity': 0}
                    base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
                except Exception as e :
                    print(f"{Colorfill.WARNING}New location added{Colorfill.RESET}")
                    base_file = pd.DataFrame()
                    base_file[f'{week}-{clock}'] = {'current_space': -1, 'avg_space': 0, 'dataset_quantity': 0}
                    base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
        
        else:
            try:
                base_file = pd.DataFrame(pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json'))
                base_file[f'{week}-{clock}']['current_space']= int(lot_num)
                #print(base_file[f'{week}_{clock}']['dataset_quantity'].value())
                base_file[f'{week}-{clock}']['avg_space'] = ((base_file[f'{week}-{clock}']['dataset_quantity'].value()*base_file[f'{week}-{clock}']['avg_space'])+lot_num)/(base_file[f'{week}-{clock}']['dataset_quantity']+1) 
                base_file[f'{week}-{clock}']['dataset_quantity'] += 1
                base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
            except Exception as e:
                print(f"{Colorfill.OK}New file_tick added{Colorfill.RESET}")
                try:
                    base_file = pd.DataFrame(pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json'))
                    base_file[f'{week}-{clock}'] = {'current_space': int(lot_num), 'avg_space': int(lot_num), 'dataset_quantity': 1}
                    base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
                except Exception as e :
                    print(f"{Colorfill.WARNING}New location added{Colorfill.RESET}")
                    base_file = pd.DataFrame()
                    base_file[f'{week}-{clock}'] = {'current_space': int(lot_num), 'avg_space': int(lot_num), 'dataset_quantity': 1}
                    base_file.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//X{location}.json')
    ############################################################################################################
    

if __name__ == '__main__':
    print(f"{Colorfill.FAIL}Working{Colorfill.RESET}")
    for i in num_list[0:6]:
        restruct(i)
        #print(f"{Colorfill.OK}File {i} has been restructed.{Colorfill.RESET}")
        #time.sleep(1)
    print(f"{Colorfill.OK}All files has been restructed.{Colorfill.RESET}")