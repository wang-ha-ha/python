#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import serial
import time
import threading
import sys
import getopt
import os

version = 20190716
ser = serial.Serial("com5", 115200)

# def main():
#     while True:
#         recv = get_recv()
#         if recv != None:
#             print(recv)
#             ser.write(recv[0] + "\n")
#         time.sleep(0.1)

# def get_recv():
#     cout = ser.inWaiting()
#     if cout != 0:
#         line = ser.read(cout)
#         recv = str.split(line)
#         ser.reset_input_buffer()
#         return recv

def crc16(x, invert):
    a = 0xFFFF
    b = 0x8408
    for byte in x:
        # a ^= ord(byte)
        a ^= byte
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    return a
    # s = hex(a).upper()

    # return s[4:6]+s[2:4] if invert == True else s[2:4]+s[
    # 
    # 4:6]

SOF =       0xC0
EOF =       0xC1
TRANSFER =  0x7D
XOR =       0x20

_id = 1

def update_id(recv_id):
    global _id 
    _id = recv_id + 1
    # if _id > 0:
    if _id > 254:
        _id = 1

def bulid_frame_basis(id, type, strcmd, data=[]):
    buf = [id, type, ord(strcmd[0]), ord(strcmd[1])]
    
    if len(data) > 0:
        buf.extend(data)
    # strcrc = crc16(buf, True)
    crc = crc16(buf, True)
    # buf.append(int(strcrc[0:2], 16))
    # buf.append(int(strcrc[2:4], 16))
    buf.append(crc & 0xFF)
    buf.append((crc >> 8) & 0xFF)

    frame = [SOF]
    for byte in buf:
        if (byte == SOF or byte == EOF or byte == TRANSFER):
            frame.append(TRANSFER)
            frame.append(byte ^ XOR)
        else:
            frame.append(byte)
    frame.append(EOF)

    return frame

_flg_start = False
_flg_transfer = False
_frame = []

def protocol_receive(buf=[]):
    global  _flg_start
    global _flg_transfer
    global _frame

    res = False

    for byte in buf:
        if (_flg_start == False):
            if (byte == SOF):
                _flg_start = True
                del _frame[:]
                _frame.append(byte)
        else:
            if (_flg_transfer == False):
                if (byte == SOF):
                    del _frame[:]

                if (byte == TRANSFER):
                    _flg_transfer = True
                    continue

                _frame.append(byte)

                if (byte == EOF):
                    res = frame_listener(_frame)
                    del _frame[:]
                    _flg_start = False
                    _flg_transfer = False
            else:
                _flg_transfer = False
                _frame.append(byte ^ XOR)

    return res

def weight_to_dict(dat=[]):
    num = int(len(dat) / 5)
    print(num)
    if (num == 0):
        return
    format_str = "<" + "bi" * num
    byte_dat = bytes(dat)
    id_weight = struct.unpack(format_str,byte_dat)
    num = int(len(id_weight))
    print(id_weight)
    dict_id_weight = {}
    for i in range(0,num,2):
        dict_id_weight[id_weight[i]] = id_weight[i + 1]

    return dict_id_weight

def frame_listener(frame=[]):
    if (len(frame) < 8):
        return False

    # _id = frame[1]
    update_id(frame[1])
    type = frame[2]
    # cmd = (frame[3] << 8) + frame[4]
    cmd = chr(frame[3]) + chr(frame[4])

    # crc_recv = (frame[-3] << 8) + frame[-2]
    # crc_calc = int((crc16(frame[1:-3], True)), 16)
    crc_recv = (frame[-2] << 8) + frame[-3]
    # print(crc_recv)
    # crc_calc = crc16(frame[1:-3], True)

    data_len = len(frame) - 8
    dat = frame[5:5+data_len]
    print("recv:{}".format(frame))
    print("dat:{}".format(dat))
    #  if (crc_recv != crc_calc):
    #      print("protocol rs error: crc recv %x(%x)\n" % (crc_recv, crc_calc))
    #      return False

    if (type == 0xF1):
        print("protocol rs invalid type: data multi\n");
        return False

    if ((cmd == "FS" or cmd == "FB" or cmd == "FE")):
        pass
    elif (cmd == "OD"):   
        ack = dat[0]
        print("OD ack:{}".format(ack))
        dat = dat[1:]
        dict_dat = weight_to_dict(dat)
        print("OD:{}".format(dict_dat))
    elif (cmd == "QV"):
        ver_str_list=map(chr,dat)
        ver = ''.join(ver_str_list)
        print("Ver:{}".format(ver))
    elif (cmd == "GG"):        
        dict_dat = weight_to_dict(dat)
        print("---GG---")
        for k,v in dict_dat.items():
            print("{}: {}".format(k,v))
    elif (cmd == "EC"):
        dict_dat = weight_to_dict(dat)
        print("EC:{}".format(dict_dat))
    return True

def serial_recv():
    cout = ser.inWaiting()
    if cout != 0:
        recv = ser.read(cout)
        # print(type(recv))
        # recv = str.split(line)
        ser.reset_input_buffer()
        return recv

def serial_send(buf=[]):
    print("send{",end = ' ')
    for byte in buf:
        print("%02X" % byte,end = ' ')
    print("}")
        # ser.write(chr(byte))
        # ser.write(byte)
    ser.write(bytes(buf))

def protocol_loop():
    while True:
        try:
            strrecv = serial_recv()
            if strrecv != None:
                recv = []
                
                print("recv:{",end = ' ')
                for byte in strrecv:
                    # recv.append(ord(byte))
                    # print(ord(byte))
                    print("%02X" % byte,end = ' ')
                    recv.append(byte)
                print("}")
                if protocol_receive(recv):
                    pass
                    # return
                del recv[:]
        except Exception as identifier:
            print(identifier)
        
    print("protocol_loop exit")

def main(argv):
    if 1:
        box_type = 0x01
        while True:
            dat = input()
            if dat == 'OD':
                data_buf = struct.pack("i",100)
                serial_send(bulid_frame_basis(_id, box_type, "OD",data_buf))
            elif dat == 'QV':
                serial_send(bulid_frame_basis(_id, box_type, "QV"))
            elif dat == 'GG':
                serial_send(bulid_frame_basis(_id, box_type, "GG"))
            elif dat == 'SD':
                __dat = input()
                box_type = int(__dat)
                print(box_type)
                data_buf = struct.pack("B",box_type)
                serial_send(bulid_frame_basis(_id, 0, "SD",data_buf))
            elif dat == 'RD':
                serial_send(bulid_frame_basis(_id, 0, "RD"))
            elif dat == 'SN':
                __dat = input()
                num = int(__dat)
                print(num)
                data_buf = struct.pack("i",num)
                serial_send(bulid_frame_basis(_id, box_type, "SN",data_buf))
            elif len(dat) == 2:
                serial_send(bulid_frame_basis(_id, box_type, dat))
    else:
        while True:
            serial_send(bulid_frame_basis(_id, 0x01, "GG"))
            # protocol_loop()
            # time.sleep(0.1)
            # serial_send(bulid_frame_basis(_id, 0x02, "GG"))
            # protocol_loop()
            time.sleep(0.1)
        
if __name__ == "__main__":
    #  python protocol_rs_file_modem.py -f rtthread.bin    
    print("version: %d" % (version))
    
    t1 = threading.Thread(target=protocol_loop)
    t1.start()
    main(sys.argv[1:])
    # t1.join()
