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

	def getInputs(self):
		return {
				'msg': self.msg,
				'username': self.username,
				'password': self.password,
				'retype': self.retype,
				'show_retype': self.show_retype,
			}

	def fillInfo(self, username, password, retype, show_retype=0, msg=''):
		self.username = username
		self.password = password
		self.retype = retype
		self.show_retype = show_retype
		self.msg = msg

	def returnDefault(self):
		self.currentForm = self.defaultForm

	def checkRetype(self):
		if self.retype=='' or self.password=='':
			self.msg = Sign.EMPTY_INPUT
		elif not self.retype==self.password:
			self.msg = Sign.WRONG_RETYPE
		else:
			self.msg = Sign.SUCCESS
		return self.msg

	def checkName(self, signin=False):
		print('hihihi')
		if self.username=='':
			self.msg = Sign.EMPTY_INPUT
		elif self.username.upper() in [u.upper() for u in self.userlist.info.keys()]:
			print('hi there')
			if signin:
				self.msg = Sign.SUCCESS
			else:
				self.msg = Sign.USERNAME_TAKEN
		else:
			self.msg = Sign.SUCCESS
		return self.msg

	def checkSignup(self, flag):
		if self.checkName()==Sign.SUCCESS:
			if flag==1:
				self.checkRetype()
			else:
				self.msg = Sign.SUCCESS
		return self.msg


	def signup(self, flag):
		self.show_retype = 1
		if self.checkSignup(flag)==Sign.SUCCESS:
			if flag==1:
				self.tag = tag()
				self.userlist.create(self.username, self.password, self.tag)
				self.updateTime()
				self.userfeed.create(self.tag, self.currentForm['time'])
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
			self.userfeed.update_login(self.tag, self.currentForm['time'])
		return self.msg

	def activity(self):
		self.userfeed.update_activity(self.tag, self.currentForm)

	def addActivity(self, form):
		self.currentForm = form
		self.activity()










