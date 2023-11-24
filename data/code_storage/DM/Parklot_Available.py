'''
This program can only be used with get_data.py  
'''
import get_data as gd
import json 
import os
import time
import re
import pandas as pd
import MySQLdb
import sys
import MySQLdb

proceeded_data = []
num_list = open(f'{gd.data_attributes.dir_path}/_0.txt',mode = 'r',encoding = 'utf-8').read().split('\n') 
num_list.remove('')


def sql_write(table_name, time, spaces) :
    db = MySQLdb.connect(
        host='webserverdatabase.cmstfznt40ot.ap-southeast-2.rds.amazonaws.com',
        port=3306,
        user='AFD_Kai',
        passwd='AFD_Kai_PythonMaster',
        db='GDSC',
    )

    curs = db.cursor()

    # Check if the table exists
    curs.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = curs.fetchone()

    if result:
        # Table exists, insert data
        for i in range(len(time)):
            curs.execute(f"INSERT INTO {table_name} (time, spaces) VALUES ('{time[i]}', {spaces[i]})")
    else:
        # Table does not exist, create table and insert data
        curs.execute(f"CREATE TABLE {table_name} (id INT, time VARCHAR(20), spaces INT)")
        for i in range(len(time)):
            curs.execute(f"INSERT INTO {table_name} (id, time, spaces) VALUES ({i+1}, '{time[i]}', {spaces[i]})")

    curs.close()
    db.commit()
    db.close()





if __name__ == '__main__':
    try:#Datatype = .json
        df = pd.read_json(f'{gd.data_attributes.dir_path}/{num_list[-1]}.json')
        new = pd.DataFrame()

        time = []
        name = []
        spaces = []

        for i in range(len(df['ParkingAvailabilities'])):
                name.append(df['ParkingAvailabilities'][i]['CarParkName']['Zh_tw'].strip())
                spaces.append([df['ParkingAvailabilities'][i]['AvailableSpaces']])

        for i in range(len(df['UpdateTime'])):
            k = re.split('[T/+]',df.loc[i,'UpdateTime'])
            k.pop()
            time.append('_'.join(k))

        new['UpdateTime'] = time
        new['ParklotName'] = name
        new['ParkingSpaces'] = spaces

        #new.to_json(f'{os.getcwd()}/data/data_storage/Parklot_Avaliable/proceeded_data/{num_list[-1]}.json') #write file
        sql_write(name,time,spaces)
        print(f"Data {num_list[-1]} reconstruct successfully.")
    except:
        print(f"Error with restructing the file {num_list[-1]} into database which listed in _0.txt")




'''

'''

''' #Datatype = .txt
# try :
#     raw = open(f'{gd.data_attributes.dir_path}/{num_list[-1]}',mode = 'r',encoding = 'utf-8').read()
#     #print(raw)
#     raw = json.loads(raw)
#     for park_lot in raw['ParkingAvailabilities']:
#         #print(f'{park_lot["CarParkName"]["Zh_tw"]}-剩餘停車位 : {str(park_lot["TotalSpaces"])}')  #Printing all the proceeded data on the prompt
#         proceeded_data.append([f'{park_lot["CarParkName"]["Zh_tw"]}',f'Total space :{str(park_lot["TotalSpaces"])}',])
    
#     #print(proceeded_data)
#     open(f'{gd.data_attributes.dir_path}/proceeded_data/{num_list[-1]}',mode = 'w',encoding = 'utf-8').write(str(proceeded_data))
#     print(f'data {num_list[-1]} successfully loaded')
# except:
#     print("Error with finding the data with data_name in the '_0.txt'")
'''