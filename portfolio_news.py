import pandas as pd
import json
from tqdm import tqdm
from Clean import Clean

def read(date):
    return pd.read_pickle(f'./All_Data/2_weeks_news/{date}')

def get_portfolio_news(df,syn):
    #special word 將兩個字併起來，並且中間加上 _ 以便找尋 synonym，如AAPL US併成AAPL_US
    def get_special_word(news):
        a=news.split()
        special_word = Clean(news);special_word.Separate(2);special_word = special_word.Text
        special_word = list(map(lambda x:x.replace(' ','_'),special_word))
        a.extend(special_word)
        return a
    df['title_add_special'] = df['title_cleaned'].apply(lambda x:get_special_word(x))
    df = df.reset_index(drop=True)
    def get_company(x):
        ans=[]
        title = set(x)
        for co in syn.index:
            syn_word = set(syn.loc[co].Synonym)
            if len(title & syn_word)>0:
                ans.extend([fullName.loc[co].Name])
        return ans
    df['title_company'] = df['title_add_special'].apply(lambda x:get_company(x))
    df['count'] = df['title_company'].apply(lambda x:1 if len(x)>0 else 0)
    del df['title_add_special']
    return df

fullName = pd.read_json("./All_Data/Reference/InfoCodeToFullName.json").set_index('InfoCode')
synonym = pd.read_json("./All_Data/Reference/Synonym.json").set_index('InfoCode')

strategies = ['PortfolioList_AbovePositive5','PortfolioList_BelowNegative5',
            'PortfolioList_WeekAbovePositive10','PortfolioList_WeekBelowNegative10']

for strategy in tqdm(strategies):
    df=pd.read_json(f'./All_Data/UIData/{strategy}.json').set_index('Date')
    for date in tqdm(df.index):
        portfolio = df.loc[date].InfoCode
        if len(portfolio)==0:
            continue
        else :
            #########有些明淇選出的股票不在synonym中，有可能是明淇在抓SP500時已經更新成分股了
            port_list = []
            for i in portfolio:
                if i in synonym.index.to_list():
                    port_list.append(i)
            portfolio = port_list
            #############################
            portfolio_list = fullName.loc[portfolio].Name.to_list()#每天portfolio 有哪幾間公司
            synonym_list = synonym.loc[portfolio]
            news = read(date).reset_index(drop=True)
            portfolio_news = get_portfolio_news(news,synonym_list)
            portfolio_news = portfolio_news.query('count == 1')
            ans = json.loads(portfolio_news.to_json(orient = 'records'))
            ans.insert(0,portfolio_list)
            with open(f'./portfolio_news/news_{strategy}_{date}.json','w')as f:
                json.dump(ans,f)