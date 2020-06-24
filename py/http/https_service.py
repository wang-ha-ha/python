
#!/usr/bin/python3
#python version 3.7
from socket import *
from http.server import HTTPServer, BaseHTTPRequestHandler,SimpleHTTPRequestHandler
import threading
import ssl

certificate_file = './certificate.pem'
private_key_file = './private.key'



'''
BaseHTTPRequestHandler.path                    #包含的请求路径和GET请求的数据
BaseHTTPRequestHandler.command                 #请求类型GET、POST...
BaseHTTPRequestHandler.request_version         #请求的协议类型HTTP/1.0、HTTP/1.1
BaseHTTPRequestHandler.headers                 #请求的头
BaseHTTPRequestHandler.responses               #HTTP错误代码及对应错误信息的字典
BaseHTTPRequestHandler.handle()                #用于处理某一连接对象的请求，调用handle_one_request方法处理
BaseHTTPRequestHandler.handle_one_request()    #根据请求类型调用do_XXX()方法，XXX为请求类型
BaseHTTPRequestHandler.do_XXX()                #处理请求
BaseHTTPRequestHandler.send_error()            #发送并记录一个完整的错误回复到客户端,内部调用send_response()方法实现
BaseHTTPRequestHandler.send_response()         #发送一个响应头并记录已接收的请求
BaseHTTPRequestHandler.send_header()           #发送一个指定的HTTP头到输出流。 keyword 应该指定头关键字，value 指定它的值
BaseHTTPRequestHandler.end_headers()           #发送一个空白行，标识发送HTTP头部结束
BaseHTTPRequestHandler.wfile    #self.connection.makefile('rb', self.wbufsize) self.wbufsize = -1 应答的HTTP文本流对象，可写入应答信息
BaseHTTPRequestHandler.rfile    #self.connection.makefile('wb', self.rbufsize) self.rbufsize = 0  请求的HTTP文本流对象，可读取请求信息
'''
class TodoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('Content-Length',len('hello'))
            self.end_headers()  #发送\r\n,意味这下一行为报体
            #send html message,
            self.wfile.write('hello'.encode())
        elif self.path == "/cert":
            try:
                with open("./certificate.pem","rb") as f:
                    flen = f.seek(0,2)
                    f.seek(0,0)
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.send_header('Content-Length',flen)
                    self.end_headers()  #发送\r\n,意味这下一行为报体
                    #send html message,
                    self.wfile.write(f.read())
            except Exception as e:
                print('{}: {}'.format(e.__class__.__name__, e))
                self.send_error(404, "not found.")
        elif self.path == "/thread" :
                self.send_response(200)
                self.send_header('Content-type','text/html')
                
                data = "active_count {}".format(threading.active_count()).encode()
                self.send_header('Content-Length',len(data))
                self.end_headers()
                
                self.wfile.write(data)

    def do_POST(self):
        self.send_error(415, "Only GET is supported.")

def https_service(address):
    print("Starting server, listen at: {}".format(address))
    httpd = HTTPServer(address, TodoHandler)
    
    httpd.socket = ssl.wrap_socket(httpd.socket,certfile=certificate_file, keyfile=private_key_file, server_side=True)
    
    httpd.serve_forever()

def Simple_web_service(address):
    print('Start web_service, listen at: {}'.format(address))
    
    httpd = HTTPServer(address, SimpleHTTPRequestHandler)

    # Wrap the socket with SSL
    httpd.socket = ssl.wrap_socket(httpd.socket,certfile=certificate_file, keyfile=private_key_file, server_side=True)
    
    # Start listening
    httpd.serve_forever()


def echo_client(socket_fd,addr):
    try:
        while True:
            data = socket_fd.recv(8192)
            print('recv msg {}({} bytes) from {}'.format(data.decode('utf-8'), len(data), addr))
            if data == b'':
                break
            socket_fd.send(data)            
            print('send msg {} to {}'.format(data.decode('utf-8'), addr))
            
    except Exception as e:
        print('{}: {}'.format(e.__class__.__name__, e))
    finally:
        socket_fd.close()



def echo_server(address):
    print('Start echo_server, listen at: {}'.format(address))
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    # Wrap with an SSL layer requiring client certs
    s_ssl = ssl.wrap_socket(s,
                            keyfile= private_key_file,
                            certfile= certificate_file,
                            server_side=True
                            )
    # Wait for connections
    try:
        while True:
            c,a = s_ssl.accept()
            print('Got connection {}'.format(a))
            echo_client(c,a)
    except Exception as e:
        print('{}: {}'.format(e.__class__.__name__, e))
    finally:
        s_ssl.close()


https_addr = ('', 8000)
http_addr = ('', 9000)
echo_addr = ('', 8888)

if __name__ == "__main__":
    #Simple_web_service(http_addr)

    t1 = threading.Thread(target=https_service,kwargs={"address":https_addr})
    t2 = threading.Thread(target=Simple_web_service,kwargs={"address":http_addr})
    t3 = threading.Thread(target=echo_server,kwargs={"address":echo_addr})
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()