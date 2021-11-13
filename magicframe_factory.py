import time
import os
import serial

error_count = 0

test_file = "/vendor/udisk_sda1/mode-test.txt"
test_uart = "/dev/ttyS1"
log_file = "magicframe_factory.log"

def log(msg):
    print(msg)
    if(os.path.getsize(log_file) > 1024 * 100):
        with open(log_file,"w") as f:
            f.write(msg)
            f.write("\n")
            f.flush()
    else:
        with open(log_file,"a") as f:
            f.write(msg)
            f.write("\n")
            f.flush()

time.sleep(10)

log("----------------------------------------------------------------")

os.system("/config/wifi/wpa_cli -i wlan0 -p /tmp/wifi/run/wpa_supplicant status > wifi_status")
os.system('/config/wifi/iwlist wlan0 scanning essid "Magicframe-2.4G-0001" > wifi_scan')

''' 
bssid=02:10:18:01:00:02
ssid=Magicframe-2.4G-0001
id=0
mode=station
pairwise_cipher=CCMP
group_cipher=CCMP
key_mgmt=WPA2-PSK
wpa_state=COMPLETED
ip_address=192.168.2.18
p2p_device_address=24:14:07:01:bb:ab
address=24:14:07:01:bb:ab
'''
with open("wifi_status") as f:
    buf = f.read()
    buf = buf.splitlines()
    dict_dat = {}
    for line in buf:
        d = line.split("=")
        dict_dat[d[0]] = d[1]
    print(dict_dat)
    if(dict_dat.get("wpa_state",None) != "COMPLETED"):
        log("Test WIFI connect failure")
        error_count += 1
        # 连接wifi失败，启动AP模式

''' 
wlan0     Scan completed :
          Cell 01 - Address: 02:10:18:01:00:02
                    Channel:7
                    Frequency:2.442 GHz (Channel 7)
                    Quality=70/70  Signal level=-24 dBm
                    Encryption key:on
                    ESSID:"Magicframe-2.4G-0001"
                    Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 18 Mb/s
                              24 Mb/s; 36 Mb/s; 54 Mb/s
                    Bit Rates:6 Mb/s; 9 Mb/s; 12 Mb/s; 48 Mb/s
                    Mode:Master
                    Extra:tsf=7fffffffffffffff
                    Extra: Last beacon: 930ms ago
                    (Unknown Wireless Token 0x8C05)
'''
with open("wifi_scan") as f:
    buf = f.read()
    index = buf.find('Magicframe-2.4G-0001')
    print(index)
    if index == -1:
        log("Test WIFI Signal level failure")
        error_count += 1
    index = buf.find("Signal level=",index-200,index)

    buf = buf[index:]
    buf = buf.splitlines()
    buf = buf[0].split("=")
    buf = buf[1].split()
    signal_level = int(buf[0])
    log("Signal level="+str(signal_level))

if not os.path.isfile(test_file):
    log("Test file does not exist in udisk")    
    exit(-1)

try:
    ser = serial.Serial(test_uart, 9600,timeout=0.5)
    send_buf = b"hello world"
    ser.write(send_buf)
    recv_buf = ser.read(len(send_buf))
    print(recv_buf)
    if(len(recv_buf) < len(send_buf)):
        log("Test UART failure")
    else:
        for i in range(len(send_buf)):
            if(send_buf[i] != recv_buf[i]):
                log("Test UART failure")
                error_count += 1
                break
    ser.close()
except Exception as e:
    print(e)
    log("Test UART failure")
    error_count += 1

if(error_count == 0):
    os.system()
else:
    os.system()

