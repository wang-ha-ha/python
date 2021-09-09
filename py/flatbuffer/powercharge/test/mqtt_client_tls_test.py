import time
import struct
import paho.mqtt.client as mqtt
import dns.resolver

def dns_query(domain, type):
    print(type + "记录：")
    try:
        dnsquery = dns.resolver.query(domain, type)
        for i in dnsquery.response.answer:
            for j in i:
                print(j)
                return j
    except dns.resolver.NoAnswer:
        print(domain+' DNS未响应！')
    print('-' * 20)

domain = "zns.commnet.com.cn"
HOST = dns_query(domain, 'A')
HOST = str(HOST)


cafile = "./cacert.pem"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("topic_qos0")
    client.subscribe("S2N/863434041549020")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
def on_publish(client, userdata, mid):
    #print("publish:%s"%(mid))
    pass

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass
    
client = mqtt.Client(client_id = "test_username1111")
client.username_pw_set("27c70a22-ab54-44f1-8de8-6e31ef9188a7","123456")
client.tls_set(cafile,None,None)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_log = on_log
client.connect(HOST, 8883, 60) # 600为keepalive的时间间隔
client.loop_start()

while(True):    
    if 0:
        dat = input()
        if(dat == "id"):
            for i in sendmsg:
                print("{0:x}".format(i),end = " ")
            print()
            client.publish(publish, payload=sendmsg, qos=0)
        elif(dat == 'ping'): 
            client.publish(publish, payload="ping", qos=0)
        elif(dat == 'PING'): 
            client.publish(publish, payload="PING", qos=0)
    else:
        i = 1
        while True:
            dat = "abcdefg"
            topic = 'echo/' + str(i)
            i += 1
            client.publish("topic_qos1", payload=dat, qos=0)
            time.sleep(110)

