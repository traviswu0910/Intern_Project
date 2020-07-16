from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt
from util import *

from GetUIData import News,Twitter,Chart

global userfeed
global userList

userfeed = json_safeLoading(Path['feed'])
userList = json_safeLoading(Path['id'])

class UserInfo:
    currentForm = {
        'date':'2020-05-05',
        'pf':'pph_2',
        'kw':'',
        "click":{},
        'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
    }
    # BrowseClick=0
    # BrowseHistory={}
    def __init__(self, name, password):
        self.username = name
        self.password = password
        self.defaultInput = self.currentForm

        
    def rewind(self):
        self.currentForm = self.defaultInput

    def signUp(self):
        userList[self.username] = {
                'Password': self.password,
                'ID': tag()
            }
        json_safeDumping(userList, Path['id'])

class InfoJson:
    def _feedDump():
        json_safeDumping(userfeed, Path['feed'])

    def Create(user, tag):
        userfeed[tag] = {'login':[user.currentForm], 'activity':[]}
        json_safeDumping(userfeed, Path['feed'])
        
    def Read(self):
        pass
    def Update(self):
        tag = userList[user.username]
        userfeed[tag]['activity'].append(user.currentForm)
        self._feedDump()

    def Delete(self):
        pass
        
LoginFlag=0
SignupFlag=0


app = Flask(__name__)

InfoFile=InfoJson()

@app.route("/")
def login():
    return render_template('Home.html')

@app.route('/Main')
def main():
    inputs = {
            'msg': '',
            'refill': 0,
            'username': '',
            'password': '',
            'retype': 0,
        }
    return render_template('Main.html', inputs=inputs)

@app.route("/NewsAssistant", methods=["POST", "GET"])
def newsAssistant():
    def userLoad():
        userList = json_safeLoading(Path['id'])

    def userUpdate():
        user.signUp()

    def userPlugin():
        userUpdate()
        InfoJson.Create(user=user, tag=userList[user.username]['ID'])

    def validateID(name, password):
        if userList==None:
            userLoad()
        users = [ u.upper() for u in userList.keys() ]
        if not (name.upper() in users):
            return({'SuccessFlag':0,'Description':'The user does not exist'})
        elif userList[name]['Password']==password:
            return({'SuccessFlag':1,'Description':'Pass'})
        else :
            return({'SuccessFlag':-1,'Description':'Password is wrong!!'})

    def signup():
        if 'signup' in request.values.keys():
            return True

    if request.method == "POST":
        global LoginFlag
        global SignupFlag

        print('LoginFlag: {}'.format(LoginFlag))
        print('SignupFlag: {}'.format(SignupFlag))

        if not LoginFlag:
            global user
            user=UserInfo(request.values['usr'], request.values['pwd'])
            validation=validateID(user.username, user.password)
            if not SignupFlag:
                if not signup(): # sign-in button
                    if not validation['SuccessFlag']:
                        inputs = {
                                'msg': validation['Description'],
                                'refill': 0,
                                'username': user.username,
                                'password': user.password,
                                'retype': 0,
                            }
                        return render_template('Main.html', inputs=inputs)
                    LoginFlag=1
                else: # sign-up button
                ### currently working here
                    if validation['SuccessFlag']==0:
                        SignupFlag = 1
                        print(user.username)
                        inputs = {
                                'msg': '',
                                'refill': 1,
                                'username': user.username,
                                'password': user.password,
                                'retype': 1,
                            }
                        return render_template('Main.html', inputs=inputs)
                    else:
                        validation['Description'] = 'Username is already in use!'
                        inputs = {
                                'msg' : validation['Description'],
                                'refill': 1,
                                'username': user.username,
                                'password': user.password,
                                'retype': 0,
                            }
                        return render_template('Main.html', inputs=inputs)
            else: ### signing up (retyping password)
                if validation['SuccessFlag']!=0:
                    validation['Description']='Username already in use!'
                    inputs = {
                            'msg': validation['Description'],
                            'refill': 1,
                            'username': user.username,
                            'password': user.password,
                            'retype': 1,
                        }
                    return render_template('Main.html', inputs=inputs)
                elif request.values['retype']!=user.password:
                    validation['Description']='The passwords don\'t match'
                    inputs = {
                            'msg': validation['Description'],
                            'refill': 1,
                            'username': user.username,
                            'password': user.password,
                            'retype': 1,
                        }
                    return render_template('Main.html', inputs=inputs)
                userPlugin()
                
        else:
            try:
                user.currentForm={
                    'date':request.values['datepicker'],
                    'pf':request.values['portfolio'],
                    'kw':request.form['ikeyword'],
                    "click":{},
                    'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')
                }
            except:
                user.rewind()
            
        selected = {'pph_1':'','pph_2':'','pph_3':'','pph_4':'','pph_5':''}
        selected[user.currentForm['pf']]='selected'
        
        # keyword=User.CurrentForm['kw']
        top_news = News.get_top_news(user.currentForm['date'], range(1, 4), user.currentForm['kw'])
        
        # portfolio=User.CurrentForm['pf']
        portfolio_list,portfolio_news = News.get_portfolio_news(user.currentForm['date'],user.currentForm['pf'],user.currentForm['kw'])
        if portfolio_list:
            ret = Chart.get_chart_data(user.currentForm['date'],user.currentForm['pf'])
        else:
            ret=''
        
        top_tws = Twitter.get_top_twitter(user.currentForm['date'], range(1, 5))

        celebs, hot_tws = Twitter.get_hot_twitter(user.currentForm['date'])
        
        return render_template("NewsAssistant.html",
            date = user.currentForm['date'],
            selected = selected,
            portfolio = portfolio_list,
            portfolio_news = portfolio_news,
            keyword = user.currentForm['kw'],
            top_news = top_news,
            ret=ret,
            top_tws=top_tws,
            hot_tws=hot_tws,
            celebs=celebs,
        )
    

@app.route("/log/create-entry", methods=["POST"])
def create_entry():
    req = request.get_json()
    
    user.currentForm={
        "date":user.currentForm['date'],
        "pf":user.currentForm['pf'],
        "kw":user.currentForm['kw'],
        "click":{"url": req['url'], "title" : req['title'], "tab": req['tab']},
        'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
        'note': req['note'],
    }
    
    InfoFile.Update()

    res = make_response(jsonify({"message": "OK"}), 200)

    return res

if __name__ == "__main__":
    app.run()

