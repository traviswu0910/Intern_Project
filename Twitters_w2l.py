#將txt轉成list


def word2list(filename):
	names = []
	with open(filename, 'r') as f:
		for l in f.readlines():
			names.append(l.strip())
	# print(names)
	return names
# word2list('top100.txt')

