###tcp_chat_room_server.py
###tcp聊天室服务端
from threading import Thread
from socket import *
import os,sys

Host = '0.0.0.0'
Post = 9696
address = (Host,Post)

chat_name = {}   ## name:conn
jobs = {}   ###conn:t  存储线程对象t    
#conn_stat = {}   ###  conn:'true'  存储套接字的状态　true为运行　　false 为结束线程

def do_login(conn,name):        ##登录
    if name not in chat_name:
        conn.send(b'OK')
    else:
        conn.send("昵称已经存在".encode())
        return
    msg = "%s 进入9696聊天室" %name
    for c in chat_name:
        chat_name[c].send(msg.encode())
    chat_name[name] = conn

def do_chat(conn,msg,name):
    text = "%s :%s"%(name,msg)
    for n in chat_name:
        if n != name:
            chat_name[n].send(text.encode())

def do_quit(conn,name):
    msg = "%s 退出9696聊天室了"%name
    for c in chat_name:
        if c == name:
            conn.send(b'q')
        else:
            chat_name[c].send(msg.encode())
    del chat_name[name]
    #conn_stat[conn] = 'false'
    conn.close()

def do_request(conn):   ##用来处理客户端的请求
    while True:
        data = conn.recv(1024).decode().strip().split(' ')
        if data[0] == 'L':   ##登录
            name = data[-1]
            do_login(conn,name)
        elif data[0] == 'C':    ##聊天
            name = data[-1]
            msg = ''.join(data[1:-1])
            do_chat(conn,msg,name)
        elif data[0] == 'Q':  ##退出
            name = data[-1]
            do_quit(conn,name)
            break
        
def main():
    
    sockfd = socket()  ##tcp套接字
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)    ##端口重用
    sockfd.bind(address)
    sockfd.listen(5)

    while True:
        try:
            conn,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("退出")
        except Exception as e:
            print(e)
            continue
        print("Connect from:",addr)
        t = Thread(target=do_request,args=(conn,))
        t.start()
        jobs[conn] = t
        #conn_stat[conn] = 'true'
        ###回收线程　　当有线程结束，只有当新的客户端连接进来才会回收结束的线程
        for c in jobs:
            if c._closed is True:
                jobs[c].join()
                print(jobs)

if __name__ == '__main__':
    main()