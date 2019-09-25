
import os
import json

current_path = os.path.abspath('.')
#print(current_path)

current_path = os.path.normpath("c:/asd/asd")
#print(current_path)

current_path = os.path.dirname(__file__)
#print(current_path)


def relative_path_to_abs(path):
	global current_path
	return current_path + '\\' + path

s = open(relative_path_to_abs('dat.json'),encoding='utf-8')

res = json.load(s)

print(type(res))
print(res.keys())

err = res["error_code"]

print("type:%s content:%s"%(type(err),err))

stu_info = res["stu_info"]

print("type:%s len:%s content:%s"%(type(stu_info),len(stu_info),stu_info))

stu1 = stu_info[0]
print("stu1 info:%s"%(stu1))

stu2 = stu_info[1]
print("stu1 info:%s"%(stu2))


stu1_file = open(relative_path_to_abs('stu1_info.txt'),'w')
json.dump(stu1,stu1_file)

stu2_file = open(relative_path_to_abs('stu2_info.txt'),'w')
json.dump(stu2,stu2_file,indent=4,ensure_ascii=False) #不用转码

s.close()
stu1_file.close()
stu2_file.close()
input("Press any key to exit!")