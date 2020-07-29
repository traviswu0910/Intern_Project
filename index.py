from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt
from util import *
from getInputs import *

user = UserInfo()        
LOGIN_FLAG, SIGNUP_FLAG = 0, 0

app = Flask(__name__)

@app.route('/draw')
def drawingBoard():
    return render_template('DrawingBoard.html')

@app.route("/")
def login():
    return redirect(url_for('main'))

@app.route('/Main', methods=['POST', 'GET'])
def main():
    def signup():
        if 'signup' in request.values.keys():
            return True
    global user, LOGIN_FLAG, SIGNUP_FLAG, LOGIN_SUCCESS
    if request.method=='GET':
        return render_template('Main.html', inputs=user.blankInputs())
    elif request.method=='POST':
        user.fillInfo(username=request.values['usr'], password=request.values['pwd'], retype=request.values['retype'])
        if signup():
            if user.signup(SIGNUP_FLAG)==Sign.SUCCESS:
                if SIGNUP_FLAG:
                    LOGIN_FLAG = 1
                SIGNUP_FLAG = 1
        elif user.signin()==Sign.SUCCESS:
            LOGIN_FLAG = 1
        if LOGIN_FLAG:
            for u in user.utilities:
                if request.values[u['input']]=='1':
                    return redirect(url_for(u['name']))
                    # return render_template(u['html'], inputs=utilInputs(util=u['name'], form=user.returnDefault()))
            user.msg = Sign.PICK_UTIL
        return render_template('Main.html', inputs=user.getInputs())



@app.route("/NewsAssistant", methods=["POST", "GET"])
def NewsAssistant():
    if request.method == "POST":
        user.updateForm(req=request)
        return render_template("NewsAssistant.html", inputs=utilInputs(user.currentForm, util='NewsAssistant'))
    elif request.method=="GET":
        return render_template("NewsAssistant.html", inputs=utilInputs(user.currentForm, util='NewsAssistant'))
    
@app.route("/NewsAssistant/History", methods=['POST', 'GET'])
def History():
    if request.method=='GET':
        return render_template('NewsAssistant_History.html', history=userHistory(user))

@app.route("/log/news-assistant-click", methods=["POST"])
def newsAssistant_click():    
    user.addClick(currForm=user.currentForm, req=request.get_json())
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

@app.route("/log/news-assistant-note", methods=["POST"])
def newsAssistant_note():    
    user.addNote(currForm=user.currentForm, req=request.get_json())
    res = make_response(jsonify({"message": "OK"}), 200)
    return res

if __name__ == "__main__":
    app.run()


