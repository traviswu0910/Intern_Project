import pandas as pd
import json
import ast
import os
from datetime import datetime, timedelta


with open('./All_Data/Twitters_Rawdata/list_try.txt') as f: #open twitter author list
	name_list = f.readline()
	name_list = ast.literal_eval(name_list)
def find_delete_tweet(date):
	print('Date:', date)
	# after_data
	with open ('./All_Data/Twitters_ParsedData/{}_API.json'.format(date),'r') as f: #open after day parsed data
		after_data = json.load(f)

	date_minus_one = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
	with open ('./All_Data/Twitters_ParsedData/{}_API.json'.format(date_minus_one),'r') as f: #open before day parsed data
		previous_data = json.load(f)

	for name in name_list:
		after_date = []
		for i in range(0,len(after_data)):
			if after_data[i]['Name'] == name:
				after_date.append(after_data[i])
		#previous_data

		previous_date = []
		for i in range(0,len(previous_data)):
			if previous_data[i]['Name'] == name:
				previous_date.append(previous_data[i])
		diff=[]
		find_if_first_deleted=[]
		missing_tweet = []
		for i in range(0,len(after_date)):
			for j in range(0,len(previous_date)):
				if after_date[i]['Text'] == previous_date[j]['Text'] and after_date[i]['Time'] == previous_date[j]['Time'] and after_date[i]['Name'] == previous_date[j]['Name']:
					if after_date[i]['Name']=='bespokeinvest':continue # bespokeinvest有400則，先忽略
					result = i-j
					find_if_first_deleted.append(j)
					if len(diff)==0:
						diff.append(result)
					else:
						if result != diff[-1]:
							for count in range(0,diff[-1]-result):
								missing_tweet.append(previous_date[j-count-1])
						diff.append(result)
					# print(i,j)
		if len(find_if_first_deleted) != 0:
			if find_if_first_deleted[0] != 0: #看前一天第一則是否為零，若不為零則就是被刪除
				for i in range(0,find_if_first_deleted[0]):
					missing_tweet.append(previous_date[i])
		# print(find_if_first_deleted[0])
					# print(result)
		# print(diff)
		if len(missing_tweet)==0:
			print('{}:\nThere\'s no deleted tweet'.format(name))
		else:
			print('{}:\n'.format(name),missing_tweet)
			with open('./All_Data/Twitter_deleted/{}_{}.json'.format(name,date),'w') as f: 
				json.dump(missing_tweet,f)
				print(name,date) #印出存誰的資訊、日期
	return missing_tweet

######deal with data from 0705 to 0720#########

# time_list=[]
# start_date = datetime.strptime('2020-07-05','%Y-%m-%d')
# while start_date <= datetime.strptime('2020-07-20','%Y-%m-%d'):
# 	result = start_date.strftime('%Y-%m-%d')
# 	time_list.append(result)
# 	start_date+=timedelta(days=1)

# for time in time_list:
# 	find_delete_tweet(time)


if __name__ == '__main__':
	# find_delete_tweet()