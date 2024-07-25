from firebase import firebase 
import pandas as pd
import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


fb = firebase.FirebaseApplication('https://potent-result-406711.firebaseio.com', None)
dir = '/data/data_storage/Parklot_Available/proceeded_data/'


        
def upload(pos,space):
    fb.put(f'/parklot_available_current', pos,space)

def construct(data,files):
    for i in range(0,48):
        for j in len(data):
            if((j-i)%48==0):
                None


def fit_func(x,a,b,c):
    return a * np.sqrt(x)*(b*np.square(x)+c) 



if __name__ == '__main__':
    file_set = os.listdir(os.getcwd()+dir)
    for files in file_set:
        print(files)
        d = pd.read_json(f'{os.getcwd()}/{dir}/{files}')
        data = d['ParkingSpaces']
        print(data)
        data = d['ParkingSpaces'].values.tolist()
        data[0] = [data[0]]
        construct(data,files)
            
    print("done")