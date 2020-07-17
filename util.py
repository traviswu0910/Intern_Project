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
	USERNAME_TAKEN		= 'This username is already taken :('
	ABSENT_USERNAME		= 'Username does not exist >o<'
	WRONG_PASSWORD		= 'You have the wrong password :('
	WRONG_RETYPE		= 'Your passwords don\'t match :('
	EMPTY_INPUT			= 'You left your input boxes empty ><'

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
        'note': '',
	}
	userlist = UserList(Path['id'])
	userfeed = UserFeed(Path['feed'])

	def __init__(self):
		self.defaultForm = self.currentForm

	def updateTime(self):
		self.currentForm['time'] = dt.datetime.now().strftime('%Y%m%d  %H:%M:%S')

	def fillInfo(self, username, password, retype):
		self.username = username
		self.password = password
		self.retype = retype
		self.exists = False
		if self.username.upper() in [a.upper() for a in self.userlist.info.keys()]:
			self.exists = True

	def defaultForm(self):
		self.currentForm = self.defaultForm
		return self.defaultForm

	def checkRetype(self):
		if self.retype=='' or self.password=='':
			return Sign.EMPTY_INPUT
		if not self.retype==self.password:
			return Sign.WRONG_RETYPE
		return Sign.SUCCESS

	def checkSignup(self, flag):
		if self.username=='':
			return Sign.EMPTY_INPUT
		elif self.exists:
			return Sign.USERNAME_TAKEN
		else:
			if flag==1:
				return self.checkRetype()
			return Sign.SUCCESS


	def signup(self, flag):
		check = self.checkSignup(flag)
		if flag==1 and check==Sign.SUCCESS:
			self.tag = tag()
			self.userlist.create(self.username, self.password, self.tag)
			self.updateTime()
			self.userfeed.create(self.tag, self.currentForm['time'])
			self.exists = True
		return check

	def checkSignin(self):
		if self.username=='' or self.password=='':
			return Sign.EMPTY_INPUT
		if self.exists:
			if not self.password==self.userlist.info[self.username]['password']:
				return Sign.WRONG_PASSWORD
			return Sign.SUCCESS
		else:
			return Sign.ABSENT_USERNAME

	def signin(self):
		check = self.checkSignin()
		if check==Sign.SUCCESS:
			self.updateTime()
			self.tag = self.userlist.info[self.username]['id']
			self.userfeed.update_login(self.tag, self.currentForm['time'])
		return check

	def activity(self):
		self.userfeed.update_activity(self.tag, self.currentForm)

	def addActivity(self, form):
		self.currentForm = form
		self.activity()










