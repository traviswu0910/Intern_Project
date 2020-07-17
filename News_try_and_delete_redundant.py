#抓贅字用，修正清洗資料用
#也可看時間序列變化
import pickle
import pandas as pd

with open('top_news_keys','rb')as f:
	data = pickle.load(f)

def show_key_words_with_score():
	total_date = pd.date_range('20180101','20200708',freq='d')
	total_date = total_date.strftime('%Y%m%d')
	for date in total_date:
		try:
			print(date)
			print(data[date][:3])
		except:
			print('This day is wrong:',date)
			pass
	return()

def show_only_key_words():
	for i in data:
		for x,y in data[i][:3]:
			print(x)
	return()

if __name__ == '__main__':
	show_only_key_words()
	# show_key_words_with_score()