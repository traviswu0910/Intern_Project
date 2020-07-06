import pandas as pd
import json
import numpy as np
import glob
import re
from tqdm import tqdm

# 之前抓歷史資料時，沒有加入pubDate。wsj當天抓的新聞就只有當天的，所以直接用檔名當作pubdate
history_news = glob.glob('./All_Data/News_ParsedData/*_WSJ.json')
for i in history_news:
    x=re.findall(r'\d*-\d*-\d*',str(i))[0]
    with open(i,'r')as f:
        news = json.load(f)
    for j in range(len(news)) :
        news[j].update({'pubdate':x})
        del news[j]['pubDate']
    with open(i,'w')as f:
        json.dump(news,f)


# 將全部新聞併起來並且sort pubdate
def rename(df):
    df=df.rename(columns={'url':'link','publishedAt':'pubdate','pubDate':'pubdate'})
    return df
all_news = glob.glob('./All_Data/News_ParsedData/*.json')

df = pd.DataFrame()
for news in tqdm(all_news):
    source = re.split(r'\d*-\d*-\d*_',news)[-1].replace('.json','')
    with open(news,'r')as f:json_file = json.load(f)
    if json_file == []:
        continue
    else:
        x = pd.read_json(news)
        x = rename(x)
        x['source'] = source
        x['pubdate'] = x['pubdate'].apply(pd.to_datetime)
        df = df.append(x)
        df.drop_duplicates('title',inplace = True)
df['pubdate'] = df['pubdate'].apply(lambda x:x.strftime('%Y%m%d'))
current = df['pubdate'].apply(lambda x:True if int(x)>=20180101 else False)
df = df[current]
df = df.sort_values('pubdate')
# '20180222', '20181003' 這兩天是沒有新聞的

#將每天新聞存成json檔
for date in df.pubdate.drop_duplicates():
    eachday_news = df.query('pubdate == @date')
    eachday_news = json.loads(eachday_news.to_json(orient = 'records'))
    with open(f'./All_Data/News_CleanedData/{date}.json','w')as f:
        json.dump(eachday_news,f)

