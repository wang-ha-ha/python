from socket import *
import ssl

http_service_addr = ('127.0.0.1', 8000)
tcp_service_addr = ('120.48.26.72', 6666)
certificate_file = './certificate.pem'

def main(addr,flag):

    BUFSIZE = 8192
    
    s = socket(AF_INET, SOCK_STREAM)

    if flag == True:
        tcpClientSocket = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED,ca_certs = certificate_file)
    else:
        tcpClientSocket = s

    tcpClientSocket.connect(addr)
    while True:
        data = input('>')
        if not data:
            continue
        if data == "q":
            break
            
        # 发送数据
        tcpClientSocket.send(data.encode('utf-8'))
        # 接收数据
        #data, ADDR = tcpClientSocket.recvfrom(BUFSIZE)
        data  = tcpClientSocket.recv(BUFSIZE)
        if not data:
            break
        print("服务器端响应：", data.decode('utf-8'))

    print("链接已断开！")
    tcpClientSocket.close()

udp_addr =('120.48.26.72',5005)

def udp_test(addr):

    BUFSIZE = 8192
    
    s = socket(AF_INET, SOCK_DGRAM)

    while True:
        data = input('>')
        if not data:
            continue
        if data == "q":
            break
            
        # 发送数据
        s.sendto(data.encode('utf-8'),addr)
        # 接收数据
        #data ,recvAddr = s.recvfrom(BUFSIZE)
        #if not data:
            #break
        #print("服务器端响应：", data.decode('utf-8'))

    print("链接已断开！")
    tcpClientSocket.close()

if __name__ == "__main__":
    #main(http_service_addr,True)
    #main(http_service_addr,False)
    #main(tcp_service_addr,False)
    udp_test(udp_addr);