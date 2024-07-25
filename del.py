from firebase import firebase 
import json




if __name__ == '__main__':
    fb = firebase.FirebaseApplication('https://potent-result-406711-ebf47.asia-southeast1.firebasedatabase.app/', None)
    #name = fb.get('/parklot_available', None)
    #print(name['name'])
    
 
    fb.delete(f'/parklot_available/', None)
    
