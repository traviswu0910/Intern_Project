#輸出三個私募基金推特

import json
import pandas as pd


data = pd.DataFrame()
time_range = pd.date_range('20180101','20200526')
time_range = time_range.strftime('%Y%m%d')


for date in time_range:
	with open(f'./All_Data/2_weeks_twitters/{date}.json') as file:
		data = pd.read_json(file)
		df = data.query('Name == "FundyLongShort"') #以FundyLongShort為例
		ans = json.loads(df.to_json(orient='records'))
		print(date)
		print(ans)
		with open(f'./All_Data/top_author_twitters/FundyLongShort+{date}.json','w') as f:
			json.dump(ans,f)


#print(time_range)




