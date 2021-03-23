#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib import func_lib
import sys

def show_func():
    print('''
1   替换文件的内容
2   匹配行首,修改行
3   匹配行尾,修改行
q   system exit
    ''')

def man():
    bool_path,conf_path=func_lib.legal_path()
    if bool_path:
        show_func()
        while True:
            inp=input('Input function code:')
            if not inp:
                break
            if inp == '1':
                old_str=input('Please enter the old_char:')
                new_str=input('Please enter the new_char:')
                func_lib.str_conf(conf_path,old_str,new_str)
            elif inp=='2':
                start_str=input('Please enter the start_str:')
                func_lib.start_conf(conf_path,start_str)
            elif inp=='3':
                end_str=input('Please enter the end_str:')
                func_lib.end_conf(conf_path,end_str)
            elif inp=='q':
                sys.exit('system exit')
    else:
        sys.exit('system exit')
