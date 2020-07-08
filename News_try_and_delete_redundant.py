#抓贅字用，修正清洗資料用
import pickle
import pandas as pd

with open('top_news_keys','rb')as f:
	data = pickle.load(f)

# total_date = pd.date_range('20180101','20200526',freq='d')
# total_date = total_date.strftime('%Y%m%d')
# for date in total_date:
# 	print(data[date][:3])


for i in data:
	for x,y in data[i][:3]:
		print(x)