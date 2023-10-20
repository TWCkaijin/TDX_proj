import requests
from pprint import pprint
import json
import os
import time
import threading

app_id = 'B123245005-ec65d34e-4947-4265'
app_key = '146df24e-2808-496d-a50e-4602a1d8dfb2'


global url
global model_name
auth_url= "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"  #Paste the authorize key here
url = "https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/ParkingAvailability/City/Kaohsiung?" #&%24top=50&%24format=JSON #Paste the target URL here 
model_name = 'Parklot_Avaliable'

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

        return{
            'authorization': 'Bearer '+access_token
        }


class data_attributes():   
    dir_path = f'{os.getcwd()}/data_storage/{model_name}'
    def __init__(self):
        self.f_time = time.strftime("%Y_%m_%d", time.localtime())  # Initialize machine time and format to specific form
        self.file_num = 0
        self.MODEL_NAME = model_name
    

    def data_storage(self,rd): #rd = RAaw Data
        while (True):
            self.file_num += 1
            
            try:
                #q = os.listdir(self.dir_path).index(f'{self.f_time}_{self.file_num}.txt')  # 必要時開啟
                t = open(file = f'{self.dir_path}/_0.txt',mode = 'r',encoding = 'utf-8').read().split("\n")
                q = t.index(f'{self.f_time}_{self.file_num}.txt')
            except:
                open(file = f'{self.dir_path}/{self.f_time}_{self.file_num}.txt',mode = 'a+',encoding = 'utf-8').write(rd)
                break

    def storage_list(self):
         open(file = f'{self.dir_path}/_0.txt',mode = 'a',encoding = 'utf-8').write(f'{self.f_time}_{self.file_num}.txt\n')


def make_url(A): #simple function for arguememts that we need to collect for the urls
    q_set = ['Top=']
    q_args = []
    guid = ['Enter any Quantity for data (NULL for all)']
    eurl = A
    for i in q_set:
        INDEX = q_set.index(i)
        q_args.append(input(f'Please enter the arguments that asks as follows:\n{i}({guid[INDEX-1]}):'))

    for i in q_set:
        if q_args[q_set.index(i)-1]!='':
            eurl = eurl+f'&%24{i}{q_args[q_set.index(i)-1]}'

    return eurl +f'&%24format=JSON'


def late_preprocess():
    exec(open(file = f'{os.getcwd()}/code_storage/DM/{model_name}.py',encoding='utf-8').read())
    

if __name__ == '__main__':
    LP = threading.Thread(target = late_preprocess)
    make_url(url)
    start_sever_time = time.time()
    time_loop = time.time()
    while (True):
        print(f'main<location>:{os.getcwd()}\nGetting data from {url}')
        
        try:
            d = data(app_id, app_key, auth_response)
            data_response = requests.get(url, headers=d.get_data_header())
        except:
            a = Auth(app_id, app_key)
            auth_response = requests.post(auth_url, a.get_auth_header())
            d = data(app_id, app_key, auth_response)
            data_response = requests.get(url, headers=d.get_data_header())
        '''
        print(auth_response)
        pprint(auth_response.text)
        print(data_response)
        pprint(data_response.text)
        '''
        da = data_attributes()
        da.data_storage(data_response.text)
        da.storage_list()
        time_loop = time.time()
        

        #Thread start zone
        LP.start()
        print(f'executing {LP.native_id}... ')

        #Thread join zone
        LP.join()


        #Wait zone
        print(time.strftime("%Y_%m_%d,%H:%M:%S", time.localtime()))
        time.sleep(1800)
        

#資料初始時間2023/10/17_21:00 + 00:18