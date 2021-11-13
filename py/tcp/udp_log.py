from socket import *
import time

def udp_echo(): 
    recv_count = 0
    send_count = 0
    times = 0
    
    # 创建监听socket
    udpServerSocket = socket(AF_INET, SOCK_DGRAM)
    
    bindAdress =('',7770)
    # 绑定IP地址和固定端口
    udpServerSocket.bind(bindAdress)

    try:
        while True:
            try:
                while True:
                    # 接收客户端发来的数据，阻塞，直到有数据到来
                    # 事实上，除非当前客户端关闭后，才会跳转到外层的while循环，即一次只能服务一个客户
                    # 如果客户端关闭了连接，data是空字符串
                    data,client_address = udpServerSocket.recvfrom(2048)
                    if data:
                        print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                        # recv_count += len(data)
                        # #if times % 10 == 0:
                        #     #data += b"sever echo" * 500
                        # times += 1
                        # data += b"**"
                        # send_count += len(data)
                        # # 返回响应数据，将客户端发送来的数据原样返回
                        # udpServerSocket.sendto(data,client_address)
                        # print('发送消息 {} 至 {}'.format(data.decode('utf-8'), client_address))
                    else:
                        print('客户端 {} 已断开！'.format(client_address))
                        break
            except Exception as e:
                print('客户端 {} 异常{}！'.format(client_address,e))
    finally:
        # 关闭监听socket，不再响应其它客户端连接
        udpServerSocket.close()

udp_echo()