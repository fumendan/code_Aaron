#!/usr/bin/env python3
# coding=utf-8

'''
f=open('mod.py','r',encoding='utf-8')
# print(type(f.read()))                   #<class 'str'>
# print(type(f.readline()))               #<class 'str'>
# print(type(f.readlines()))              #<class 'list'>
print(f.readlines())

f.close()d
'''
'''open通过文件句柄读取文件'''
'''
f=open('mod.py','a')
f.write('\nlaozhang.space')
# f.seek(0)
# print(f.read(5))
print(f.readable())
print(f.writable())


# f.close()
'''
'''with as 方式打开文件操作与open方式打开'''
'''
import time

# print(time.time())
with open('mod.py','r',encoding='utf-8') as f,open('b.txt','w',encoding='utf-8') as ff:
    data=f.read()
    print(data)
    ff.write(data)
# print(time.time())

# print(time.time())
# f=open('mod.py','r',encoding='utf-8')
# print(f.read())
# f.close()
# print(time.time())
'''
'''with as 读取文件，不调用file的方法'''
# with open('a.txt') as f:
#     for line in f:
#         print(line,end='')
'''
markdown
    Typory
'''
'''修改文件内容：通过原文件修改内容创建新文件，把新文件覆盖旧的文件'''
'''
line.startswith(str) # 以什么开头
line.endswitch(str) # 以什么结尾
'''

import os
conf_file='/root/mod.py' # 要修改的配置文件
old_char='b'            # 老字符
new_char='a'            # 新字符
# old=os.path.dirname(conf_file) # 获取文件路径
# file_name=conf_file.split('/')[len(conf_file.split('/'))-1] # 获取文件名

with open(conf_file,'r') as f,open('.mod.py.swap','w') as ff:
    for line in f:
        data=line.replace(old_char,new_char)
        ff.write(data)
os.remove(conf_file)
os.renames('.mod.py.swap',conf_file)

'''运行python脚本传参数'''

