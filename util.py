# tag.py
import random
import json
import datetime as dt
from download import strategy_list

SchemaLocation='All_Data/'
Path={
    'schema':SchemaLocation,
    'feed':'{}Reference/Info.json'.format(SchemaLocation),
    'id':'{}Reference/Info_ID.json'.format(SchemaLocation),
}

class Sign():
	SUCCESS				= ''
	USERNAME_TAKEN		= 'This username is already taken :('
	ABSENT_USERNAME		= 'Username does not exist >o<'
	WRONG_PASSWORD		= 'You have the wrong password :('
	WRONG_RETYPE		= 'Your passwords don\'t match :('
	EMPTY_INPUT			= 'You left your input boxes empty ><'
	PICK_UTIL			= 'Please pick a destination before you enjoy the ride :)'

def tag(num):
	tag = ''
	for i in range(num):
		n = random.randint(0, 61)
		if n<10:
			tag+=str(n)
		elif n<36:
			tag+=chr(n+55)
		else:
			tag+=chr(n+61)
	return tag


def json_safeLoading(filename):
	try:
		with open(filename, 'r') as f:
			return json.load(f)
	except:
		with open(filename, 'w+') as f:
			json.dump({}, f)
		return {}

def json_safeDumping(content, filename):
	with open(filename, 'w+') as f:
		json.dump(content, f, indent=4)


class InfoJson():
	def __init__(self, filename):
		self.info = json_safeLoading(filename)
		self.filename = filename

	def pull(self):
		self.info = json_safeLoading(filename)

	def push(self):
		json_safeDumping(self.info, self.filename)



class UserList(InfoJson):
	def __init__(self, filename):
		super().__init__(filename)

	def create(self, username, password, tag):
		self.info[username] = {
			'password': password,
			'id': tag,
		}
		self.push()

	def delete(self):
		pass

	def changePassword(self):
		pass



class UserFeed(InfoJson):
	def __init__(self, filename):
		super().__init__(filename)

	def create(self, tag, time):
		self.info[tag] = {
			'login':[],
			'click':[],
			'note':[],
			'log':[],
			'portfolio': strategy_list
		}
		self.updateLogin(tag, time)

	def notes(self, tag):
		return self.info[tag]['note']

	def clicks(self, tag):
		return self.info[tag]['click']

	def logs(self, tag):
		return self.info[tag]['log']

	def addHistory(self, tag, log):
		self.logs(tag).append(log)

	def updateLogin(self, tag, time):
		self.addHistory(tag, {'action': 'login', 'content': {'time': time}})
		self.info[tag]['login'].append(time)
		self.push()

	def updateClick(self, tag, clickContent):
		self.addHistory(tag, {'action': 'click', 'content': clickContent})
		for i, click in enumerate(self.clicks(tag)):
			if click['title']==clickContent['title'] and click['url']==clickContent['url']:
				self.clicks(tag).pop(i)
		self.clicks(tag).append(clickContent)
		self.push()

	def updateNote(self, tag, noteContent):
		self.addHistory(tag, {'action': 'note', 'content': noteContent})
		for i, note in enumerate(self.notes(tag)):
			if note['title']==noteContent['title'] and note['url']==noteContent['url']:
				self.notes(tag).pop(i)
		self.notes(tag).append(noteContent)
		self.push()



class UserInfo():
	utilities = [{
        'image': '/static/img/togo/{}.png'.format(a),
        'name': a,
        'id': a,
        'input': '{}_input'.format(a),
        'html': '{}.html'.format(a),
    } for a in ['NewsAssistant', 'Stock',]]
	currentForm = {
	    'date':'2020-05-05',
        'pf':'pph_2',
        'kw':'',
        "click":{},
        'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
        'note': '',
	}
	userlist = UserList(Path['id'])
	userfeed = UserFeed(Path['feed'])
	flag = {'signup':False, 'login':False}

	def __init__(self):
		self.defaultForm = self.currentForm

	def loggedIn(self):
		return self.flag['login']

	def signingUp(self):
		return self.flag['signup']

	def notes(self):
		return self.userfeed.notes(self.tag)

	def clicks(self):
		return self.userfeed.clicks(self.tag)

	def logs(self):
		return self.userfeed.logs(self.tag)

	def copy(self, target):
		dest = []
		for t in target:
			dest.append(t)
		return dest

	def copyClicks(self):
		return self.copy(self.clicks())

	def copyNotes(self):
		return self.copy(self.notes())

	def copyLogs(self):
		return self.copy(self.logs())

	def updateTime(self):
		self.currentForm['time'] = dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')

	def addHistory(self, content):
		self.userfeed.addHistory(self.tag, content)

	def blankInputs(self):
		return {
			'msg': '',
			'username': '',
			'password': '',
			'retype': '',
			'show_retype': '',
			'utilities': self.utilities,
		}

	def getInputs(self):
		return {
			'msg': self.msg,
			'username': self.username,
			'password': self.password,
			'retype': self.retype,
			'show_retype': self.show_retype,
			'utilities': self.utilities,
		}

	def fillInfo(self, username, password, retype, show_retype=0, msg=''):
		self.username = username
		self.password = password
		self.retype = retype
		self.show_retype = show_retype
		self.msg = msg

	def updateForm(self, req=None):
		if not req:
			self.returnDefault()
			return
		self.currentForm = {
			'date': req.values['datepicker'],
			'pf': req.values['portfolio'],
			'kw': req.form['ikeyword'],
			'time': dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
		}

	def returnDefault(self):
		self.currentForm = self.defaultForm
		return self.currentForm

	def checkRetype(self):
		if self.retype=='' or self.password=='':
			self.msg = Sign.EMPTY_INPUT
		elif not self.retype==self.password:
			self.msg = Sign.WRONG_RETYPE
		else:
			self.msg = Sign.SUCCESS
		return self.msg

	def checkName(self, signin=False):
		if self.username=='':
			self.msg = Sign.EMPTY_INPUT
		elif self.username.upper() in [u.upper() for u in self.userlist.info.keys()]:
			if signin:
				self.msg = Sign.SUCCESS
			else:
				self.msg = Sign.USERNAME_TAKEN
		else:
			self.msg = Sign.SUCCESS
		return self.msg

	def checkSignup(self):
		if self.checkName()==Sign.SUCCESS:
			if self.signingUp():
				self.checkRetype()
			else:
				self.msg = Sign.SUCCESS
		return self.msg


	def signup(self):
		self.show_retype = 1
		if self.checkSignup()==Sign.SUCCESS:
			if self.signingUp():
				self.tag = tag(40)
				self.userlist.create(self.username, self.password, self.tag)
				self.updateTime()
				self.userfeed.create(self.tag, self.currentForm['time'])
				self.flag['login'] = True
			self.flag['signup'] = True
		return self.msg

	def checkSignin(self):
		if self.username=='' or self.password=='':
			self.msg = Sign.EMPTY_INPUT
		elif self.checkName(signin=True)==Sign.SUCCESS:
			if not self.password==self.userlist.info[self.username]['password']:
				self.msg = Sign.WRONG_PASSWORD
		else:
			self.msg = Sign.ABSENT_USERNAME
		return self.msg

	def signin(self):
		self.show_retype = 0
		if self.checkSignin()==Sign.SUCCESS:
			self.updateTime()
			self.tag = self.userlist.info[self.username]['id']
			self.userfeed.updateLogin(self.tag, self.currentForm['time'])
			self.flag['login'] = True
		return self.msg

	def addNote(self, currForm, req):
		self.currentForm = {
				"date": currForm['date'],
	            "pf": currForm['pf'],
	            "kw": currForm['kw'],
	            "url": req['url'],
	            "title" : req['title'],
	            "tab": req['tab'],
	            'time': dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
	            'note': req['note'],
	        }
		self.userfeed.updateNote(self.tag, self.currentForm)

	def addClick(self, currForm, req):
		self.currentForm = {
				"date": currForm['date'],
	            "pf": currForm['pf'],
	            "kw": currForm['kw'],
	            "url": req['url'],
	            "title" : req['title'],
	            "tab": req['tab'],
	            'note': '',
	            'time': dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
	        }
		self.userfeed.updateClick(self.tag, self.currentForm)

	def changeNote(self, news, noteContent):
		for i, note in enumerate(self.notes()):
			if note['title']==news['title'] and note['url']==news['url']:
				self.notes()[i]['note'] = noteContent
		self.userfeed.push()

	def deleteNote(self, news):
		self.addHistory({'action': 'delete note', 'content': news})
		for i, note in enumerate(self.notes()):
			if note['title']==news['title'] and note['url']==news['url']:
				self.notes().pop(i)
				break
		self.userfeed.push()

	def deleteStory(self, news, move=False):
		if not move:
			self.addHistory({'action': 'delete click', 'content': news})
		for i, click in enumerate(self.clicks()):
			if click['title']==news['title'] and click['url']==news['url']:
				self.clicks().pop(i)
		self.userfeed.push()








