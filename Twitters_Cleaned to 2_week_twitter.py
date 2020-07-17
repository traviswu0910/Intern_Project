#Cleaned data to two_week_twitter

import json
import pandas as pd
import datetime

time_range = pd.date_range('20180101','20200713') #想要輸出多久的資料

for time in time_range:
	two_week_range = pd.date_range(pd.to_datetime(time)-pd.to_timedelta(2,'w'),time,freq='d')
	df = []
	for days in two_week_range:
		days = days.strftime('%Y%m%d')
		try:
			with open(f'./All_Data/Twitters_CleanedData/{days}.json','r') as f:
				x=json.load(f)
			df.extend(x)
		except:pass
	with open(f'./All_Data/2_weeks_twitters/{days}.json','w') as file:
		json.dump(df,file)

