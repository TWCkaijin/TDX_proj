import json 
import os

with open (f'{os.getcwd()}//info.json',mode ='r+',encoding='utf-8') as f1:
        with open (f'{os.getcwd()}//2024_02_27_24.json',mode ='r+',encoding='utf-8') as f2:
                b1 = json.load(f1)
                b2 = json.load(f2)
                for i in range(len(b2['ParkingAvailabilities'])):
                        print(b2['ParkingAvailabilities'][i]['CarParkID'])




        