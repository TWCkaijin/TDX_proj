import requests
from pprint import pprint
import json
import os
import time
import threading
import pandas as pd 
import re
from firebase import firebase 
app_id = 'B123245005-ec65d34e-4947-4265'
app_key = '146df24e-2808-496d-a50e-4602a1d8dfb2'


global url
global model_name
auth_url= "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"  #Paste the authorize key here
url = "https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/Kaohsiung?" #&%24top=50&%24format=JSON #Paste the target URL here
model_name = 'Parklot_Available'


class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self): #auth = athorized
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }



class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')
        #print(access_token)
        return{
            'authorization': 'Bearer ' + access_token
        }



class data_attributes():
    dir_path = f'{os.getcwd()}/data/data_storage/{model_name}'
    
    def __init__(self):
        self.f_time = time.strftime("%Y_%m_%d", time.localtime())  # Initialize machine time and format to specific form
        self.MODEL_NAME = model_name
        self.hour = lambda x : (int(time.strftime("%H",time.localtime())))*2 if int(x)==0 or int(x)==59 or int(x)==1 else (int(time.strftime("%H",time.localtime())))*2+1
        self.file_num = time.strftime("%Y_%m_%d",time.localtime())+"_"+ str(self.hour(time.strftime("%M",time.localtime())))

    def data_storage(self,rd): #rd = Raw Data
            try:
                open(file = f'{self.dir_path}/{self.file_num}.json',mode = 'w',encoding = 'utf-8').write(rd)
                self.storage_list()
            except Exception as e:
                print(f"storaging error:{e}")


    def storage_list(self):
         open(file = f'{self.dir_path}/_0.txt',mode = 'a',encoding = 'utf-8').write(f'{self.file_num}\n')


def make_url(A): #simple function for arguememts that we need to collect for the urls
    q_set = ['Top=']
    q_args = []
    guid = ['Enter any Quantity for data (NULL for all)']
    eurl = A
    for i in q_set:
        INDEX = q_set.index(i)
        # q_args.append(input(f'Please enter the arguments that asks as follows:\n{i}({guid[INDEX-1]}):'))
        q_args.append("")
    for i in q_set:
        if q_args[q_set.index(i)-1]!='':
            eurl = eurl+f'&%24{i}{q_args[q_set.index(i)-1]}'

    return eurl +f'&%24format=JSON'


def late_preprocess():
    print(f'main<location>:{os.getcwd()}\nGetting data from {make_url(url)}')
    #os.system(f'python {os.getcwd()}/data/code_storage/DM/{model_name}.py')    # till 2023_12_04_31
    print(time.strftime("%Y_%m_%d,%H:%M:%S", time.localtime()))
    time.sleep(1200)




if __name__ == '__main__':
    print(f'{Colorfill.FAIL}Start sever time {Colorfill.RESET}{time.strftime("%Y_%m_%d,%H:%M:%S",time.localtime())}')
    print(f'{Colorfill.FAIL}Intepreter Directory: {Colorfill.OK}{os.getcwd()}{Colorfill.RESET}')
    da = data_attributes()
    while (True):
        minute = time.strftime("%M", time.localtime())
        hour = time.strftime("%H", time.localtime())
        da.file_num  = time.strftime("%Y_%m_%d",time.localtime())+"_"+ str(da.hour(minute))
        if(int(hour)%4==0 and int(minute)%30==0):
            try:
                a = Auth(app_id, app_key)
                auth_response = requests.post(auth_url, a.get_auth_header())
                d = data(app_id, app_key, auth_response)
                data_response = requests.get(url, headers=d.get_data_header())
                da.data_storage(data_response.text)
                late_preprocess()
            except Exception as e:
                print(f'{Colorfill.FAIL}Hourly error:{Colorfill.RESET}{e}')
        elif(int(minute)%30==0):
            try:
                d = data(app_id, app_key, auth_response)
                data_response = requests.get(url, headers=d.get_data_header())
                da.data_storage(data_response.text)
                late_preprocess()

            except Exception as e:
                a = Auth(app_id, app_key)
                auth_response = requests.post(auth_url, a.get_auth_header())
                d = data(app_id, app_key, auth_response)
                data_response = requests.get(url, headers=d.get_data_header())
                da.data_storage(data_response.text)
                late_preprocess()
        time.sleep(10)
        









#資料初始時間2023/10/17_21:00 + 00:18