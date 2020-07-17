# import json

# filename = 'Info_ID.json'

# t = {
# 	'WillyWu': {
# 		'Password': '0000',
# 		'ID': 'jcoiej0284',
# 	},
# }

# with open(filename, 'w+') as f:
# 	json.dump(t, f)



### fix tabs
filenames = ['login_willy.css', 'main.css']
newfiles = 'dr.py'

t = None

for filename in filenames:
	with open(filename, 'r') as f:
		t = f.read().replace('\t\t', '\t')

	with open(filename, 'w') as f:
		f.write(t)





