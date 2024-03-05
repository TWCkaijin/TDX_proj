import json 
import os
import re

with open (file = '1.json',encoding = 'utf-8',mode ='r+') as f:
    target = json.load(f)
    with open('info.json',encoding = 'utf-8',mode = 'r+') as f2:
        data = json.load(f2)
        for i in range(len(data['CarParks'])):
            name = data['CarParks'][i]['CarParkID']
            try:
                
                target['parklot_available'][name]['Money'] = data['CarParks'][i]['FareDescription']
                print(f"Success {target['parklot_available'][i]['Money']}")

            except Exception as e:
                print(f'Err :{e}:{i}')

        
        f.truncate(0)
        f.seek(0)
        json.dump(target,f)
        f.close()
        