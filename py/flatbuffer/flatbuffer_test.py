#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' flatbuffer test '''

import flatbuffers

import locakerbox.Msg.Door
import locakerbox.Msg.GPS
import locakerbox.Msg.OnlineEv
import locakerbox.Msg.Payload
import locakerbox.Msg.Payloads
import locakerbox.Msg.PingEv
import locakerbox.Msg.Result
import locakerbox.Msg.UpgradeEv

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("chat")
    client.subscribe("lock_status")
    client.subscribe("read_lock")
    client.subscribe("lock")
    client.subscribe("online")

def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))
    if(msg.topic == "online"):
        en_payload = locakerbox.Msg.Payload.Payload.GetRootAsPayload(msg.payload,0)
        print("flatbuffer payload type:%s "%(en_payload.PayloadType()))
        if(en_payload.PayloadType() == 3):
            en_msg = en_payload.Payload()
            data = locakerbox.Msg.OnlineEv.OnlineEv()
            data.Init(en_msg.Bytes,en_msg.Pos)

            print("Softver:%s"%(data.Softver()))
            print("Hardver:%s"%(data.Hardver()))
            print("Iccid:%s"%(data.Iccid()))

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass
    
client = mqtt.Client(client_id = "MQTT flatbuffer server")
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.connect("116.231.80.201", 1883, 60)
client.loop_forever()


'''
builder = flatbuffers.Builder(1024)

ver1 = builder.CreateString('1.0.0')
url1 = builder.CreateString('http://127.0.0.1:8080/')

locakerbox.Msg.UpgradeEv.UpgradeEvStart(builder)
locakerbox.Msg.UpgradeEv.UpgradeEvAddSoftver(builder,ver1)
locakerbox.Msg.UpgradeEv.UpgradeEvAddUrl(builder,url1)
upgradev = locakerbox.Msg.UpgradeEv.UpgradeEvEnd(builder)

locakerbox.Msg.Payload.PayloadStart(builder)
locakerbox.Msg.Payload.PayloadAddPayloadType(builder,locakerbox.Msg.Payloads.Payloads.UpgradeEv)
locakerbox.Msg.Payload.PayloadAddPayload(builder,upgradev)
payload = locakerbox.Msg.Payload.PayloadEnd(builder)

builder.Finish(payload)

buf = builder.Output()

print(buf)

enpayload = locakerbox.Msg.Payload.Payload.GetRootAsPayload(buf,0)
print(enpayload.PayloadType())
print(enpayload.Payload().Bytes)

msg = enpayload.Payload()
enupgrade = locakerbox.Msg.UpgradeEv.UpgradeEv()
enupgrade.Init(msg.Bytes,msg.Pos)

print(enupgrade.Url())
print(enupgrade.Softver())
'''



