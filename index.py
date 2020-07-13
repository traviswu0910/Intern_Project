from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt

from GetUIData import News,Twitter,Chart

def check(msg):
    with open('./check.txt', 'w+') as f:
        f.write('{}\n'.format(msg))

class UserInfo:
    defaultInput = {
        'date':'2020-05-05',
        'pf':'pph_2',
        'kw':'',
        "clc":{},
        'click_time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
    }

    CurrentForm = {
        'date':'2020-05-05',
        'pf':'pph_2',
        'kw':'',
        "clc":{},
        'click_time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
    }
    # BrowseClick=0
    # BrowseHistory={}
    def __init__(self,ID,Password):
        self.ID=ID
        self.Password=Password

        
    def rewind(self):
        self.CurrentForm = self.defaultInput
    
    
class InfoJSON:
    Path='./All_Data/Reference/'
    File='Info.json'
    def Create(self,ID,Content):
        with open('{}{}'.format(self.Path,self.File), 'r') as json_file:
                data = json.load(json_file)
        
        if data:
            data=data[0]
            count=max([int(entry) for entry in data[ID].keys()])+1
        else:
            data={}
            data[ID]={}
            count=0
            
        data[ID][count] = Content
        
        with open('{}{}'.format(self.Path,self.File), 'w') as json_file:
            json.dump([data], json_file, indent=4, ensure_ascii=False)
        
    def Read(self):
        pass
    def Update(self):
        pass
    def Delete(self):
        pass
        
LoginFlag=0


app = Flask(__name__)

InfoFile=InfoJSON()
@app.route("/")
def main():
    return render_template('login.html')

@app.route("/main.html", methods=["POST", "GET"])
def login():
    def ValidateID(User,Password):
        with open('./All_Data/Reference/Info_ID.json', 'r') as json_file:
            IDList = json.load(json_file)

        if not (User in IDList.keys()):
            return({'SuccessFlag':0,'Description':'The user does not exist'})
        elif IDList[User]['Password']==Password:
            return({'SuccessFlag':1,'Description':'Pass'})
        else :
            return({'SuccessFlag':0,'Description':'Password is wrong!!'})
    if request.method == "POST":
        global LoginFlag
        if not LoginFlag:
            global User
            User=UserInfo(request.values['usr'],request.values['pwd'])
            
            Validation=ValidateID(User.ID,User.Password)
            if not Validation['SuccessFlag']:
                return render_template('login.html')
            
            LoginFlag=1
        else:
            try:
                User.CurrentForm={
                    'date':request.values['datepicker'],
                    'pf':request.values['portfolio'],
                    'kw':request.form['ikeyword'],
                    "clc":{},
                    'click_time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
                }
            except:
                User.rewind()
            
            InfoFile.Create(User.ID,User.CurrentForm)

        selected = {'pph_1':'','pph_2':'','pph_3':'','pph_4':'','pph_5':''}
        selected[User.CurrentForm['pf']]='selected'
        
        # keyword=User.CurrentForm['kw']
        top_news = News.get_top_news(User.CurrentForm['date'], range(1, 4), User.CurrentForm['kw'])
        
        # portfolio=User.CurrentForm['pf']
        portfolio_list,portfolio_news = News.get_portfolio_news(User.CurrentForm['date'],User.CurrentForm['pf'],User.CurrentForm['kw'])
        if portfolio_list:
            ret = Chart.get_chart_data(User.CurrentForm['date'],User.CurrentForm['pf'])
        else:
            ret=''
        
        top_tws = Twitter.get_top_twitter(User.CurrentForm['date'], range(1, 5))

        celebs, hot_tws = Twitter.get_hot_twitter(User.CurrentForm['date'])
        
        return render_template("main.html",
            date = User.CurrentForm['date'],
            selected = selected,
            portfolio = portfolio_list,
            portfolio_news = portfolio_news,
            keyword = User.CurrentForm['kw'],
            top_news = top_news,
            ret=ret,
            top_tws=top_tws,
            hot_tws=hot_tws,
            celebs=celebs,
        )
    

@app.route("/log/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    
    User.CurrentForm={
        "date":User.CurrentForm['date'],
        "pf":User.CurrentForm['pf'],
        "kw":User.CurrentForm['kw'],
        "clc":{"url": req['url'], "title" : req['title'], "tab": req['tab']},
        'click_time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
        'note': req['note'],
    }
    
    InfoFile.Create(User.ID,User.CurrentForm)

    res = make_response(jsonify({"message": "OK"}), 200)

    return res

if __name__ == "__main__":
    app.run()

