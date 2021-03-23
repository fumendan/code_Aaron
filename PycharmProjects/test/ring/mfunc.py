#!/usr/bin/env python3
# coding=utf8

import time
import sys

def timer():
    print(time.strftime('%Y-%m-%d %X'))

def f31():
    print('this is f31')

def f32():
    print('this is f32')

def f3():
    print('this is f3')

# 一级菜单
check_log_menu = [
    ['三级菜单第一项', f31, ''],
    ['三级菜单第二项', f32, ''],
]

# 二级菜单
check_sys = [
    ['二级菜单第一项', '',check_log_menu],
]

# 顶级菜单列表
menu_list = [
    ['一级菜单第一项', timer, ''],
    ['一级菜单第二项', '', check_sys],
    ['一级菜单第三项', f3, ''],
]

menu_dict = {}
current_list = menu_list
up_lay_list = []

while True:
    for idx, item in enumerate(current_list, 1):
        menu_dict.update({str(idx): {'title': item[0], 'func': item[1], 'next_menu': item[2]}})

    for k, v in menu_dict.items():
        print(k,v['title'])

    while True:
        inp=input('--|:')
        if not inp: break

        if inp == 'q':
            sys.exit('system exit')
        if inp == 'b':
            if up_lay_list:
                current_list=up_lay_list.pop()
                menu_dict.clear()
            break

        if inp not in menu_dict: break
        elif menu_dict[inp]['next_menu']:
            up_lay_list.append(current_list)
            current_list=menu_dict[inp]['next_menu']
            menu_dict.clear()
            break
        elif menu_dict[inp].get('func'):
            func=menu_dict[inp].get('func')

            for k,v in menu_dict.items():
                print(k,v['title'])

            print('-'*20)
            print()
            func()
            print()
            print('-'*20)
