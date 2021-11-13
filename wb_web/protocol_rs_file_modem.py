#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time
import threading
import sys
import getopt
import os

version = 20190716
ser = serial.Serial("com3", 115200)

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

    # return s[4:6]+s[2:4] if invert == True else s[2:4]+s[4:6]

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
    print("recv:{}".format(frame))

    #  if (crc_recv != crc_calc):
    #      print("protocol rs error: crc recv %x(%x)\n" % (crc_recv, crc_calc))
    #      return False

    if (type == 0xF1):
        print("protocol rs invalid type: data multi\n");
        # return False

    if ((cmd == "FS" or cmd == "FB" or cmd == "FE")):
        pass
    else:
        print("cmd err: " + cmd)
        # return False

    return True

def serial_recv():
    time.sleep(0.1)
    cout = ser.inWaiting()
    if cout != 0:
        recv = ser.read(cout)
        # print(type(recv))
        # recv = str.split(line)
        ser.reset_input_buffer()
        return recv

def serial_send(buf=[]):
    print("send:{}".format(len(buf)))
    # for byte in buf:
        # ser.write(chr(byte))
        # ser.write(byte)
    ser.write(bytes(buf))

def protocol_loop():
    while True:
        strrecv = serial_recv()
        if strrecv != None:
            recv = []
            for byte in strrecv:
                # recv.append(ord(byte))
                # print(ord(byte))
                recv.append(byte)            
            if protocol_receive(recv):
                # pass
                return
            del recv[:]
    print("protocol_loop exit")

def main(argv):
    filepath = ''
    try:
        opts, args = getopt.getopt(argv, "f:", ["file="])
    except getopt.GetoptError as s:
        print("XXX.py [-f file]")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            filepath = arg

    try:
        chunk_size = 1024

        with open(filepath, 'rb') as f:
            totalsize = os.path.getsize(filepath)
            #print("totalsize:")
            #print(totalsize)
            size = 0  

            serial_send(bulid_frame_basis(_id, 0x01, "FS"))
            protocol_loop()
            
            while True:
                chunk_data = f.read(chunk_size)
                # print(type(chunk_data))
                # print(chunk_data)
                if not chunk_data:
                    break
                content = []
                for byte in chunk_data:
                    # print(type(byte))
                    content.append(byte)
                # print(content)
                serial_send(bulid_frame_basis(_id, 0x01, "FB", content))
                protocol_loop()

                size+=len(chunk_data)
                print("progress: %d/%d(%d)" % (size, totalsize, (size*100)/totalsize))

        serial_send(bulid_frame_basis(_id, 0x01, "FE"))
        protocol_loop()

    except KeyboardInterrupt:
        if ser != None:
            ser.close()

if __name__ == "__main__":
    #  python protocol_rs_file_modem.py -f rtthread.bin    
    print("version: %d" % (version))
    begin_time = time.time()
    main(sys.argv[1:])
    end_time = time.time()
    run_time = end_time-begin_time
    print ('该循环程序运行时间：',run_time) 

