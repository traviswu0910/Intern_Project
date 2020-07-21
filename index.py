from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt
from util import *

from GetUIData import News,Twitter,Chart

user = UserInfo()        
LOGIN_FLAG=0
SIGNUP_FLAG=0

utilities = ['na', 'stock']
utilities = [{
            'image': '/static/img/togo/{}.png'.format(a),
            'name': '{}'.format(a),
            'id': a,
        } for a in utilities]

app = Flask(__name__)

@app.route('/draw')
def drawingBoard():
    return render_template('DrawingBoard.html')

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
            'retype': '',
            'show_retype': 0,
        }
    return render_template('Main.html', inputs=inputs, utilities=utilities)

@app.route("/NewsAssistant", methods=["POST", "GET"])
def newsAssistant():
    def signup():
        if 'signup' in request.values.keys():
            return True
    global user, LOGIN_FLAG, SIGNUP_FLAG
    if request.method == "POST":
        if not LOGIN_FLAG:
            usr = request.values['usr']
            pwd = request.values['pwd']
            retype = request.values['retype']
            user.fillInfo(usr, pwd, retype)
            if not SIGNUP_FLAG:
                if signup(): # sign-up button
                    msg = user.signup(SIGNUP_FLAG)
                    show_retype=0
                    if msg==Sign.SUCCESS: ### username available
                        SIGNUP_FLAG = 1
                        show_retype = 1
                        
                    inputs = {
                            'msg': msg,
                            'refill': 1,
                            'username': user.username,
                            'password': user.password,
                            'retype': retype,
                            'show_retype': show_retype,
                        }
                    return render_template('Main.html', inputs=inputs, utilities=utilities)
                else: # sign-in button
                    msg = user.signin()
                    if not msg==Sign.SUCCESS:
                        inputs = {
                                'msg': msg,
                                'refill': 1,
                                'username': user.username,
                                'password': user.password,
                                'retype': retype,
                                'show_retype': 0,
                            }
                        return render_template('Main.html', inputs=inputs, utilities=utilities)
                    LOGIN_FLAG=1
            else: ### signing up (retyping password)
                if signup():
                    msg = user.signup(SIGNUP_FLAG)
                    if not msg==Sign.SUCCESS:
                        inputs = {
                                'msg': msg,
                                'refill': 1,
                                'username': user.username,
                                'password': user.password,
                                'retype': retype,
                                'show_retype': 1,
                            }
                        return render_template('Main.html', inputs=inputs, utilities=utilities)
                else:
                    msg = user.signin()
                    SIGNUP_FLAG=0
                    if not msg==Sign.SUCCESS:
                        inputs = {
                                'msg': msg,
                                'refill': 1,
                                'username': user.username,
                                'password': user.password,
                                'retype': retype,
                                'show_retype': 0,
                            }
                        return render_template('Main.html', inputs=inputs, utilities=utilities)
        else:
            try:
                user.currentForm={
                    'date': request.values['datepicker'],
                    'pf': request.values['portfolio'],
                    'kw': request.form['ikeyword'],
                    "click": {},
                    'time': dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
                    'note': ''
                }
            except:
                user.defaultForm()
            
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
    
    user.addActivity(form={
            "date":user.currentForm['date'],
            "pf":user.currentForm['pf'],
            "kw":user.currentForm['kw'],
            "click":{"url": req['url'], "title" : req['title'], "tab": req['tab']},
            'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
            'note': req['note'],
        })

    res = make_response(jsonify({"message": "OK"}), 200)
    return res

if __name__ == "__main__":
    app.run()

