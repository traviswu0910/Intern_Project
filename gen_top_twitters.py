#從gen_top_twitters_keys中選出的關鍵字，再去選出推文

import pickle
import pandas as pd
from tqdm import tqdm
import json
from Module_Clean import Clean



def clean_text(x): #清洗資料
    text = Clean(x)
    text.Capitalize()
    text.DeletePunctuation()
    text.DeleteRedundant()
    # print(text.Text)
    return text.Text
with open('top_news_keys','rb')as f:
    key = pickle.load(f)


def gen_topnews(start,end):
    with open('top_news_keys','rb')as f:
        key = pickle.load(f)
    total_date = [x.strftime('%Y%m%d') for x in pd.date_range(start,end,freq='d')]
    for date in tqdm(total_date):
        #取前三大關鍵字
        keys = [i for i,j in key[date][:4]]
        df = pd.read_json(f'./All_Data/2_weeks_twitters/{date}.json')
        df['clean_text'] = df.Text.apply(clean_text)
        for i in range(4):
            try:
                df[f'count{i+1}'] = df.clean_text.apply(lambda x:x.split().count(keys[i]))
            except:pass
        df=df.sort_values(['Time','Name'],ascending=False)
        #將關鍵字填入list中第一項，之後UI抓值用
        try:
            top_twitters_1 = json.loads(df.query('count1 > 0').to_json(orient = 'records'))
            top_twitters_1.insert(0,keys[0])
        except:pass
        try:
            top_twitters_2 = json.loads(df.query('count2 > 0').to_json(orient = 'records'))
            top_twitters_2.insert(0,keys[1])
        except:pass
        try:    
            top_twitters_3 = json.loads(df.query('count3 > 0').to_json(orient = 'records'))
            top_twitters_3.insert(0,keys[2])
        except:pass
        try:
            top_twitters_4 = json.loads(df.query('count4 > 0').to_json(orient = 'records'))
            top_twitters_4.insert(0,keys[3])
        except:pass
        
        with open(f'../top_twitters/{date}_1.json','w')as f:
            json.dump(top_twitters_1,f)
        with open(f'../top_twitters/{date}_2.json','w')as f:
            json.dump(top_twitters_2,f)
        with open(f'../top_twitters/{date}_3.json','w')as f:
            json.dump(top_twitters_3,f)
        with open(f'../top_twitters/{date}_4.json','w')as f:
            json.dump(top_twitters_4,f)



if __name__ == '__main__':   
    gen_topnews('2018-01-01','2020-05-26')
    