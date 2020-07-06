#推文內容丟入W2V找出前四名

import pandas as pd
import json
import glob
from tqdm import tqdm
from gensim.models import Word2Vec
import pickle
import numpy as np
from Module_Clean import Clean

#清洗資料
def clean_text(x):
    #print(text)
    #print('-------')
    text = Clean(x)
    text.Capitalize()
    text.DeletePunctuation()
    text.DeleteRedundant()
    #print(text)
    return text.Text


def gen_keywords(start,end):
    total_date = pd.date_range(start,end,freq='d')
    ans = {}
    for dates in tqdm(total_date):
        #print(dates)
        ans_list = []
        all_similar = []
        date = dates.strftime('%Y%m%d')
        try:
            df = pd.read_json(f'./All_Data/2_weeks_twitters/{date}.json')
            df['clean_text'] = df.Text.apply(clean_text)
            string = [ ' '.join(df.clean_text.values).split() ]
            model = Word2Vec(string,min_count=2) #min_count多少代表這個字最少要出現幾次
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
        except:pass
    with open('top_news_keys','wb')as f:
        pickle.dump(ans,f)
if __name__ == '__main__':   
    gen_keywords('2018-01-01','2020-06-01')