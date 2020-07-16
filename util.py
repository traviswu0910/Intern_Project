# tag.py
import random
import json
import datetime as dt

SchemaLocation='All_Data/'
Path={
    'schema':SchemaLocation,
    'feed':'{}Reference/Info.json'.format(SchemaLocation),
    'id':'{}Reference/Info_ID.json'.format(SchemaLocation),
}

class Sign():
	SUCCESS				= ''
	ABSENT_USERNAME		= 'Username does not exist >o<'
	WRONG_PASSWORD		= 'You have the wrong password :('
	WRONG_RETYPE		= 'Your passwords don\'t match :('

def tag():
	tag = ''
	for i in range(40):
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
			return json.dump({}, f)
		return {}

def json_safeDumping(content, filename):
	with open(filename, 'w+') as f:
		json.dump(content, f, indent=4)


class InfoJson():
	def __init__(self, filename):
		self.info = json_safeLoading(filename)
		self.filename

	def pull(self):
		self.info = json_safeLoading(filename)

	def push(self):
		json_safeDumping(self.info, self.filename)

class UserList(InfoJson):
	def __init__(self, filename):
		super().__init__(fiilename)

	def create(self, username, password):
		self.info[username] = {
			'password': password,
			'id': tag(),
		}

	def delete(self):
		pass

	def changePassword(self):
		pass

class UserFeed(InfoJson):
	def __init__(self, filename):
		super().__init__(fiilename)

	def create(self, tag, time):
		self.info[tag] = {
			'login':[],
			'activity':[],
		}
		self.update_login(tag, time)

	def update_login(self, tag, time):
		self.info[tag]['login'].append(time)
		self.push()

	def update_activity(self, tag, action):
		self.info[tag]['activity'].append(action)
		self.push()

class UserInfo():
	currentForm = {
	    'date':'2020-05-05',
        'pf':'pph_2',
        'kw':'',
        "click":{},
        'time':dt.datetime.now().strftime('%Y%m%d  %H:%M:%S'),
	}
	self.userlist = InfoJson(Path['id'])
	self.userfeed = InfoJson(Path['feed'])

	def __init__(self, username, password):
		self.defaultForm = self.currentForm

	def updateTime(self):
		currentForm['time'] = dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')

	def fillInfo(self, username, password):
		self.username = username
		self.password = password
		self.tag = self.userlist.info[self.username]['id']

	def defaultForm(self):
		self.currentForm = self.defaultForm
		return self.defaultForm

	def checkInput(self, input_usr, input_pwd):
		users = self.userlist.keys()
		if input_usr in users:
			if not input_pwd==users[input_usr]:
				return Sign.WRONG_PASSWORD
			return Sign.SUCCESS
		else
			return Sign.ABSENT_USERNAME

	def signup(self, input_usr, input_pwd, input_re, flag):
		check = self.checkInput(input_usr, input_pwd)
		if flag==1:
			if input_pwd==input_re:
				if check==Sign.SUCCESS:
					self.userlist.create(input_usr, input_pwd)
					self.updateTime()
					self.userfeed.create(self.tag, self.currentForm['time'])
					return check
				return Sign.WRONG_RETYPE
		else:
			return check

	def signin(self, input_usr, input_pwd):
		check = self.checkInput(input_usr, input_pwd)
		if check==Sign.SUCCESS:
			self.updateTime()
			self.userfeed.update_login(self.tag, self.currentForm['time'])
		return check

	def activity(self, action):
		self.userfeed.update_activity(self.tag, action)












