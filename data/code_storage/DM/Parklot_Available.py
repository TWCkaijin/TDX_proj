'''
This program can only be used with get_data.py
And only use for simplifying the data structure of Parklot_Available 
'''
import json 
import os
import time
import pandas as pd
import threading as t
import re

class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR

num_list = open(f'{os.getcwd()}//data//data_storage//Parklot_Available//_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')
thread_list = []

if __name__ == '__main__':
    T_S = time.time()
    try:#Datatype = .json
        df = pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//{num_list[-1]}.json')
        new = pd.DataFrame()

        time = []
        name = []
        spaces = []

        for i in range(len(df['ParkingAvailabilities'])):
                name.append(df['ParkingAvailabilities'][i]['CarParkName']['Zh_tw'].strip())
                spaces.append([df['ParkingAvailabilities'][i]['AvailableSpaces']])

        for i in range(len(df['UpdateTime'])):
            k = re.split('[T/+]',df.loc[i,'UpdateTime'])
            k.pop()
            time.append('_'.join(k))

        new['UpdateTime'] = time
        new['ParklotName'] = name
        new['ParkingSpaces'] = spaces
        
        for row in range(len(new)):
            try : 
               f = pd.DataFrame(pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json'))
               k = pd.DataFrame(new.iloc[row,:]).T
               result = pd.concat([f,k],axis=0,ignore_index=True)
               result.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json')
               #print(f'{Colorfill.OK}Data {Colorfill.WARNING}{data.iloc[row,1]}.json {Colorfill.OK} reconstruct complete{Colorfill.RESET}')         
            except Exception as e:
               #print(f'{Colorfill.FAIL} {e} {Colorfill.RESET}')
               f = pd.DataFrame()
               f = new.iloc[row,:]
               #f = pd.concat([f,f],axis=0,ignore_index=True)
               f.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json',index = [0])


        #new.to_json(f'{os.getcwd()}/data/data_storage/Parklot_Available/proceeded_data/{num_list[-1]}.json') #write file
        print(f"{Colorfill.OK}Data {num_list[-1]} reconstruct successfully.{Colorfill.RESET}")
        print(f'time:{time.time()-T_S}')
    except Exception  as e :
        print(f"Error with restructing the file {num_list[-1]} into database which listed in _0.txt")
        print(f"Error message:{e}")

