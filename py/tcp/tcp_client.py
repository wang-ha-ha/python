from socket import *

def main():
    HOST = '192.168.199.145'
    PORT = 6666
    BUFSIZE = 1024
    ADDRESS = (HOST, PORT)

    tcpClientSocket = socket(AF_INET, SOCK_STREAM)
    tcpClientSocket.connect(ADDRESS)

    while True:
        data = input('>')
        if not data:
            continue
        if data == "q":
            break
            
        # 发送数据
        tcpClientSocket.send(data.encode('utf-8'))
        # 接收数据
        data, ADDR = tcpClientSocket.recvfrom(BUFSIZE)
        if not data:
            break
        print("服务器端响应：", data.decode('utf-8'))

    print("链接已断开！")
    tcpClientSocket.close()

if __name__ == "__main__":
    main()
