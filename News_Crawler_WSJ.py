# ws.py

from bs4 import BeautifulSoup as bs
import json
from datetime import date
import requests
from fake_useragent import UserAgent

def getUrl(text):#整理資料，只留下title跟link
	link = ''
	title = ''
	text = str(text)
	filt = text.split('"')
	#today = str(date.today()).replace('-', '')
	for a in filt:
		if len(a)>=5:
			if a[:5]=='https':
				link = a
			if a[0]=='>':
				title = a[1:-5]
	return title, link

# def cleanHtml(a):
# 	str_1 = str(a)
# 	split_1 = str_1.split('"')
# 	Html = split_1[3]
# 	split_2 = split_1[4].split('>')
# 	split_3 = split_2[1].split('<')
# 	Title = split_3[0]
# 	# print(Html,Title)

# 	return(Html,Title)


ua = UserAgent()
headers = {
	'User-Agent':ua.random
}
print(headers)#檢查哪個user agent可以哪個不行
today = str(date.today())
today_for_crawl = str(date.today()).replace('-', '')
target = '20200714' #要抓的日期
date_for_pubdate = '2020-07-14'
url='https://www.wsj.com/news/archive/'+target
print(target)

page = requests.get(url,headers = headers)
print(page)
# print(page.text)
soup = bs(page.content, 'html.parser')


found = soup.findAll('a', {'class':''})
# print(found)
found = [a for a in soup.findAll('a', {'class':''}) if 'articles' in str(a).split('/')]
print(len(found))


# print(found)

news_list = []
for i, a in enumerate(found):
	# if i%2==1:
	b = getUrl(a)
	if (not '<img' in b) and b[0][0:5]!='About':
		news_list.append(b)
		# print(news_list)
		# print('~~~~~~~~~~~~~~~~~~')
# print(len(news_list[1]))
data = []
for news in news_list:
	dic = {}
	dic['title'] = news[0]
	dic['link'] = news[1]
	dic['pubdate'] = date_for_pubdate
	dic['source'] = 'Wall Street Journal'
	data.append(dic)


with open(f'./All_Data/News_ParsedData/2020-07-14_WSJ.json','w') as f:
	json.dump(data,f)










