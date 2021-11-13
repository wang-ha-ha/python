import paho.mqtt.client as mqtt
import time

cafile = "./ca.pem"
certfile = "./client.crt"
keyfile = "./client.key"

server_ip = '120.48.26.72'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("echo/#")
    client.subscribe("online")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
def on_publish(client, userdata, mid):
    #print("publish:%s"%(mid))
    pass

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass

client = mqtt.Client(client_id = "MQTT test client")
#client.tls_set(cafile,certfile,keyfile)
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_log = on_log

client.connect(server_ip, 1883, 60) # 600为keepalive的时间间隔

client.loop_start()

while(True):
    if 1:
        dat = input("Enter 0 or 1 to select the message type:")
        if(dat == "1"):
            dat = input("message:")
            client.publish('topic_qos1', payload=dat, qos=0)
        elif(dat == "0"):
            dat = input("message:")
            client.publish('topic_qos0/123', payload=dat, qos=0)
    else:
        while True:
            dat = "abcdefg"
            client.publish('test', payload=dat, qos=0)
            time.sleep(30)