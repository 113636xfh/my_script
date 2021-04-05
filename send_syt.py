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

def main():
    '''
    调用前面封装的类，发送

    Returns
    -------
    None.

    '''
    target = ('127.0.0.1', 1202)    #要发送的地址
    udp_send = Udp_send(target)
    for f in mk_files('new'):    #要发送文件的保存路径
        udp_send.main(f)
    #udp_send.close()
        
if __name__ == '__main__':
    i = 0
    while True:
        i += 1
        print(i)
        time.sleep(0.001)
        main()