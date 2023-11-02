import os
from turtle import goto
import pandas as pd 
#48 datas each day


class Colorfill:
    OK = "\033[92m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR


    
def read_file():
    index_list = []
    with open(f'{os.getcwd()}\data/data_storage/Parklot_Avaliable/_0.txt', encoding = 'utf-8', mode = 'r' ) as index:
         index_list = index.read().split()  #read 
#### begin read data with line to line 
    for i in index_list:
        try: #read json as default 
            data = pd.read_json(f'{os.getcwd()}\data/data_storage/Parklot_Avaliable/proceeded_data/{i}.json')
            # Writ down the read logic below
            for row in range(1):#len(data)):
                try : 
                    f = pd.DataFrame(pd.read_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json'))
                    print(f'{Colorfill.WARNING} {data.iloc[row,:]} {Colorfill.RESET}')
                    print(pd.DataFrame({"UpdateTime": data.iloc[row,0],"ParklotName":data.iloc[row,1],"ParkingSpaces":[data.iloc[row,2]]}))
                    print(f"UpdateTime: {data.iloc[row,0]}")
                    f = f.append(pd.DataFrame({"UpdateTime": data.iloc[row,0],"ParklotName":data.iloc[row,1],"ParkingSpaces":[data.iloc[row,2]]}))
                    print(f)
                    f.to_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json')
                except:
                    f = pd.DataFrame()
                    f = data.iloc[row,:]
                    f.to_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json')
                    print("4")
                
            print(f'{Colorfill.OK}Data {i}.json successfully loaded{Colorfill.RESET}')

        except: # If json file not found , then try to read txt files
        
            try:    
                print(f"{Colorfill.WARNING}Json file {i}.json not found, try to read .txt instead...{Colorfill.RESET}") #warning
                
                data_dict = dict()
                with open(f'{os.getcwd()}/data/data_storage/Parklot_Avaliable/proceeded_data/{i}.txt', encoding = 'utf-8', mode = 'r' ) as f:
                    data = f.read()
                    spdata = data.split( '\'], [\'' )
                    lens = len(spdata) #lens :

                    spdata[0] = spdata[0][3:len(spdata[0])]

                    spdata[len(spdata)-1] = spdata[len(spdata)-1][0:len( spdata[len(spdata)-1] ) - 3]
                    # print(spdata[len(spdata)-1])

                    for i in spdata :
                        temp = i.split('\', \'Total space :') # i  spdata 
                        # index : value
                        # data_dict[ index ] = value
                        data_dict[temp[0]] = temp[1]
                print("1")
                print(data_dict)
               
            except :
                None
                print(f"{Colorfill.FAIL}Errors with reading the data {Colorfill.WARNING}{i}{Colorfill.FAIL} with .txt and .json, please check the the file.{Colorfill.RESET}")
         

def dataset_append():
    None #begins here 
    



if __name__ == '__main__':
    
    read_file()