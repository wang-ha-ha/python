#!/usr/bin/python3
# # -*- coding: utf-8 -*-

''' flatbuffer test '''

import flatbuffers

import magicframe.route.msg.Alerts
import magicframe.route.msg.Payload
import magicframe.route.msg.Payloads
import magicframe.route.msg.PingPong
import magicframe.route.msg.PowerCtl
import magicframe.route.msg.QueryStatus
import magicframe.route.msg.Result
import magicframe.route.msg.RouteInfo
import magicframe.route.msg.Status

import paho.mqtt.client as mqtt
import time
import random
import struct

route_id = "ABCD"
topic_python_to_ra = route_id + "-ra/magicframe/powerctl[-flat]"

#存储大小写字母和数字，特殊字符列表
_STR = [chr(i) for i in range(65,91)]   #65-91对应字符A-Z
_str = [chr(i) for i in range(97,123)]   #a-z
_number = [chr(i) for i in range(48,58)]  #0-9

total = _STR + _str + _number

def ranstr(num):
    salt = ''.join(random.sample(total, num))
    return salt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("magicframe/routeinfo")

def on_message(client, userdata, msg):
    print(msg.topic)
    client.unsubscribe(msg.topic)
    en_payload = magicframe.route.msg.Payload.Payload.GetRootAsPayload(msg.payload, 0)
    print("-----------------")
    print("flatbuffer payload type:%s " % (en_payload.TypeType()))
    if (en_payload.TypeType() == 1): #RouteInfo 
        en_msg = en_payload.Type()
        data = magicframe.route.msg.RouteInfo.RouteInfo()
        data.Init(en_msg.Bytes,en_msg.Pos)

        print("countx:{}".format(data.Countx()))
        print("county:{}".format(data.County()))
        print("routeid:{}".format(data.Routeid()))

        global route_id,topic_python_to_ra

        route_id = data.Routeid()
        topic_python_to_ra = route_id.decode() + "-ra/magicframe/powerctl[-flat]"
        print("topic:{}".format(topic_python_to_ra))
        
    elif (en_payload.TypeType() == 2):  #PingPong
        en_msg = en_payload.Type()
        data = magicframe.route.msg.PingPong.PingPong()
        data.Init(en_msg.Bytes, en_msg.Pos)
        
        print("Version:{}".format(data.Version()))
        print("Result:{}".format(data.Result()))
        print("Reason:{}".format(data.Reason()))

    elif (en_payload.TypeType() == 3):  #PowerCtl
        en_msg = en_payload.Type()
        data = magicframe.route.msg.PowerCtl.PowerCtl()
        data.Init(en_msg.Bytes, en_msg.Pos)

        print("Result:{}".format(data.Result()))
        print("Reason:{}".format(data.Reason()))
    elif (en_payload.TypeType() == 4):  #Status
        pass
    elif (en_payload.TypeType() == 5):  #QueryStatus
        pass
    elif (en_payload.TypeType() == 6): #Alerts
        pass

def on_log(client, userdata, level, buf):
    #print("log:%s-%s"%(level,buf))
    pass

def build_payload(B,payload_type,offset):
    magicframe.route.msg.Payload.PayloadStart(B)
    magicframe.route.msg.Payload.PayloadAddTypeType(B,payload_type)
    magicframe.route.msg.Payload.PayloadAddType(B,offset)
    payload_offset = magicframe.route.msg.Payload.PayloadEnd(B)

    B.Finish(payload_offset)

    return B.Output()

def send_pingev():
    builder = flatbuffers.Builder(1024)
    reply_str = ranstr(4) + '-' + ranstr(4) + '-' + ranstr(4)
    reply = builder.CreateString(reply_str)

    # reqtime = time.time()
    # print("reqtime:{} type{}".format(reqtime,type(reqtime)))
    # localtime = time.asctime( time.localtime(reqtime) )
    # print(localtime)
    reqtime = int(time.time())
    print("reqtime:{} type{}".format(reqtime,type(reqtime)))
    localtime = time.asctime( time.localtime(reqtime) )
    print(localtime)
    magicframe.route.msg.PingPong.PingPongStart(builder)
    magicframe.route.msg.PingPong.PingPongAddReqtime(builder,reqtime)
    magicframe.route.msg.PingPong.PingPongAddReply(builder,reply)
    pingev_offset = magicframe.route.msg.PingPong.PingPongEnd(builder)

    global route_id,topic_python_to_ra
    buf = build_payload(builder, magicframe.route.msg.Payloads.Payloads.PingPong, pingev_offset)
    
    print("topic:{}".format(topic_python_to_ra))
    print("topic:{}".format(topic_python_to_ra + reply_str))
    client.subscribe(topic_python_to_ra + "/" +reply_str)
    client.publish(topic_python_to_ra, payload=buf, qos=0)

    en_payload = magicframe.route.msg.Payload.Payload.GetRootAsPayload(buf, 0)
    en_msg = en_payload.Type()
    data = magicframe.route.msg.PingPong.PingPong()
    data.Init(en_msg.Bytes,en_msg.Pos)

    print("Reqtime:{0:x}".format(data.Reqtime()))

def send_power_ctl():
    builder = flatbuffers.Builder(1024)
    reply_str = ranstr(4) + '-' + ranstr(4) + '-' + ranstr(4)
    reply = builder.CreateString(reply_str)

    magicframe.route.msg.PowerCtl.PowerCtlStart(builder)
    power_ctl_mode = int(input("please enter(0-1):"))
    magicframe.route.msg.PowerCtl.AddMode(builder,power_ctl_mode)
    magicframe.route.msg.PowerCtl.PowerCtlAddReply(builder,reply)
    pingev_offset = magicframe.route.msg.PowerCtl.PowerCtlEnd(builder)

    global route_id,topic_python_to_ra
    buf = build_payload(builder, magicframe.route.msg.Payloads.Payloads.PowerCtl, pingev_offset)
    
    print("topic:{}".format(topic_python_to_ra))
    print("topic:{}".format(topic_python_to_ra + reply_str))
    client.subscribe(topic_python_to_ra + "/" +reply_str)
    client.publish(topic_python_to_ra, payload=buf, qos=0)

    en_payload = magicframe.route.msg.Payload.Payload.GetRootAsPayload(buf, 0)
    en_msg = en_payload.Type()
    data = magicframe.route.msg.PingPong.PingPong()
    data.Init(en_msg.Bytes,en_msg.Pos)

    print("Reqtime:{0:x}".format(data.Reqtime()))

if (__name__ == "__main__"):
    '''
    client_id = "MQTT flatbuffer server"
    '''
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = on_log
    client.connect("192.168.2.1", 1883, 60)
    # client.connect("120.48.26.72", 1883, 60)
    client.loop_start()
    
    dat = input("输入回车开始发送消息")
    while (True):
        if 1:
            dat = input()
            if (dat == 'ping'):
                send_pingev()
            elif (dat == 'power_ctl'):
                send_power_ctl()
        elif 1:
            send_pingev()
            print("-----------------\r\n")
            time.sleep(5)
        else:
            dat = input()
            client.publish(topic_python_to_ra, payload=dat, qos=0)
            






