import json 
import os
import time
import pandas as pd
import re
from firebase import firebase
import sys

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
        
        if(df.empty):
            print(f"{Colorfill.FAIL}No data in file. Consider the source is down.(File name: {file_num}){Colorfill.RESET}")
            return
        

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
                if(new.iloc[row,0] in f['UpdateTime'].values):
                    print("data already exist!")
                    break
                result = pd.concat([f,k],axis=0,ignore_index=True)
                result.to_json(f'{os.getcwd()}/data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json')
            except Exception as e:
                result = pd.DataFrame()
                result = new.iloc[row,:]
                result.to_json(f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//{new.iloc[row,1]}.json',index = [0])
                print(f"build file{new.iloc[row,1]}")

            try :  # Write data to Firebase Realtime Database
                firebase.put(f'/parklot_available/{new.iloc[row,1]}', new.iloc[row,0],new.iloc[row,2][0])
                #print("Data written to Firebase Realtime Database successfully.")
            except Exception as e:
                print(f"Error writing data to Firebase Realtime Database: {e}")


        print(f"{Colorfill.OK}Data {file_num} reconstruct successfully.{Colorfill.RESET}")
        return
    except Exception  as e :
        print(f"Error with restructing the file {file_num} into database which listed in _0.txt",end = "    ")
        print(f"{Colorfill.FAIL}Error message:{e}{Colorfill.RESET}")




if __name__ == '__main__':
    print(f"{Colorfill.WARNING}reconstructing and uploading... {Colorfill.RESET}")
    restruct(num_list[-1])
    