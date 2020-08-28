# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 16:07:17 2020

@author: ZuroChang
"""

import json
import pandas as pd
import datetime as dt

fullName = pd.read_json("./All_Data/Reference/InfoCodeToFullName.json").set_index('InfoCode')

method_list = {
    'pph_1':'news_PortfolioList_AbovePositive5',
    'pph_2':'news_PortfolioList_BelowNegative5',
    'pph_3':'news_PortfolioList_WeekAbovePositive10',
    'pph_4':'news_PortfolioList_WeekBelowNegative10',
    'pph_5':'news_PortfolioList_MonthAbovePositive20',
    'New': 'New'
}

class News:
    def get_top_news(day, ran, kw):
        def get_top_news_ind(which_day, num, keyword):
            which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
            with open(f'./All_Data/top_news/{which_day}_{num}.json')as f:
                file = json.load(f)
                key = file[0]
                news = file[1:]
            
            news = pd.DataFrame.from_records(news)
            news = news[['title','link','pubdate','source']]
            news = json.loads(news.to_json(orient='records'))
            
            if keyword != '':
                keyword = keyword.upper()
                choose = []
                for i in news:
                    title = i['title'].upper().split()
                    if keyword in title:
                        choose.append(i)
                news = choose
            
            return key,news
        news_lists = []
        for i in ran:
            k, n = get_top_news_ind(day, i, kw)
            news_lists.append({
                    'key': k,
                    'list': n,
                })
        return news_lists

    
    def get_portfolio_news(which_day,method,keyword):
        which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
        method = method_list[method]
        print('method: {}'.format(method))
        try:
            with open(f'./All_Data/portfolio_news/{method}_{which_day}.json')as f:
                file = json.load(f)
            if len(file)>1:
                portfolio = file[0]
                news = file[1:]
                
                news = pd.DataFrame.from_records(news)
                news['title_company'] = news['title_company'].apply(lambda x:x[0])
                news = news.sort_values(['title_company','pubdate','source'],ascending=[True,False,True])
                news = news[['title','link','pubdate','source','title_company']]
                news = json.loads(news.to_json(orient='records'))
            #當該投組 沒有新聞時
            else :
                portfolio = file[0]
                news = ''
                
            if keyword != '':
                keyword = keyword.upper()
                choose = []
                for i in news:
                    title = i['title'].upper().split()
                    if keyword in title:
                        choose.append(i)
                news = choose
            
            return portfolio,news
        except:
            portfolio = ''
            news = ''
            
            return portfolio,news

class Twitter:
    def get_top_twitter(day, ran):
        def get_top_twitter_ind(which_day,num):
            which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
            with open(f'./All_Data/top_twitters/{which_day}_{num}.json')as f:
                file = json.load(f)
                key = file[0]
                twitter = file[1:]
        
            return key, twitter
        lists = []
        for i in ran:
            k, l = get_top_twitter_ind(day, i)
            lists.append({
                    'key': k,
                    'list': l,
                })
        return lists
    
    def get_hot_twitter(day):
        day = pd.to_datetime(day).strftime('%Y%m%d')
        accounts = [
            'FundyLongShort',
            'SmallCapLS',
            'ShortSightedCap',
        ]
        files = []
        for account in accounts:
            with open('./All_Data/top_author_twitters/{}+{}.json'.format(account, day), 'r') as f:
                files.append(json.load(f))
        return accounts,files

class Chart:
    def get_chart_data(which_day,method):
        which_day = pd.to_datetime(which_day).strftime('%Y%m%d')
        method = method_list[method].replace('news_PortfolioList_','')
        
        data = pd.read_json(f'./All_Data/UIData/PortfolioPerformance_{method}_{which_day}.json')
        data['company'] = data['InfoCode'].apply(lambda x:fullName.loc[int(x)][0])
        data['Single']=data['Single']*360
        data=data.rename(columns={'Single':'day','Nearest7DaysAnnualSingle':'week',
                'Nearest30DaysAnnualSingle':'month','Nearest365DaysAnnualSingle':'year'})
        data = data[['company','day','week','month','year']]
        
        if len(data)>20:
            if method=='AbovePositive5':
                data = data.sort_values('day', ascending=False).iloc[:20,:]
            elif method=='BelowNegative5':
                data = data.sort_values('day', ascending=True).iloc[:20,:]
            elif method=='WeekAbovePositive10':
                data = data.sort_values('week', ascending=False).iloc[:20,:]
            elif method=='WeekBelowNegative10':
                data = data.sort_values('week', ascending=True).iloc[:20,:]
            elif method=='MonthAbovePositive20':
                data = data.sort_values('month', ascending=False).iloc[:20,:]
        else:
            if method=='AbovePositive5':
                data = data.sort_values('day', ascending=False)
            elif method=='BelowNegative5':
                data = data.sort_values('day', ascending=True)
            elif method=='WeekAbovePositive10':
                data = data.sort_values('week', ascending=False)
            elif method=='WeekBelowNegative10':
                data = data.sort_values('week', ascending=True)
            elif method=='MonthAbovePositive20':
                data = data.sort_values('month', ascending=False)
        data=json.loads(data.to_json(orient='records'))
        return data