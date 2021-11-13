#!/usr/bin/python3
# python version 3.7
from socket import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import configparser

# screen_parm_conf_file = "screen_parm.ini"
screen_parm_conf_file = "/root/magicframe/screen_parm.ini"
# conf = configparser.ConfigParser() 这个会把原始配置文件全变成小写
# 重载大小写
screen_parm_conf= configparser.RawConfigParser()
screen_parm_conf.optionxform = lambda option: option
screen_parm_conf.read(screen_parm_conf_file,encoding="utf-8")

def screen_parm_conf_save():
    screen_parm_conf.write(open(screen_parm_conf_file, 'w'))
    os.system("sync")

GET = "GET"
POST = "POST"

post_dict = {}
get_dict = {}

def WebRoute(method=None, routePath=None, name=None) :

    if type(method) is type(lambda x:x) and not routePath :
        raise ValueError('[@WebRoute] arguments are required for this decorator.')
    
    def decorated(handler) :
        if(method == GET):
            get_dict[routePath] = handler
        elif(method == POST):
            post_dict[routePath] = handler
        s = (' (%s)' % name) if name else ''
        print(' + [@WebRoute] %s %s' % (method, routePath) + s)
        return handler
    
    return decorated

@WebRoute(POST,"/picture_get_data")
def post_handle_picture_get_data(self):
    data = self.rfile.read(int(self.headers['content-length']))
    rjson = json.loads(data.decode('utf-8'))
    
    i = rjson["data"]
    item_name = "luma_{}".format(i)
    send_data = {}
    for name in screen_parm_conf.options(item_name):
        send_data[name] = screen_parm_conf.getint(item_name,name)
    print(item_name,send_data)

    cmd_line = "/root/magicframe/client 4{}".format(i)
    os.system(cmd_line)

    send_data = json.dumps(send_data)
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    # self.send_header('Content-Length',len(send_data))
    self.end_headers()
    self.wfile.write(send_data.encode())

@WebRoute(POST,"/wb_get_data")
def post_handle_wb_get_data(self):
    data = self.rfile.read(int(self.headers['content-length']))
    rjson = json.loads(data.decode('utf-8'))
    
    i = rjson["data"]
    item_name = "color_temper_{}".format(i) 
    send_data = {}
    for name in screen_parm_conf.options(item_name):
        send_data[name] = screen_parm_conf.getint(item_name,name)

    cmd_line = "/root/magicframe/client 5{}".format(i)
    os.system(cmd_line)

    send_data = json.dumps(send_data)
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    # self.send_header('Content-Length',len(send_data))
    self.end_headers()
    self.wfile.write(send_data.encode())

@WebRoute(POST,"/test_picture_set")
def post_handle_test_picture_set(self):
    data = self.rfile.read(int(self.headers['content-length']))
    rjson = json.loads(data.decode('utf-8'))
    i = rjson["data"]

    cmd_line = "/root/magicframe/client 10{}".format(i)
    os.system(cmd_line)

    self.send_response(200)
    self.end_headers()

@WebRoute(POST,"/picture_choose_1")
@WebRoute(POST,"/picture_choose_2")
@WebRoute(POST,"/picture_choose_3")
def post_handle_picture_choose(self):
    data = self.rfile.read(int(self.headers['content-length']))

    d = self._parse_form(data.decode())
    i = int(self.path[-1])
    item_name = item_name = "luma_{}".format(i) 
    d = self._parse_form(data.decode())
    for name in screen_parm_conf.options(item_name):
        if(name != 'eCscMatrix'):
            screen_parm_conf.set(item_name,name,d[name])
    print(screen_parm_conf.items(item_name))
    screen_parm_conf_save()
    cmd_line = "/root/magicframe/client 4{}".format(i)
    os.system(cmd_line)

    self.send_response(200)
    self.end_headers()

@WebRoute(POST,"/wb_choose_1")
@WebRoute(POST,"/wb_choose_2")
@WebRoute(POST,"/wb_choose_3")
def post_handle_wb_choose(self):
    data = self.rfile.read(int(self.headers['content-length']))

    d = self._parse_form(data.decode())
    i = int(self.path[-1])
    item_name = item_name = "color_temper_{}".format(i) 
    d = self._parse_form(data.decode())
    for name in screen_parm_conf.options(item_name):
        screen_parm_conf.set(item_name,name,d[name])
    print(screen_parm_conf.items(item_name))
    screen_parm_conf_save()
    cmd_line = "/root/magicframe/client 5{}".format(i)
    os.system(cmd_line)

    self.send_response(200)
    self.end_headers()

@WebRoute(POST,"/curve_get_data")
def post_handle_curve_get_data(self):
    data = self.rfile.read(int(self.headers['content-length']))
    rjson = json.loads(data.decode('utf-8'))
    
    i = rjson["data"]
    item_names = ["luma_curve","contrast_curve","hue_curve","saturation_curve","sharpness_curve"]
    item_name = item_names[i - 1]
    send_data = {}
    for name in screen_parm_conf.options(item_name):
        send_data[name] = screen_parm_conf.getint(item_name,name)

    send_data = json.dumps(send_data)
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    # self.send_header('Content-Length',len(send_data))
    self.end_headers()
    self.wfile.write(send_data.encode())

@WebRoute(POST,"/curve_choose_1")
@WebRoute(POST,"/curve_choose_2")
@WebRoute(POST,"/curve_choose_3")
@WebRoute(POST,"/curve_choose_4")
@WebRoute(POST,"/curve_choose_5")
def post_handle_curve_choose(self):
    data = self.rfile.read(int(self.headers['content-length']))

    i = int(self.path[-1])
    item_names = ["luma_curve","contrast_curve","hue_curve","saturation_curve","sharpness_curve"]
    item_name = item_names[i - 1]
    d = self._parse_form(data.decode())
    for name in screen_parm_conf.options(item_name):
        screen_parm_conf.set(item_name,name,d[name])
    print(screen_parm_conf.items(item_name))
    screen_parm_conf_save()

    self.send_response(200)
    self.end_headers()


class TodoHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _parse_form(self, msg):
        msg = msg.split('&')
        d = {}

        for i in msg:
            t = i.split('=')
            d[t[0]] = t[1]
        
        return d

    def do_GET(self):
        f = get_dict.get(self.path);
        if f != None:
            f(self)
        elif self.path == '/' :
            with open("index.html",encoding = 'UTF-8') as f:
                data = f.read()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.send_header('Content-Length',len(data.encode()))
                self.end_headers()  #发送\r\n,意味这下一行为报体
                #send html message,
                self.wfile.write(data.encode())
        else:
            path = self.path[1:]
            if os.path.isfile(path):
                with open(path,encoding = 'UTF-8') as f:
                    data = f.read()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', len(data.encode()))
                self.end_headers()

                self.wfile.write(data.encode('utf-8'))
            else:
                self.send_error(404)

    def do_POST(self):
        f = post_dict.get(self.path);
        if f != None:
            f(self)
        else:
            self.send_error(404)

def https_service(address):
    print("Starting server, listen at: {}".format(address))
    httpd = HTTPServer(address, TodoHandler)

    httpd.serve_forever()


https_addr = ('', 8000)
https_service(https_addr)
