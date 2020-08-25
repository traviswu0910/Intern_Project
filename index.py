# index.py
from flask import Flask, redirect, url_for, render_template, request,jsonify,make_response
import json
import pandas as pd
import datetime as dt
from util import *
from getInputs import *

user = UserInfo()		

app = Flask(__name__)

developing = False

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
	global user, LOGIN_FLAG, SIGNUP_FLAG
	if request.method=='GET':
		return render_template('Main.html', inputs=user.blankInputs())
	elif request.method=='POST':
		user.fillInfo(username=request.values['usr'], password=request.values['pwd'], retype=request.values['retype'])
		if signup():
			user.signup()
		else:
			user.signin()
		if user.loggedIn():
			for u in user.utilities:
				if request.values[u['input']]=='1':
					return redirect(url_for(u['name']))
					# return render_template(u['html'], inputs=utilInputs(util=u['name'], form=user.returnDefault()))
			user.msg = Sign.PICK_UTIL
		return render_template('Main.html', inputs=user.getInputs())

@app.route("/NewsAssistant", methods=["POST", "GET"])
def NewsAssistant():
	if request.method == "POST":
		if not user.loggedIn():
			return redirect(url_for('main'))
		user.updateForm(req=request)
		return render_template("NewsAssistant.html", inputs=utilInputs(user.currentForm, util='NewsAssistant', user_portfolios=user.pflists))
	elif request.method=="GET":
		if not user.loggedIn():
			if developing:
				user.fillInfo(username='BazingaWonka', password='buzz', retype='')
				user.signin()
			else:
				return redirect(url_for('main'))
		return render_template("NewsAssistant.html", inputs=utilInputs(user.currentForm, util='NewsAssistant', user_portfolios=user.pflists))
	
@app.route('/NewsAssistant/HistoryLog', methods=['POST', 'GET'])
def HistoryLog():
	if request.method=='GET':
		if not user.loggedIn():
			return redirect(url_for('main'))
		return render_template('HistoryLog.html', logfile=userLog(user))

@app.route("/NewsAssistant/History", methods=['POST', 'GET'])
def History():
	if request.method=='GET':
		if not user.loggedIn():
			return redirect(url_for('main'))
		return render_template('NewsAssistant_History.html', history=userHistory(user))

@app.route("/log/news-assistant-change-note", methods=["POST"])
def newsAssistant_changeNote():
	req = request.get_json()
	user.changeNote(news=req['news'], noteContent=req['note'])
	res = make_response(jsonify({"message": "OK"}), 200)
	return res

@app.route("/log/news-assistant-delete-note", methods=["POST"])
def newsAssistant_deleteNote():
	req = request.get_json()
	user.deleteNote(news=req['news'])
	res = make_response(jsonify({"message": "OK"}), 200)
	return res

@app.route("/log/news-assistant-delete-story", methods=["POST"])
def newsAssistant_deleteStory():
	req = request.get_json()
	user.deleteStory(news=req['news'], move=(int(req['move'])==1))
	res = make_response(jsonify({"message": "OK"}), 200)
	return res

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

@app.route("/log/news-assistant-download", methods=['Post'])
def newsAssistant_Download():
	res = make_response(jsonify({"message": "OK"}), 200)
	utilInputs(user.currentForm, util='download')
	return res

@app.route("/portfolio-upload", methods=['post'])
def uploadPortfolio():
	res  = make_response(jsonify({"message": "New portfolio uploaded!"}), 200)
	for attr in dir(request):
		print('{}: {}'.format(attr, getattr(request, attr)))
	file = request.files['upload']
	data = json.load(file)
	# print(data)
	return res

if __name__ == "__main__":
	app.run()










