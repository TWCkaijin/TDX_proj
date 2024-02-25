import json 
import os

with open (f'{os.getcwd()}//data//data_storage//Parklot_Available//proceeded_data//龍華.json',mode ='r+') as f:
        #base_file = json.load(f)
        #base_file["6-31"]["current_space"]= -1
        #json.dump(base_file,f)

        

        base_file = json.load(f)
        print(base_file['6-31'])
        base_file['6-31'].update({"current_space": -1})
        print(base_file['6-31'])
        print(base_file)
        f.seek(0)
        json.dump(base_file,f)