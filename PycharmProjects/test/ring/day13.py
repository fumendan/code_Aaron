#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import subprocess
# subprocess 使用shell
'''
sub=subprocess.getoutput('cat /root/mod.py | grep 7')
print(type(sub))
print(sub)
'''
# 不使用shell,调用系统的python接口
'''
ret = subprocess.check_call(['date', '-u'])
print(ret)

ll=subprocess.getoutput('ls')
print(ll)
'''
'''loggin'''

import logging

# create logger
logger = logging.getLogger('TEST-LOG') # getLogger(name=None) return root
logger.setLevel(logging.DEBUG) # log level
# logger.setLevel(logging.WARN)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# ch.setLevel(logging.WARN)

# create file handler and set level to warning
fh = logging.FileHandler("access.log")
# fh.setLevel(logging.WARNING)
fh.setLevel(logging.DEBUG)

# create formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

#实例：
try:
    a=r+1
except Exception as e:
    logger.error(e)


import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.18.44.120', port=22, username='root')
stdin, stdout, stderr = ssh.exec_command('ls')
result = stdout.read()
print(result)
ssh.close()