import requests
import sys

file_name = "./机智云设备列表.txt"
did_list = []
with open(file_name,"r") as f:
    for lines in f.readlines():
        lines=lines.rstrip('\n')
        b=lines.split('\t')
        if len(b) > 2:
            did_list.append(b[1])
        #for i in b:
        #    print(i,end="\t")
        #print()

print(did_list)

for did in did_list:
    body = "did={}&passcode=passcode".format(did)
    header = {'Host': 'api.gizwits.com',"Content-Type":"application/x-www-form-urlencoded"}
    url = "http://api.gizwits.com/dev/devices"

    r = requests.delete(url,headers=header,data = body)

    print("----------------------------------")
    print(r.url)
    print("----------------------------------")
    print(r.status_code)
    print("----------------------------------")
    print(r.headers)
    print("----------------------------------")
    print(r.text)