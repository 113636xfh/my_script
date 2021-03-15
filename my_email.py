#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 00:56:11 2021

@author: xfh
功能：将dirname中的文件发送到指定邮箱
"""

import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication



sender = ''
reciever = ['']

mail_host = 'pop.qq.com'
mail_user = ''
mail_pass = ''
subject = 'ubuntu文件'
text = '这是来自ubuntu的文件'
dirname = './send'



class Mk_email:
    def __init__(self,mail_user,mail_pass,subject, \
                 text,dirname = './send'):
        threading.Thread.__init__(self)
        self.dirname = dirname
        self.subject = subject
        self.text = text
        self.mail_user = mail_user
        
    def mkpath(self):
        paths = os.listdir(self.dirname)
        dirname = self.dirname
        paths = list(map(lambda x:os.path.join(dirname,x),paths))
        i = 0
        while i < len(paths):
            i += 1
            if not paths:
                break
            if sum(list(map(os.path.getsize,paths[:i]))) > 30*(2**20) :
                paths = paths[i-1:]
                yield paths[:i-1]
                i = 0
            elif i == len(paths):
                yield paths
                break
        
    def mk_message(self,ID):
        message = MIMEMultipart()
        message['From'] = Header(self.mail_user,'utf-8')
        message['To'] = Header(self.mail_user,'utf-8')
        message['Subject'] = Header(self.subject + '-' + str(ID),'utf-8')
        message.attach(MIMEText(self.text,'plain','utf-8'))
        return message
    
    def attach_file(self):
        messages = []
        for i,msg_files in enumerate(self.mkpath()):
            for f in msg_files:
                with open(f,'rb') as fp:
                    msg_file = MIMEApplication(fp.read())
                    msg_file.add_header('Content-Disposition', 'attachment', filename = f)
            msg = self.mk_message(i + 1)
            msg.attach(msg_file)
            messages.append(msg)
        return messages
        
class Send_email(threading.Thread):
    def __init__(self,mail_host,mail_pass,mail_use,ID,sender,receivers,message):
        threading.Thread.__init__(self)
        self.id = ID
        self.mail_pass = mail_pass
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.sender = sender
        self.receivers = receivers
        self.message = message
             
    def run(self):
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host,25)
            smtpObj.login(self.mail_user,self.mail_pass)
            smtpObj.sendmail(self.sender,self.receivers,self.message.as_string())
            print('成功',self.id)
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print('错误',self.id,e)
        
email = Mk_email(mail_user,mail_pass,subject,text,dirname)
messages = email.attach_file() 
i = 0
for msg in messages:
    i += 1
    th = Send_email(mail_host,mail_pass,mail_user,i,sender,reciever,msg)
    th.start()
    