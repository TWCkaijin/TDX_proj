import os
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

    for i in index_list:
        try: #read json as default 
            data = pd.read_json(f'{os.getcwd()}\data/data_storage/Parklot_Avaliable/proceeded_data/{i}.json')
            # Writ down the read logic below 

            print(f'{Colorfill.OK}Data {i}.json successfully loaded{Colorfill.RESET}')
            

        except: # If json file not found , then try to read txt files
            try:    
                print(f"{Colorfill.WARNING}Json file {i}.json not found, try to read txt instead...{Colorfill.RESET}") #warning
                
                data_dict = {}
                with open(f'{os.getcwd()}/data/data_storage/Parklot_Avaliable/proceeded_data/{i}.txt', encoding = 'utf-8', mode = 'r' ) as f:
                    data = f.read()
                    spdata = data.split( '\'], [\'' )
                    lens = len(spdata) #lens : 有幾組資料

                    spdata[0] = spdata[0][3:len(spdata[0])]

                    spdata[len(spdata)-1] = spdata[len(spdata)-1][0:len( spdata[len(spdata)-1] ) - 3]
                    # print(spdata[len(spdata)-1])

                    for i in spdata :
                        temp = i.split('\', \'Total space :') # i 是 spdata 裡面的值
                        # index : value
                        # data_dict[ index ] = value
                        data_dict[temp[0]] = temp[1]
               
            except :
                print(f"{Colorfill.FAIL}Errors with reading the data {Colorfill.WARNING}{i}{Colorfill.FAIL} with txt and json, please check the execution log.{Colorfill.RESET}")
        

def dataset_construct():
    None #begins here 
    






if __name__ == '__main__':
    read_file()