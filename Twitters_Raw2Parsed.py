#將rawdata轉成parsed_data
import ast
import json
dic = {}
data=[]
with open('./All_Data/Twitters_Rawdata/2020-07-07.txt') as fp: #填入要parse的rawdata名稱
	for line in fp:
		obj = ast.literal_eval(line)
		for x in range (len(obj)):
			if (x%6==0):
				dic={}
				dic['Name'] = obj[x]
			elif (x%6==1):
				dic['Text'] = obj[x]
			elif (x%6==2):
				dic['Time'] = obj[x]
			elif (x%6==3):
				dic['Fav'] = obj[x]
			elif (x%6==4):
				dic['Retw'] = obj[x]
			else:
				dic['Source'] = obj[x]
				data.append(dic)
		json_result = json.dumps(data) #轉換成json格式
#print(json_result)

f = open('./All_Data/Twitters_ParsedData/p0707.txt','w')
f.write(json_result)
f.close()


