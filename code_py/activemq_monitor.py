#-*- coding:utf-8 -*-

"""
python2

使用方法：
执行脚本可添加参数，如：
python parsemq.py aaa bbb
即只打印消息队列aaa与bbb的信息
python parsemq.py
不写参数，打印出全部的消息队列信息
python parsemq.py -r 每隔一秒循环打印全部
python parsemq.py -r  aaa bbb 每隔一秒循环打印aaa与bbb的信息
"""
import urllib2,urllib
import HTMLParser
import os
import sys
import time
 
#解析html
class MyHTMLParser(HTMLParser.HTMLParser):
   def __init__(self):
      HTMLParser.HTMLParser.__init__(self)
      self.trflag = False
      self.tdflag = False
      self.tdcount = 0
      self.data = []
   #标签开始,这里只关心tr与td
   def handle_starttag(self, tag, attrs):
      if tag == 'tr':
         self.trflag = True
         self.tdcount = 0
      if self.trflag == True and tag == 'td':
         self.tdcount = self.tdcount + 1
         #只关心前五个
         if self.tdcount <= 5:
            self.tdflag = True
         else:
            self.tdflag = False
   #标签结束,这里只关心tr与td
   def handle_endtag(self, tag):
      if tag == "tr":
         self.trflag = False
         self.tdflag = False
         self.printdatas()
         self.data = []
      if tag == 'td' and self.tdflag == True:
         self.tdflag = False
    #得到data
   def handle_data(self, data):
      if self.tdflag == True:
         if data:
            #去除回车
            data1 = data.replace('\r','').replace('\n','')
            self.data.append(data1)
   #打印信息
   def printdata(self):
       print "~~~~~~~~~~~~~~~~~~~~~"
       print "queue     :" ,self.data[0]
       print "pending   :" ,self.data[1]
       print "consummers:" ,self.data[2]
       print "enqueued  :" ,self.data[3]
       print "dequeued  :" ,self.data[4]
 
   def printdatas(self):
       if len(self.data) == 5:
           if len(forcusmq) != 0:
               for forcusdata in forcusmq:
                   if self.data[0] == forcusdata:
                       self.printdata()
                       break
           else:
               self.printdata()
 
def pararg():
    if len(sys.argv) > 1:
        print sys.argv[1]
        if sys.argv[1] == "-r":
            global isfor
            isfor = 1
            if len(sys.argv) > 2:
                for i in range(2,len(sys.argv)):
                    forcusmq.append(str(sys.argv[i]))
        else:
            for i in range(1,len(sys.argv)):
                forcusmq.append(str(sys.argv[i]))
    if len(forcusmq):
        print "output queue:",
        for i in forcusmq:
            print i,
        print
 
def getmqip():
    mqip = raw_input("input mq ip:")
    print "mq ip:", mqip
    return mqip
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
forcusmq = []
isfor = 0
 
pararg()
#mqip = getmqip()
mqip='192.168.174.129'

user = "admin"
passwd = "admin"
login_url = "http://%s:8161/admin/queues.jsp" % mqip
print "connect to",login_url
 
#urllib2抓取html
passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
passwdmgr.add_password(None, login_url, user, passwd)
httpauth_hander = urllib2.HTTPBasicAuthHandler(passwdmgr)
opener = urllib2.build_opener(httpauth_hander)
urllib2.install_opener(opener)
 
while True:
    os.system('clear')
    print "__________________",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"____________________"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~begin~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    req = urllib2.Request(login_url)
    res = urllib2.urlopen(req)
    data = res.read()

    myhtml = MyHTMLParser()
    myhtml.feed(data)
    myhtml.close()
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    if isfor == 0:
        break
    time.sleep(1)
 
exit()
