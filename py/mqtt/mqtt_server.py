import paho.mqtt.client as mqtt

cafile = "./ca.pem"
certfile = "./client.crt"
keyfile = "./client.key"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("chat")
    client.subscribe("lock_status")
    client.subscribe("read_lock")
    client.subscribe("lock")

def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass
    
client = mqtt.Client(client_id = "MQTT test server")
client.tls_set(cafile,None,None)
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.connect("192.168.2.107", 8883, 60)
client.loop_forever()