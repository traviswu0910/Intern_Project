from MetaClass import Clean
from MetaClass import Crawler
import tweepy
from Twitters_credentials import *
import Twitters_w2l
import time
import datetime
import json

# test_string = '''hi this is a simple test for the class,\
#  change the string to test different functions'''

# test = None
# def prep():
# 	return Clean(test_string)

# prep().Separate(gram=3).Close()
# prep().DeleteRedundant().Close()
# prep().DeletePunctuation().Close()
# prep().Capitalize().Close()
#text = 'I have a text'

class TestCleaner(Clean):
	def __init__(self, text):
		super().__init__(text)

	def Capitalize(self):
		self.Text = self.Text.upper()

		return (self)

	def Separate(self,gram=1):
		sent = self.Text.split()
		self.Text = []
		for a in range(len(sent)-gram+1):
			temp = ''
			for s in range(gram):
				temp = temp+sent[a+s]+' '
			self.Text.append(temp[:-1])


		return (self)

	def DeletePunctuation(self,
			Punctuation=[',','.','-','"',"'","'S","S'","{","}","[","]",":","@"]):
		for p in Punctuation:
			self.Text = self.Text.replace(p,'')

		return (self)

	def DeleteRedundant(self,
			Words=['A','THE','AN','TO','AND','OR','NOT'

			]):
		self.DeletePunctuation()
		sent = self.Text.split()
		meaningful = []
		for s in sent:
			meaningful.append(s)
			for w in Words:
				if s.upper()==w.upper():
					meaningful = meaningful[:-1]

		self.Text = ''
		for w in meaningful:
			self.Text = self.Text+w+' '
		self.Text = self.Text[:-1]

		return (self)

	def Substitute(self, Oldletter, Newletter):
		self.Text = self.Text.replace(Oldletter,Newletter)
		return self

	def Close(self):
		print(self.Text)

		return self


class TestCrawler(Crawler):
	def __init__(self, name, source):
		super().__init__(name, source)

	def CrawlerRawData(self):
		"""
		Utility function to setup the Twitter's API
		with our access keys provided.
		"""
		
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
		start_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		self.CrawlerTime['Start'] = start_time

		for tweetersname in top100_list:
			try:
				tweets = extractor.user_timeline(screen_name=tweetersname, count=200)
				#self.RawData.append(tweetersname)
				#print('Number of tweets extracted: {}.\n'.format(len(tweets)))
				print(tweetersname)
				# print the mist recent 5 tweets:
				#print('5 recent tweets:\n')
				for tweet in tweets[:200]:
					#print(tweet.text)
					#json_dict[tweetersname] = {i: tweet}
					self.RawData.append(tweetersname)
					self.RawData.append(tweet.text) #推文
					self.RawData.append(tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')) #推文時間
					self.RawData.append(tweet.favorite_count) #按讚次數
					self.RawData.append(tweet.retweet_count) #轉推次數
					self.RawData.append(tweet.source) #推文工具
					#print(self.RawData)
			except:
				pass
		end_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		self.CrawlerTime['End'] = end_time
		print(self.CrawlerTime)
		#self.RawData = json.dumps(json_dict)
		#print(self.RawData)

		return (self.RawData)

	def __RecordCrawlerTime(self):
		print(self.CrawlerTime)
		return(self.CrawlerTime)

	def ParseRawData(self):

		return (self)

	def Close(self):
		return self



# text = "SEC Cyber Unit Task Force should pay special attention to Citron Research interview on CNBC Fast Money regarding\u2026 https://t.co/EaLzKtefzT"
# TestCleaner(text).DeleteRedundant().Close()
# print(text)

#爬top100人200則資料
rawdatas = TestCrawler('Twitter_Trump','https://twitter.com/').CrawlerRawData()

#寫入rawdata_try.txt (寫入top100裡的前200則)
f = open('./All_Data/RawData/0706.txt','w')
f.write(str(rawdatas))
f.close()








	