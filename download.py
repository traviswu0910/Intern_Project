import pandas as pd
import json
from datetime import datetime
from os import path, mkdir

fPath = './All_Data'

strategy_list = {
    'pph_1':'news_PortfolioList_AbovePositive5',
    'pph_2':'news_PortfolioList_BelowNegative5',
    'pph_3':'news_PortfolioList_WeekAbovePositive10',
    'pph_4':'news_PortfolioList_WeekBelowNegative10',
    'pph_5':'news_PortfolioList_MonthAbovePositive20'
}


def package(date, strategy_name, keyword):
	print(strategy_name)
	p = path.join(fPath,'Download_Data')
	if not path.isdir(p):
		mkdir(p)
	date = date.replace('-','')
	result={}
	def top_news_package(date,keyword):
		top_news_package_dic={}
		del_key_list=['content','description','feedburner:origlink','guid','metadata:id',
						'metadata:sponsored','metadata:type','urlToImage','title_cleaned',
						'count1','count2','count3']
		for num in range(1,4):
			try:
				with open(fPath+'/top_news/{}_{}.json'.format(date,num),'r') as f:
					top_news_file = json.load(f)
				# print(top_news_file[1])
				for i in range(len(top_news_file)):
					if i == 0:
						top_news_package_dic[top_news_file[i]]=[]
					else:
						if keyword == '':
							for key in del_key_list:
								if key in top_news_file[i]:
									del top_news_file[i][key]
							top_news_package_dic[top_news_file[0]].append(top_news_file[i])
						else:
							keyword = keyword.upper()
							if keyword in top_news_file[i]['title'].upper().split():
								# print('hihi')
								# print(top_news_file[num]['title_cleaned'])
								# print(num,i)
								for key in del_key_list:
									if key in top_news_file[i]:
										del top_news_file[i][key]
								top_news_package_dic[top_news_file[0]].append(top_news_file[i])


			except:pass
		# print(top_news_package_dic)
		return top_news_package_dic #return dict {'A':['author':...,]}
	result['Top_News'] = top_news_package(date,keyword)

	def top_twitters_package(date):
		top_twitters_package_dic={}
		del_key_list = ['clean_text','count1','count2','count3','count4']
		for num in range(1,5):
			try:
				with open(fPath+'/top_twitters/{}_{}.json'.format(date,num),'r') as f:
					top_twitters_file = json.load(f)
					# print(top_twitters_file)
					for i in range(len(top_twitters_file)):
						if i == 0:
							top_twitters_package_dic[top_twitters_file[i]]=[]
						else:
							for key in del_key_list:
								if key in top_twitters_file[i]:
									del top_twitters_file[i][key]
							top_twitters_package_dic[top_twitters_file[0]].append(top_twitters_file[i])
			except:pass
		# print(top_twitters_package_dic)
		return top_twitters_package_dic # return {'A':['Name':...,]}
	result['Top_Twitters'] = top_twitters_package(date)

	def portfolio_performance_package(date,strategy_name):
		strategy_name= strategy_list[strategy_name].split('_')[2]
		# print(strategy_name)
		portfolio_performance_package_dic={}
		del_key_list = ['AnnualConti','AnnualSingle','Conti','Nearest30DaysSingle','Nearest365DaysSingle',
						'Nearest7DaysSingle','Period','Price','created','id']
		# print('PortfolioPerformance_{}_{}'.format(strategy_name,date))
		try:
			with open(fPath+'/UIData/PortfolioPerformance_{}_{}.json'.format(strategy_name,date),'r') as f:
				portfolio_performance_file = json.load(f)
				# print(portfolio_performance_file[0]['InfoCode'])
				for i in range(len(portfolio_performance_file)):
					# print(i)
					for key in del_key_list:
						if key in portfolio_performance_file[i]:
		# 					# print(key)
		# 					# print('hihi')
							del portfolio_performance_file[i][key]
					# print(portfolio_performance_file[i]['InfoCode'])
					portfolio_performance_package_dic[portfolio_performance_file[i]['InfoCode']]=portfolio_performance_file[i]
					# print('123')
		except:pass
		# print(portfolio_performance_package_dic)
		return portfolio_performance_package_dic # return dict {'A':['InfoCode':...,]}
	result['Portfolio_Performance'] = portfolio_performance_package(date,strategy_name)	

	def portfolio_news_package(date,strategy_name,keyword):
		strategy_name= strategy_list[strategy_name]
		portfolio_news_package_dic={}
		del_key_list=['author','content','description','feedburner:origlink','guid','metadata:id',
						'metadata:sponsored','metadata:type','urlToImage','title_cleaned','count']
		try:
			with open(fPath+'/portfolio_news/{}_{}.json'.format(strategy_name,date),'r') as f:
				portfolio_news_file = json.load(f)
			# print(portfolio_news_file)
			for i in range(len(portfolio_news_file)):
				if i == 0:
					portfolio_news_package_dic['portfolio_news']=[]
				else:
					portfolio_news_file[i]['Company_Name'] = portfolio_news_file[i].pop('title_company')
					if keyword == '':
						for key in del_key_list:
							if key in portfolio_news_file[i]:
								del portfolio_news_file[i][key]
						portfolio_news_package_dic['portfolio_news'].append(portfolio_news_file[i])
					else:
						keyword = keyword.upper()
						if keyword in portfolio_news_file[i]['title'].upper().split():
							for key in del_key_list:
								if key in portfolio_news_file[i]:
									del portfolio_news_file[i][key]
							portfolio_news_package_dic['portfolio_news'].append(portfolio_news_file[i])

		except:pass
		# print(portfolio_news_package_dic)
		return portfolio_news_package_dic # return {'A':[{'link':...,}]}
	result['Portfolio_News'] = portfolio_news_package(date,strategy_name,keyword)

	def portfolio_list_package(date):
		portfolio_list_package_dic={}
		try:
			with open(fPath+'/UIData/PortfolioList_AbovePositive5.json','r') as f:
				portfolio_list_file = json.load(f)
				# print(portfolio_list_file)
			for i in range(len(portfolio_list_file)):
				if str(portfolio_list_file[i]['Date']) == date:
					portfolio_list_package_dic['Company_Name'] = portfolio_list_file[i]['FullName']
		except:pass
		
		# print(portfolio_list_package_dic)
		return portfolio_list_package_dic # return {'A':['Compname','']}
	result['Portfolio_Information'] = portfolio_list_package(date)

	def top_author_twitter_package(date):
		top_author_twitters_dic = {}
		author_list = ['FundyLongShort','SmallCapLS','ShortSightedCap']
		try:
			for author in author_list:
				with open(fPath+'/top_author_twitters/{}+{}.json'.format(author,date),'r') as f:
					top_author_twitters_file = json.load(f)
				# print(top_author_twitters_file)
				top_author_twitters_dic[author] = []
				for i in range(len(top_author_twitters_file)):
					top_author_twitters_dic[author].append(top_author_twitters_file[i])
		except:pass

		# print(top_author_twitters_dic)

		return top_author_twitters_dic # return {'A':[{'Name':...,}]}
	result['Top_Twitters_Author'] = top_author_twitter_package(date)
	strategy_name= strategy_list[strategy_name]
	with open(fPath+'/Download_Data/{}_{}_{}.json'.format(date, strategy_name, keyword), 'w') as f:
		json.dump(result,f)
	return result

# print(package('20200505','pph_2','')['Portfolio_Perfomance'].keys())