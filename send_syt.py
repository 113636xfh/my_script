#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 14:39:14 2021

@author: xfh
"""

import socket
import os
import time
import sys
import threading
from queue import Queue

class Udp_send:
    def __init__(self,target):
        self.udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.target = target    
            
    def send_line(self,line):
        #time.sleep(0.001)
        self.udp_socket.sendto(line,self.target)
    
    def main(self,item):
        self.size = len(item)
        self.send_line(item)
        print(self.size)
    
    def close(self):
        self.udp_socket.close()
        
class Tcp_send:
    def __init__(self, target):
        try:
            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.connect(target)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
            
    def send_line(self, line):
        self.s.send(line)
        
    def pack_line(self, line):
        if type(line) == 'str':
            line = bytes(line, encoding = 'utf-8')
        else:
            line = bytes(line)
        return line
        
    def main(self, item):
        self.size = len(item)
        line = self.pack_line(item)
        self.send_line(line)
        print(self.size)
        
    def close(self):
        self.s.close()
        
            
def mk_files(path):
    '''
    读取文件，返回二进制流

    Parameters
    ----------
    path : str
        文件路径

    Yields
    ------
    TYPE
        二进制流

    '''
    file_list = os.listdir(path)
    file_list = list(map(lambda x:os.path.join(path, x),file_list))
    for f in file_list:
        with open(f,'rb') as byte_f:
            #print(type(byte_f.read()))
            yield byte_f.read()  
        #os.remove(f) #把发过的文件删除

def main_udp(target):
    '''
    调用前面封装的类，发送
    开始运行后，只要有文件放入，便开始发送

    Returns
    -------
    None.

    '''
    i = 0
    udp_send = Udp_send(target)
    while True:
        time.sleep(0.02)
        for f in mk_files('new'):    #要发送文件的保存路径
            udp_send.main(f)
            i += 1
            print(i)
        #udp_send.close()
        
def main_tcp(target, update):
    '''
    调用前面封装的类，发送

    Parameters
    ----------
    target : tuple
        地址

    Returns
    -------
    None.

    '''
    ViewPara_flag = update.get()
    if ViewPara_flag != None:
        tcp_send = Tcp_send(target)
        tcp_send(ViewPara_flag)
        print(ViewPara_flag,'已发送')
                
if __name__ == '__main__':
    update = Queue()
    target_udp = ('127.0.0.1', 1202)    #要发送的地址
    target_tcp = ('127.0.0.1', 1203) 
    ViewPara_flag = 1234     #要用tcp发送的变量
    update.put(ViewPara_flag) #更新变量
    p_udp = threading.Thread(target = main_udp, args = (target_udp,))
    p_tcp = threading.Thread(target = main_tcp, args = (target_tcp, update))
       
    p_udp.start()
    p_tcp.start()
    p_udp.join()
    p_tcp.join()
    