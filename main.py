#!/usr/bin/env python3
# coding:utf-8

import socket,time,threading,requests,re
from socket import error
# Python time asctime() 函数接受时间元组并返回一个可读的形式为
# "Tue Dec 11 18:07:14 2008"（2008年12月11日 周二18时07分14秒）的24个字符的字符串。
# Python time localtime() 函数类似gmtime()，作用是格式化时间戳为本地的时间。 如果sec参数未输入，则以当前时间为转换标准。
# time.localtime([ sec ])   sec -- 转换为time.struct_time类型的对象的秒数。
localtime = time.asctime(time.localtime(time.time()))
class ProxyServerTest():
    def __init__(self,proxyip):
        # 创建socket对象 本地socket服务
        self.ser = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.proxyip = proxyip

    def run(self):
        try:
            #本地服务ip和端口
            self.ser.bind(("127.0.0.1",5320))
            #最大连接数
            self.ser.listen(10)
        except error as e:
            print("[-]The local server :"+ str(e))
            return "[-]The local server :"+ str(e)
        while True:
            try:
                #接受客户端数据 
                client , addr = self.ser.accept()
                print("[*]accept %s connect" %(addr,))
                date = client.recv(1024)
                if not date:
                    break
                print('[*'+localtime+']: Accept date ...')
            except error as e:
                print('[*]Local recviving client :'+str(e))
                return '[*]Local recviving client :'+str(e)
        while True:
            # 目标代理服务器，将客户端接收到的数据转发给代理服务器
            mbsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('Now proxy ip :'+ str(self.proxyip))
            prip = self.proxyip[0]
            prpo = self.proxyip[1]
            
            try:
                mbsocket.settimeout(3)
                mbsocket.connect(prip,prpo)
            except:
                print('[-]RE_Connect')
                continue
            break
        try:
            mbsocket.send(date)
        except error as e:
            print('[-]Send to the proxy server :' + str(e))
            return '[-]Send to the proxy server :' + str(e)
        
        while True:
            try:
                #从代理服务器接收数据，然后转发给客户端
                date_1 = mbsocket.recv(1024)
                if not date_1:
                    break
                print('[*'+localtime+']: Send date ...')
                client.send(date_1)
            except socket.timeout as e:
                print(self.proxyip)
                print("Back to the client:"+str(e))
                continue
        #断开连接
        client.close()
        mbsocket.close()

def main():
    print("Author:ZhouZiHeng")
    file = open("ip.txt","r")
    for i in file:
        ip = i.split(":")
        ip_list = (ip[0],int(ip[1]))
        print(ip_list)
    
        try:
            try_ip = ProxyServerTest(ip_list)
        except Exception as e:
            print("[-]main : " + str(e))
            return "[-]main : " + str(e)
        
    t = threading.Thread(target=try_ip.run,name='shuaiziheng')
    print("waiting for connection...")
    #关闭多线程
    t.start()
    t.join()

if __name__ == '__main__':
    main()



        
        






