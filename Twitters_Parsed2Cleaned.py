#Parsed data to Cleaned data
import pandas as pd
import json
import datetime
import glob

#合併parsed data
data = pd.DataFrame()
all_txt_files = glob.glob('./All_Data/ParsedData/*.txt')
for file in all_txt_files:
    a = pd.read_json(file)
    data = data.append(a)
#只取推文、作者、時間
b = data[['Name','Time','Text']]
c = b.sort_values('Time')

#將時間改成yyyymmdd
c['Time'] = pd.to_datetime(c['Time']).apply(lambda x:x.strftime('%Y%m%d'))


#將相同推文內容去除
c.drop_duplicates('Text',inplace=True)


#取20170101到20200601的資料
time_range = pd.date_range('20170101','20200601')
time_range = time_range.strftime('%Y%m%d')

#建json檔
for time in time_range:
    df = c.query('Time == @time')
    ans = json.loads(df.to_json(orient='records'))
    with open(f'./All_Data/CleanedData/{time}.json','w') as f:
        json.dump(ans,f)




