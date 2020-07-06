from MetaClass import Clean
from MetaClass import Crawler
import tweepy
from Twitters_credentials import *
import Twitters_w2l
import time
from datetime import datetime
import json

today=datetime.now().strftime('%Y-%m-%d')
RawData=[]


def get_Twitters_data():

	# Authentication and access using keys:
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	json_dict = {}

	# Return API with authentication:
	api = tweepy.API(auth)

	# create an extractor object:
	extractor = api

	#top100 twitters'name
	top100_list = Twitters_w2l.word2list('Twitters_top100.txt')

	# create a tweet list as follows:
	for tweetersname in top100_list:
		try:
			tweets = extractor.user_timeline(screen_name=tweetersname, count=200)
			print(tweetersname)#印出正在爬的作者
			for tweet in tweets[:200]:
				RawData.append(tweetersname)#作者姓名
				RawData.append(tweet.text) #推文
				RawData.append(tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')) #推文時間
				RawData.append(tweet.favorite_count) #按讚次數
				RawData.append(tweet.retweet_count) #轉推次數
				RawData.append(tweet.source) #推文工具
				#print(self.RawData)
		except:
			pass

		with open(f'./All_Data/Twitters_Rawdata/{today}.txt','w') as f:
			f.write(str(RawData))



if __name__ == '__main__':
	get_Twitters_data()
