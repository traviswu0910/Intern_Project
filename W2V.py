import pandas as pd
import numpy as np
import glob
from Module_Clean import Clean
from tqdm import tqdm
import re
import pickle
from gensim.models import Word2Vec
import json

#API RSS新聞欄位命名名稱不同，因此統一命名
def rename(df):
    df=df.rename(columns={'url':'link','publishedAt':'pubdate','pubDate':'pubdate'})
    return df

#將title 清理，去除關鍵字等等
def clean_title(x):
    x=Clean(x)
    x.Capitalize()
    x.DeletePunctuation()
    x.DeleteRedundant()
    return x.Text
#讀取存好的兩周新聞
def read(date):
    return pd.read_pickle(f'./All_Data/2_weeks_news/{date}')


########generate 2 weeks news 每天都抓前兩周所有新聞，存成pickle

def gen_2week_news(start,end):
    '''
    example：start = '2019-01-01', end = '2020-05-25'
    '''
    total_date = pd.date_range(start,end,freq='d')
    
    for date in tqdm(total_date):
        two_week_range = pd.date_range(date-pd.to_timedelta(2, 'w'),date,freq='d')
        df=pd.DataFrame()
        for days in two_week_range:
            day = days.strftime('%Y%m%d')
            if day not in ['20180222','20181003']:
                files = glob.glob(f'./All_Data/News_CleanedData/{day}.json')
                for file in files:
                    x=pd.read_json(file)
                    x=rename(x)
                    if 'author' not in x:
                        x['author']=''
                    df= pd.concat([df,x])
        df = df.drop_duplicates('title')
        df = df.dropna(subset=['title'])
        df['title_cleaned'] = df['title'].apply(clean_title)
        x=date.strftime('%Y%m%d')
        df.to_pickle(f'./2_weeks_news/{x}')
########找出每天兩周新聞標題的關鍵字
def gen_keywords(start,end):
    total_date = pd.date_range(start,end,freq='d')
    ans = {}
    for dates in tqdm(total_date):
        ans_list = []
        all_similar = []
        date = dates.strftime('%Y%m%d')
        df = read(date)
        string = [' '.join(df.title_cleaned.values).split()]
        model = Word2Vec(string)
        
        for all_word in model.wv.vocab.keys():
            similar = model.wv.most_similar(all_word)
            for i in similar:
                all_similar.append(i[0])
        value,count = np.unique(all_similar,return_counts=True)
        
        count_sort_ind = np.argsort(-count)
        value = value[count_sort_ind] ; count = count[count_sort_ind]
        for i in range(len(count)):
            ans_list.append( (value[i],count[i]/len(model.wv.vocab.keys())) )
        ans[date] = ans_list
    with open('top_news_keys','wb')as f:
        pickle.dump(ans,f)
        
########找出含有關鍵字的新聞前三大關鍵字)
def gen_topnews(start,end):
    with open('top_news_keys','rb')as f:
        key = pickle.load(f)
    total_date = [x.strftime('%Y%m%d') for x in pd.date_range(start,end,freq='d')]
    for date in tqdm(total_date):
        keys = [i for i,j in key[date][:3]]
        df = read(date)
        for i in range(3):
            df[f'count{i+1}'] = df.title_cleaned.apply(lambda x:x.split().count(keys[i]))
        top_news_1 = json.loads(df.query('count1 > 0').to_json(orient = 'records'))
        top_news_1.insert(0,keys[0])
        top_news_2 = json.loads(df.query('count2 > 0').to_json(orient = 'records'))
        top_news_2.insert(0,keys[1])
        top_news_3 = json.loads(df.query('count3 > 0').to_json(orient = 'records'))
        top_news_3.insert(0,keys[2])
        
        with open(f'./All_Data/top_news/{date}_1.json','w')as f:
            json.dump(top_news_1,f)
        with open(f'./All_Data/top_news/{date}_2.json','w')as f:
            json.dump(top_news_2,f)
        with open(f'./All_Data/top_news/{date}_3.json','w')as f:
            json.dump(top_news_3,f)
    

        
if __name__ == '__main__':      
    
    gen_2week_news('2018-01-02','2020-05-26')
    gen_keywords('2018-01-02','2020-05-26')
    gen_topnews('2018-01-02','2020-05-26')
    # gen_2week_news('2018-01-14','2018-01-15')
    # gen_keywords('2018-01-14','2018-01-15')
    # gen_topnews('2018-01-14','2018-01-15')
