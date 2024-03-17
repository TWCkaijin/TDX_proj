import os
import json 





if __name__ == '__main__':
    with open(file = '1.json',encoding = 'utf-8',mode ='r+') as f:
        data = json.load(f)
        x = data['PA']
        for i in x :
            for j in x[f'{i}']:
                #print(j)
                try:
                    rounded = round(x[f'{i}'][f'{j}']['AS'],2)
                    x[f'{i}'][f'{j}']['AS'] = rounded
                    #print(f"{x[f'{i}']}success")
                except Exception as e:  
                    print(e)




            '''
                print(f"{j['AS']}{type(j['AS'])}")

                rounded = round(int(j['AS']),2)
                data['PA'][x.index(i)][i.index(j)] = rounded'''
            
        
        f.truncate(0)
        f.seek(0)
        json.dump(data,f,indent = 4)