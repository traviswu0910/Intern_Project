import pandas as pd
import json
import ast
import glob
import os
from datetime import datetime
import random
from Module_Clean import Clean

fullName = pd.read_json("./All_Data/Reference/InfoCodeToFullName.json").set_index('InfoCode')
synonym = pd.read_json("./All_Data/Reference/Synonym.json").set_index('InfoCode')

def get_data(Name,Strategy,date=datetime.today().strftime('%Y%m%d')): #生infocode, 輸出infocode list
	with open ('./All_Data/Reference/InfoCodeToFullName.json') as f:
		x = pd.read_json(f)
	Info_list = x['InfoCode'].sample(n=10,random_state=Strategy)
	Info_list = Info_list.to_json(orient='values')
	# with open('{}_{}_{}.txt'.format(Name,Strategy,date),'w') as f:
	# 	f.write(Info_list)
	if os.path.exists('{}_{}.json'.format(str(Name),Strategy)) == False:
		with open('{}_{}.json'.format(Name,Strategy),'w') as f:
			hist_port=[]
			json.dump(hist_port,f)
	with open('{}_{}.json'.format(Name,Strategy),'r') as f:
		hist_port = json.load(f)
		incase_dup=[] #確保日期不會重複
		if len(hist_port)==0:
			dic = {}
			dic[date]=eval(Info_list)
			hist_port.append(dic)
		for i in range(0,len(hist_port)):
			incase_dup.append(list(hist_port[i].keys())[0])
		if date not in incase_dup:
			dic = {}
			dic[date]=eval(Info_list)
			hist_port.append(dic)
	with open('./All_Data/api_port/{}_{}.json'.format(Name,Strategy),'w') as f:
		json.dump(hist_port,f)
		# f.write(str(dic))
	print(hist_port)
	return hist_port


def Info2PortfolioNews_element(Name,Strategy): # infocode list轉need info
	with open ('./All_Data/Reference/InfoCodeToFullName.json') as f:
		x = pd.read_json(f)
	with open ('./All_Data/api_port/{}_{}.json'.format(Name,Strategy),'r') as f:
		y = json.load(f)

	show_re = []
	for j in range(0,len(y)):
		Info_list = list(y[j].values())[0]
		dic={'Date': int(list(y[j].keys())[0])}
		# print(dic)
		temp=[]
		for i in x['InfoCode']:
			if i in Info_list:
				data = x.loc[x['InfoCode']== i].values.tolist()
				# data[0].insert(0,20200716)
				# print(data[0][1])
				temp.append(data)
		# print(temp)
				new_list = [x[0] for x in temp]

		result=[]
		for i in range(0,len(new_list)):
			if i == 0:
				dic['InfoCode']=[]
				dic['FullName']=[]
			for j in range(0,len(new_list[i])):
				if j==0:
					# dic['InfoCode']=new_list[i][j]
					dic['InfoCode'].append(new_list[i][j])
				else:
					# dic['FullName']=new_list[i][j]
					dic['FullName'].append(new_list[i][j])
		result.append(dic)
		show_re.append(dic)
	# print(result)
		with open('./All_Data/api_port/{}_{}_{}.json'.format(Name,Strategy,dic['Date']),'w') as f:
			json.dump(result,f)
	print(show_re)

	return show_re
# get_data('travis0825',6)
# Info2PortfolioNews_element('travis0825',6)

# print(fullName)

def get_syn_intersection(df,syn):
    '''
    用來比對新聞標題是否包含公司名稱，並且將包含哪些公司名稱存成list
    input為dataframe
        df:新聞
        syn:公司名稱、同義詞
    '''
    #special word 將兩個字併起來，並且中間加上 _ 以便找尋 synonym，如AAPL US併成AAPL_US
    def get_special_word(news):
        news_title = news.split()
        special_word = Clean(news);special_word.Separate(2);special_word = special_word.Text
        special_word = list(map(lambda x:x.replace(' ','_'),special_word))
        news_title.extend(special_word)
        return news_title
    df['title_add_special'] = df['title_cleaned'].apply(lambda x:get_special_word(x))
    df = df.reset_index(drop=True)
    def get_company(news_title):
        intersection=[]
        title = set(news_title)
        for co in syn.index:
            syn_word = set(syn.loc[co].Synonym)
            #如果標題中含有公司的同義字，就把公司名稱加入list中
            if len(title & syn_word)>0:
                intersection.extend([fullName.loc[co].Name])
        return intersection

    df['title_company'] = df['title_add_special'].apply(lambda x:get_company(x))
    df['count'] = df['title_company'].apply(lambda x:1 if len(x)>0 else 0)
    del df['title_add_special']
    return df


df = pd.read_json('./All_Data/api_port/travis0825_6_20200825.json').set_index('Date')

for date in df.index:
	portfolio = df.loc[date].InfoCode
	port_list=[]
	for i in portfolio:
		if i in synonym.index.to_list():
			port_list.append(i)
	portfolio = port_list
	# print(portfolio)

	portfolio_list = fullName.loc[portfolio].Name.to_list()
	# print(portfolio_list)

	synonym_list = synonym.loc[portfolio]
	# print(synonym_list)

	news = pd.read_json('/Users/tianyouwu/Desktop/Intern/All_Data/2_weeks_news/20200505.json').reset_index(drop=True)
	portfolio_news = get_syn_intersection(news,synonym_list)
	portfolio_news = portfolio_news.query('count == 1')
	portfolio_news.sort_values(['pubdate','source'],ascending=False)
	ans = json.loads(portfolio_news.to_json(orient = 'records'))
	ans.insert(0,portfolio_list)
	print(ans)
	with open ('./All_Data/api_port/news_6_20200825.json','w') as f:
		json.dump(ans,f)


















