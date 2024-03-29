import paho.mqtt.client as mqtt

cafile = "./cacert.pem"
certfile = "./client.crt"
keyfile = "./client.key"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("lock_status")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
def on_publish(client, userdata, mid):
    #print("publish:%s"%(mid))
    pass

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass
    
client = mqtt.Client(client_id = "MQTT test client")
client.tls_set(cafile)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_log = on_log
client.connect('120.48.26.72', 8883, 60) # 600为keepalive的时间间隔
client.loop_start()

while(True):
    dat = input()
    if(dat == "r"):
        client.publish('read_lock', payload=dat, qos=0)
    else:
        client.publish('lock', payload=dat, qos=0)