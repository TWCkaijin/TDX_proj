import requests
import json
import time
import pandas as pd
import re
from firebase import firebase


auth_url= "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"  #Paste the authorize key here
url = "https://tdx.transportdata.tw/api/basic/v1/Parking/OffStreet/CarPark/City/Kaohsiung?%24format=JSON"
app_id = 'B123245005-ec65d34e-4947-4265'
app_key = '146df24e-2808-496d-a50e-4602a1d8dfb2'

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


def uplod_to_firebase(data):
    fb = firebase.FirebaseApplication('https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/', None)
    for i in range(len(data['CarParks'])):
        #print(f"{data['CarParks'][i]['CarParkID']}: ({data['CarParks'][i]['CarParkPosition']['PositionLat']},{data['CarParks'][i]['CarParkPosition']['PositionLon']})")
        #print(f"/parklot_available/{data['CarParks'][i]['CarParkID']}--Money: {data['CarParks'][i]['FareDescription']}")
        fb.put(f"/parklot_available/{data['CarParks'][i]['CarParkID']}", "LatLon",f"({data['CarParks'][i]['CarParkPosition']['PositionLat']},{data['CarParks'][i]['CarParkPosition']['PositionLon']})")
        fb.put(f"/parklot_available/{data['CarParks'][i]['CarParkID']}","Money",f"data['CarParks'][i]['FareDescription']")

    


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    auth_response = requests.post(auth_url, a.get_auth_header())
    d = data(app_id, app_key, auth_response)
    data_response = requests.get(url, headers=d.get_data_header())
    uplod_to_firebase(data_response.json())
    #print(data_response.text)

    