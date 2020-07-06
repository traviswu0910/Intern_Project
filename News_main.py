# <<<<<<< HEAD
from Module_Clean import *
from News_Crawler import *
import pandas as pd
import glob
from datetime import datetime

today=datetime.now().strftime('%Y-%m-%d')

def get_RSS_data():
    rss_list = pd.read_excel('RSS_list.xlsx')
    for name, url in zip(rss_list.name, rss_list.url):
        website = RSS(name, url)
        website.CrawlerRawData()
        website.ParseRawData()
        parsed_data = website.Close()
        raw_data = website.RawData

        # save raw data into txt
        with open(f'./All_Data/News_Rawdata/{today}_{name}.txt', 'w', encoding='utf-8')as f:
            f.write(raw_data)
        # save dictionary to json file
        with open(f'./All_Data/News_ParsedData/{today}_{name}.json', 'w')as f:
            json.dump(parsed_data, f)


def get_API_data():
    api_list = pd.read_excel('API_list.xlsx')
    for name, url in zip(api_list.name, api_list.url):
        website = API(name, url)
        website.CrawlerRawData()
        website.ParseRawData()
        parsed_data = website.Close()
        raw_data = website.RawData

        # save raw data into txt
        with open(f'./All_Data/News_Rawdata/{today}_{name}.txt', 'w', encoding='utf-8')as f:
            f.write(raw_data)
        # save dictionary to json file
        with open(f'./All_Data/News_ParsedData/{today}_{name}.json', 'w')as f:
            json.dump(parsed_data, f)

#def import_json():
#    files = glob.glob('parsed_data/*.json')
#    for file in files:
#        with open(file) as json_file:
#            data = json.load(json_file)
#            print(data)
            
if __name__ == '__main__':
    get_RSS_data()
    get_API_data()
#    import_json()
# =======
# from Clean import Clean
# from Crawler import RSS, API
# import pandas as pd
# import glob
# from datetime import datetime
# import json

# today=datetime.now().strftime('%Y-%m-%d')

# def get_RSS_data():
#     rss_list = pd.read_excel('RSS_list.xlsx')
#     for name, url in zip(rss_list.name, rss_list.url):
#         website = RSS(name, url)
#         website.CrawlerRawData()
#         website.ParseRawData()
#         parsed_data = website.Close()
#         raw_data = website.RawData

#         # save raw data into txt
#         with open(f'./raw_data/{today}_{name}.txt', 'w', encoding='utf-8')as f:
#             f.write(raw_data)
#         # save dictionary to json file
#         with open(f'./parsed_data/{today}_{name}.json', 'w')as f:
#             json.dump(parsed_data, f)


# def get_API_data():
#     api_list = pd.read_excel('API_list.xlsx')
#     for name, url in zip(api_list.name, api_list.url):
#         website = API(name, url)
#         website.CrawlerRawData()
#         website.ParseRawData()
#         parsed_data = website.Close()
#         raw_data = website.RawData

#         # save raw data into txt
#         with open(f'./raw_data/{today}_{name}.txt', 'w', encoding='utf-8')as f:
#             f.write(raw_data)
#         # save dictionary to json file
#         with open(f'./parsed_data/{today}_{name}.json', 'w')as f:
#             json.dump(parsed_data, f)

            
# if __name__ == '__main__':
#     get_RSS_data()
#     get_API_data()
    
    

# >>>>>>> 97ebe13b7a524f82655659569af60351937bb467
