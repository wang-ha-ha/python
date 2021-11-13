from socket import *
import time

HOST = ''
PORT = 6666
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

def tcp_echo():
    recv_count = 0
    send_count = 0
    times = 0
    # 创建监听socket
    tcpServerSocket = socket(AF_INET, SOCK_STREAM)

    # 绑定IP地址和固定端口
    tcpServerSocket.bind(ADDRESS)
    print("服务器启动，监听端口{}...".format(ADDRESS[1]))

    tcpServerSocket.listen(5)

    try:
        while True:
            print('服务器正在运行，等待客户端连接...')

            # client_socket是专为这个客户端服务的socket，client_address是包含客户端IP和端口的元组
            client_socket, client_address = tcpServerSocket.accept()
            print('客户端{}已连接！'.format(client_address))
            recv_count = send_count = times = 0

            try:
                while True:
                    # 接收客户端发来的数据，阻塞，直到有数据到来
                    # 事实上，除非当前客户端关闭后，才会跳转到外层的while循环，即一次只能服务一个客户
                    # 如果客户端关闭了连接，data是空字符串
                    data = client_socket.recv(2048)
                    if data:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                        recv_count += len(data)
                        
                        if times % 10 == 0:
                            data += b"sever echo" * 500
                        
                        data += b"**"
                        
                        client_socket.send(data)
                        print('发送消息 {} 至 {}'.format(data.decode('utf-8'), client_address))
                        send_count += len(data)

                        times += 1
                        print("times:{} recv:{} send:{}".format(times,recv_count,send_count))
                        print()
                        print()
                    else:
                        print("times:{} recv:{} send:{}".format(times,recv_count,send_count))
                        print('客户端 {} 已断开！'.format(client_address))
                        break
            except Exception as e:
                print("times:{} recv:{} send:{}".format(times,recv_count,send_count))
                print('客户端 {} 异常{}！'.format(client_address,e))
            finally:
                # 关闭为这个客户端服务的socket
                client_socket.close()
    finally:
        # 关闭监听socket，不再响应其它客户端连接
        tcpServerSocket.close()

def udp_echo():
    recv_count = 0
    send_count = 0
    times = 0
    
    # 创建监听socket
    udpServerSocket = socket(AF_INET, SOCK_DGRAM)
    
    bindAdress =('',5005)
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
                        recv_count += len(data)
                        #if times % 10 == 0:
                            #data += b"sever echo" * 500
                        times += 1
                        data += b"**"
                        send_count += len(data)
                        # 返回响应数据，将客户端发送来的数据原样返回
                        #udpServerSocket.sendto(data,client_address)
                        #print('发送消息 {} 至 {}'.format(data.decode('utf-8'), client_address))
                    else:
                        print('客户端 {} 已断开！'.format(client_address))
                        break
            except Exception as e:
                print('客户端 {} 异常{}！'.format(client_address,e))
    finally:
        # 关闭监听socket，不再响应其它客户端连接
        udpServerSocket.close()

def recv_file():
    # 创建监听socket
    tcpServerSocket = socket(AF_INET, SOCK_STREAM)

    # 绑定IP地址和固定端口
    tcpServerSocket.bind(ADDRESS)
    print("服务器启动，监听端口{}...".format(ADDRESS[1]))

    tcpServerSocket.listen(5)
    
    print('服务器正在运行，等待客户端连接...')

    # client_socket是专为这个客户端服务的socket，client_address是包含客户端IP和端口的元组
    client_socket, client_address = tcpServerSocket.accept()
    print('客户端{}已连接！'.format(client_address))
    
    f = open("test.pem","wb");
    
    try:
        while True:
            # 接收客户端发来的数据，阻塞，直到有数据到来
            # 事实上，除非当前客户端关闭后，才会跳转到外层的while循环，即一次只能服务一个客户
            # 如果客户端关闭了连接，data是空字符串
            data = client_socket.recv(2048)
            if data:
                print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                f.write(data);
            else:
                print('客户端 {} 已断开！'.format(client_address))
                break
    except Exception as e:
        print('客户端 {} 异常{}！'.format(client_address,e))
    finally:
        # 关闭为这个客户端服务的socket
        client_socket.close()
    tcpServerSocket.close()

if __name__ == "__main__":
    udp_echo()
