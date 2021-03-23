#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
'''
conf_file='/root/a.txt' # 要修改的配置文件
old_char='b'            # 老字符
new_char='a'            # 新字符
# old=os.path.dirname(conf_file) # 获取文件路径
# file_name=conf_file.split('/')[len(conf_file.split('/'))-1] # 获取文件名

with open(conf_file,'r') as f,open('.a.txt.swap','w') as ff:
    for line in f:
        data=line.replace(old_char,new_char)
        ff.write(data)
os.remove(conf_file)
os.renames('.a.txt.swap',conf_file)
'''

def legal_path():
    '''
    判断输入的路径是否合法
    如果存在并合法,返回True 有效的配置文件路径
    如果不存在或不合法,返回False ''
    :return:
    '''
    inp=input('The path to the input configuration file:')
    alive_path=os.path.normpath(inp)
    if os.path.exists(alive_path):
        if os.path.isfile(alive_path):
            return True,alive_path
        else:
            print('This is not a document')
            return False,''
    else:
        print('Path unlawful')
        return False,''

def str_conf(conf_file,old_char,new_char):
    '''
    配置文件conf_file,用new_char替换old_char
    :param conf_file: 配置文件路径
    :param old_char: 被替换的字符或字符串
    :param new_char: 替换用的字符或字符串
    :return:
    '''
    with open(conf_file, 'r') as f, open('.conf.swap', 'w') as ff:
        for line in f:
            data = line.replace(old_char, new_char)
            ff.write(data)
    os.remove(conf_file)
    os.renames('.conf.swap', conf_file)

def start_conf(conf_file,start_str):
    '''
    匹配conf_file文件中,以start_str开头的行,打印出来,并输入要替换的内容
    :param conf_file: 配置文件路径
    :param start_str: 匹配开头字符或字符串
    :return:
    '''
    with open(conf_file) as f,open('.conf.swap','w') as ff:
        for line in f:
            if line.startswith(start_str):
                print(line)
                inp=input('Whether or not to modify[y/n]:')
                if inp == 'y' or inp == 'Y':
                    inp=input('Input modified configuration:')
                    ff.write(inp)
                elif inp == 'n'or inp =='N':
                    ff.write(line)
            else:
                ff.write(line)
    os.remove(conf_file)
    os.renames('.conf.swap',conf_file)

def end_conf(conf_file,end_str):
    '''
    匹配conf_file文件中,以end_str结尾的行,打印出来,并输入要替换的内容
    :param conf_file: 配置文件路径
    :param end_str: 匹配结尾字符或字符串
    :return:
    '''
    with open(conf_file) as f,open('.conf.swap','w') as ff:
        for line in f:
            if line.endswith(end_str+'\n'):
                print(line)
                inp=input('Whether or not to modify[y/n]:')
                if inp == 'y' or inp == 'Y':
                    inp=input('Input modified configuration:')
                    ff.write(inp+'\n')
                elif inp == 'n'or inp =='N':
                    ff.write(line)
            else:
                ff.write(line)
    os.remove(conf_file)
    os.renames('.conf.swap',conf_file)
