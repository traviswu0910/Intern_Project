from MetaClass import Crawler
import datetime
import requests
from html.parser import HTMLParser
import time
import json

class RSS_Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cur_stag = []   # list
        self.content = []    # dic in list [{}, {}]

    def handle_starttag(self, tag, attrs):
        self.cur_stag.append(tag)
        if tag == 'item':
            self.content.append({})

    def handle_endtag(self, tag):
        self.cur_stag.pop()

    def handle_data(self, data):
        if len(self.cur_stag) >= 4 and \
                 'item' in self.cur_stag:
            self.content[-1].update({self.cur_stag[-1]:data})

class RSS(Crawler):
    def CrawlerRawData(self):
        self.RawData = requests.get(self.Source).text
        return (self)

    def __RecordCrawlerTime(self):
        return (datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M%S"))

    def ParseRawData(self):
        # self.ParsedData = feedparser.parse(self.RawData)
        self.CrawlerTime['Start'] = self.__RecordCrawlerTime()
        parser = RSS_Parser()
        parser.feed(self.RawData)
        self.ParsedData = parser.content
        self.CrawlerTime['End'] = self.__RecordCrawlerTime()

class API(Crawler):
    RawData = ''
    CrawlerTime = {'Start': 19000101000000, 'End': 21001231235959}
    ParsedData = [{}]

    def __init__(self, Name, Source):
        self.Name = Name
        self.Source = Source

    def CrawlerRawData(self):
        response = requests.get(self.Source)
# <<<<<<< HEAD
#         retry=0
# =======
        retry = 0
# >>>>>>> 97ebe13b7a524f82655659569af60351937bb467
        while response.status_code != 200 and retry < 3:
            try:
                response = requests.get(self.Source)
                time.sleep(1)
                retry = 10
            except Exception:
                retry = retry + 1
                time.sleep(1)
        self.RawData = response.text
        return (self)

    def __RecordCrawlerTime(self):
        return (datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S"))

    def ParseRawData(self):
        self.CrawlerTime['Start'] = self.__RecordCrawlerTime()

        jd = json.loads(self.RawData)
        self.ParsedData = jd.get('articles')

        self.CrawlerTime['End'] = self.__RecordCrawlerTime()

    def Close(self):
        return (self.ParsedData)






