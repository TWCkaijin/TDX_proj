from firebase import firebase 
import json




if __name__ == '__main__':
    fb = firebase.FirebaseApplication('https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/', None)
    #name = fb.get('/parklot_available', None)
    #print(name['name'])
    
    try:
        with open (file='info.json',mode='r+',encoding='utf-8') as f:
            data = json.load(f)
            i=0
            while(True):    
                fb.delete(f'/parklot_available/{data["CarParks"][i]["CarParkID"]}', None)
                
                print(data["CarParks"][i]["CarParkID"])
                i+=1
    except:
    
        fb.delete('/', None)