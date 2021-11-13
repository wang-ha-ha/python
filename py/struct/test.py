
import asyncio
import time
import numpy as np

# print(np.eye(4))

# import struct

# t = time.strptime("2020-06-23 15:19:55","%Y-%m-%d %H:%M:%S")
# print(t)
# ts = time.mktime(t)
# print(ts)
# print(type(ts))

# localtime = time.localtime(int(ts))
# print("本地时间为 :{}",format(localtime))

# bin_buf_s = struct.pack("f", ts)
# print(type(bin_buf_s))
# for i in bin_buf_s:
#     print("{0:x}".format(i),end = " ")
# print()

# ts, = struct.unpack("f",bin_buf_s)
# print(ts)
# print(type(ts))

# localtime = time.localtime(ts)
# print("本地时间为 :{}",format(localtime))

# bin_buf_s = bytes([0x5e, 0xf1,0xab,0x1b])
# for i in bin_buf_s:
#     print("{0:x}".format(i),end = " ")
# print()

# ts, = struct.unpack(">i",bin_buf_s)
# print(ts)
# print(type(ts))

# localtime = time.localtime(ts)
# print("本地时间为 :{}", format(localtime))

# bin_buf_s = struct.pack("<i", ts)
# for i in bin_buf_s:
#     print("{0:x}".format(i),end = " ")
# print()

reqtime = int(time.time())
print("reqtime:{} type{}".format(reqtime,type(reqtime)))
localtime = time.asctime( time.localtime(reqtime) )
print(localtime)
reqtime = time.time()
print("reqtime:{} type{}".format(reqtime,type(reqtime)))
localtime = time.asctime( time.localtime(reqtime) )
print(localtime)