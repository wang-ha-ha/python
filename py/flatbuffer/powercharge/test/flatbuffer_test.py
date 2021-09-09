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
    client.subscribe("flatbuffer")

def on_message(client, userdata, msg):
    if(msg.topic == "online" or msg.topic == "flatbuffer"):
        en_payload = locakerbox.Msg.Payload.Payload.GetRootAsPayload(msg.payload,0)
        print("flatbuffer payload type:%s "%(en_payload.PayloadType()))
        if(en_payload.PayloadType() == 1):
            en_msg = en_payload.Payload()
            data = locakerbox.Msg.Door.Door()
            data.Init(en_msg.Bytes,en_msg.Pos)
                                             
            print("Doors:%s --- len:%s"%(data.Doors(0),data.DoorsLength()))
            print("Session:%s"%(data.Session()))
            print("Reply:%s"%(data.Reply()))
            print("Result:%s"%(data.Result()))
            print("Success:%s"%(data.Success(0)))
            print("Failure:%s"%(data.Failure(0)))

        elif(en_payload.PayloadType() == 2):
            en_msg = en_payload.Payload()
            data = locakerbox.Msg.PingEv.PingEv()
            data.Init(en_msg.Bytes,en_msg.Pos)

            print("Temp:%s"%(data.Temp()))
            print("Signal:%s"%(data.Signal()))
            print("Pos:%s.%s"%(data.Pos().Lat(),data.Pos().Log()))

        elif(en_payload.PayloadType() == 3):
            en_msg = en_payload.Payload()
            data = locakerbox.Msg.OnlineEv.OnlineEv()
            data.Init(en_msg.Bytes,en_msg.Pos)

            print("Softver:%s"%(data.Softver()))
            print("Hardver:%s"%(data.Hardver()))
            print("Iccid:%s"%(data.Iccid()))

        elif(en_payload.PayloadType() == 4):
            en_msg = en_payload.Payload()
            data = locakerbox.Msg.UpgradeEv.UpgradeEv()
            data.Init(en_msg.Bytes,en_msg.Pos)
            
            print("Softver:%s"%(data.Softver()))
            print("Url:%s"%(data.Url()))
    else:
        print(msg.topic+" " + ":" + str(msg.payload))


def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass

def build_payload(B,payload_type,offset):
    locakerbox.Msg.Payload.PayloadStart(B)
    locakerbox.Msg.Payload.PayloadAddPayloadType(B,payload_type)
    locakerbox.Msg.Payload.PayloadAddPayload(B,offset)
    payload_offset = locakerbox.Msg.Payload.PayloadEnd(B)

    B.Finish(payload_offset)

    return B.Output()

def flatbuffer_test():
    builder = flatbuffers.Builder(1024)
    ver1 = builder.CreateString('1.0.0')
    url1 = builder.CreateString('http://127.0.0.1:8080/')

    locakerbox.Msg.UpgradeEv.UpgradeEvStart(builder)
    locakerbox.Msg.UpgradeEv.UpgradeEvAddSoftver(builder,ver1)
    locakerbox.Msg.UpgradeEv.UpgradeEvAddUrl(builder,url1)
    upgradev_offset = locakerbox.Msg.UpgradeEv.UpgradeEvEnd(builder)
    
    buf = build_payload(builder,locakerbox.Msg.Payloads.Payloads.UpgradeEv,upgradev_offset)
    print("buf len:%s"%(len(buf)))
    print(buf)

    enpayload = locakerbox.Msg.Payload.Payload.GetRootAsPayload(buf,0)
    print(enpayload.PayloadType())
    print(enpayload.Payload().Bytes)

    msg = enpayload.Payload()
    enupgrade = locakerbox.Msg.UpgradeEv.UpgradeEv()
    enupgrade.Init(msg.Bytes,msg.Pos)

    print(enupgrade.Url())
    print(enupgrade.Softver())

def send_doorev():
    builder = flatbuffers.Builder(1024)

    session = builder.CreateString('1010')
    doors = bytes([1])
    doors_ = builder.CreateByteVector(doors)
    locakerbox.Msg.Door.DoorStart(builder)
    locakerbox.Msg.Door.DoorAddDoors(builder,doors_)
    locakerbox.Msg.Door.DoorAddSession(builder,session)
    locakerbox.Msg.Door.DoorAddResult(builder,locakerbox.Msg.Result.Result.Failure)

    doors_offset = locakerbox.Msg.Door.DoorEnd(builder)

    buf = build_payload(builder,locakerbox.Msg.Payloads.Payloads.Door,doors_offset)
    client.publish('flatbuffer', payload=buf, qos=0)

def send_pingev():

    builder = flatbuffers.Builder(1024)
    signal = builder.CreateString('signal')

    locakerbox.Msg.PingEv.PingEvStart(builder)
    locakerbox.Msg.PingEv.PingEvAddTemp(builder,17)
    locakerbox.Msg.PingEv.PingEvAddSignal(builder,signal)
    locakerbox.Msg.PingEv.PingEvAddPos(builder,locakerbox.Msg.GPS.CreateGPS(builder,1.1,3.3))
    pingev_offset = locakerbox.Msg.PingEv.PingEvEnd(builder)

    buf = build_payload(builder,locakerbox.Msg.Payloads.Payloads.PingEv,pingev_offset)
    client.publish('flatbuffer', payload=buf, qos=0)

def send_upgrade():
    builder = flatbuffers.Builder(1024)

    ver1 = builder.CreateString('1.0.0')
    url1 = builder.CreateString('http://127.0.0.1:8080/')

    locakerbox.Msg.UpgradeEv.UpgradeEvStart(builder)
    locakerbox.Msg.UpgradeEv.UpgradeEvAddSoftver(builder,ver1)
    locakerbox.Msg.UpgradeEv.UpgradeEvAddUrl(builder,url1)
    upgradev_offset = locakerbox.Msg.UpgradeEv.UpgradeEvEnd(builder)

    buf = build_payload(builder,locakerbox.Msg.Payloads.Payloads.UpgradeEv,upgradev_offset)
    client.publish('flatbuffer', payload=buf, qos=0)

if (__name__ == "__main__"):
    '''
    client_id = "MQTT flatbuffer server"
    '''
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()

    while(True):
        dat = input()
        if (dat == 'flat1'):
            send_doorev()
        elif (dat == 'flat2'):
            send_pingev()
        elif (dat == 'flat3'):
            pass
        elif (dat == 'flat4'):
            send_upgrade()          
        elif (dat == "test"):
            flatbuffer_test()




