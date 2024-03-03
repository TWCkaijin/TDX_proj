from firebase import firebase
import json
import os

fb = firebase.FirebaseApplication('https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/', None)

if __name__ == "__main__":
    with open (os.getcwd()+'info.json','r',encoding='utf-8') as f:
        file = json.load(f)
        i=0
        while(True):
            fb.put(f'parklot_name/{file["CarParks"][i]["CarParkID"]}','name',file[i]["CarParkName"]["Zh_tw"])
            i+=1
