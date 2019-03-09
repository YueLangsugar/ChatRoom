import os,sys,signal
from socket import *

server_addr = (('127.0.0.1',9696))

def msg_recv(sockfd):       ##接收消息
    while True:
        data = sockfd.recv(1024)
        if data.decode() == 'q':
            break
        print(data.decode())

def msg_send(sockfd,name):      ##发送消息
    while True:
        try:
            data = input("发言>>")
        except KeyboardInterrupt:
            data = 'quit'
        if data == 'quit':  ##退出
            msg = 'Q %s'%name
            sockfd.send(msg.encode())
            break
        else:
            msg = 'C %s %s'%(data,name)
            sockfd.send(msg.encode())

def main():
    sockfd = socket()##创建套接字
    
    try:
        sockfd.connect(server_addr)
    except Exception:
        print("连接失败")
        sockfd.close()
        return
    
    while True:             ####输入姓名登录
        name = input("请输入昵称:")
        sockfd.send(('L '+name).encode())   ## L 区分消息类型
        data = sockfd.recv(128)
        if data.decode() == 'OK':
            print("你已经进入9696聊天室")
            break
        else:
            print(data.decode())

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    pid = os.fork()

    if pid < 0:
        sys.exit("err")  
    elif pid == 0:        ##子进程
        msg_recv(sockfd)
    else:
        msg_send(sockfd,name) 
    sys.exit("退出")
     

if __name__ == "__main__":
    main()

