import csv
import os

def get_did_pubkey(index):
    with open('TEST.csv','r') as myFile:  
        lines=csv.reader(myFile)
        i = 0
        for line in lines:            
            if(i == index):
                return  line[0],line[1]
            i += 1
    return None,None

did,key = get_did_pubkey(1)
print("did:{} key:{}".format(did,key))

did,key = get_did_pubkey(4)
print("did:{} key:{}".format(did,key))

with open('pubkey','w') as f:
    f.write(key)

mac = "00:" + did[0:2] + ":" + did[2:4] + ":" +did[4:6] + ":" +did[6:8]
print("mac:{}".format(mac))

cmd = "sed -i " + "'/mac=/c/mac=" + mac + "' test.txt"
print("cmd:{}".format(cmd))
os.system(cmd)

cmd = "sed -i " + "'/did:/c/did: " + did + "' test.txt"
print("cmd:{}".format(cmd))
os.system(cmd)

