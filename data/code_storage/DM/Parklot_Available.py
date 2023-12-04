import json 
import os
import time
import pandas as pd
import re
from firebase import firebase

class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR

num_list = open(f'{os.getcwd()}//data//data_storage//Parklot_Available//_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')
firebase = firebase.FirebaseApplication('https://potent-result-406711.firebaseio.com', None)
def restruct(file_num):
    try:#Datatype = .json
        df = pd.read_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//{file_num}.json')
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
            except Exception as e:
               f = pd.DataFrame()
               f = new.iloc[row,:]
               f.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json',index = [0])
               print("build file")
            
            try :  # Write data to Firebase Realtime Database
                data = result.iloc[len(result)-1].to_dict()
                firebase.put(f'/parklot_available/{data["ParklotName"]}', data['UpdateTime'],data['ParkingSpaces'][0])
                #print("Data written to Firebase Realtime Database successfully.")
            except Exception as e:
                print(f"Error writing data to Firebase Realtime Database: {e}")


        print(f"{Colorfill.OK}Data {file_num} reconstruct successfully.{Colorfill.RESET}")
    except Exception  as e :
        print(f"Error with restructing the file {file_num} into database which listed in _0.txt")
        print(f"Error message:{e}")



if __name__ == '__main__':
    restruct(num_list[-1])