
#48 datas each day

#delcare
data_dict = dict()

#Read file
with open(r'C:\Users\ADMIN\Documents\NSYSU\GDSC\Parklot_Avaliable\proceeded_data\2023_10_25_1.txt', encoding = 'utf-8', mode = 'r' ) as f:
    data = f.read()

# for i in range(100):

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


# self-define output
# print(data_dict['重平'])
