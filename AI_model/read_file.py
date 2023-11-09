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
    for data_name  in index_list:
        try: #read json as default 
            
            json_append(data_name)
            print('\n')
        except Exception as e: # If json file not found , then try to read txt files
            txt_append(data_name)
            print('\n')
    print(f"ALl execution are done")
            
         

def json_append(i):
    data = pd.read_json(f'{os.getcwd()}\data/data_storage/Parklot_Avaliable/proceeded_data/{i}.json')
    # Writ down the read logic below
    print(f'Data {i} executing: ',end = '')
    exe_time = 0
    generate = False
    for row in range(len(data)):
        generate = False 
        try : 
           f = pd.DataFrame(pd.read_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json'))
           k = pd.DataFrame(data.iloc[row,:]).T
           result = pd.concat([f,k],axis=0,ignore_index=True)
           result.to_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json')
           #print(f'{Colorfill.OK}Data {Colorfill.WARNING}{data.iloc[row,1]}.json {Colorfill.OK} reconstruct complete{Colorfill.RESET}')         
        except Exception as e:
           print(f'{Colorfill.FAIL} {e} {Colorfill.RESET}')
           f = pd.DataFrame()
           f = data.iloc[row,:]
           #f = pd.concat([f,f],axis=0,ignore_index=True)
           f.to_json(f'{os.getcwd()}/AI_model/source/{data.iloc[row,1]}.json',index = [0])
           print(f'{Colorfill.OK}Data {Colorfill.WARNING}{data.iloc[row,1]}.json {Colorfill.OK} generate complete{Colorfill.RESET}')
           generate = True
        finally:
           if (int(len(data) - len(data)/(row+1))/(len(data)/80)>exe_time) and not(generate):
               #print('#',end='')
               exe_time += 1
    if not (generate) :
        #print("|")
        None
    print(f'{Colorfill.OK}Data {i}.json have successfully loaded{Colorfill.RESET}')
     
def txt_append(i):
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
        print(data_dict)
               
    except :
        None
        print(f"{Colorfill.FAIL}Errors with reading the data {Colorfill.WARNING}{i}{Colorfill.FAIL} with .txt and .json, please check the the file.{Colorfill.RESET}")
    



if __name__ == '__main__':
    
    read_file()