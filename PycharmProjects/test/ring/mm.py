#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# 导入
import time


# 下面的函数是每个菜单项对应要执行的函数
def timer():
    """
    打印出当前时间
    :return:
    """
    print(time.strftime("%Y-%m-%d  %X"))


def func31():
    print("我是三级菜单的第一项")


def func32():
    print("我是三级菜单的第二项")


def f3():
    print("一级菜单第三项")


# 下面是每一级菜单的内容，列表的名字可以随意起
check_log_menu = [
    ['三级菜单第一项', func31, ''],
    ['三级菜单第二项', func32, ''],

]

# 二级菜单
check_sys = [
    ['二级菜单第一项 ', '', check_log_menu],
]

" [['菜单名称', 函数名，下一级菜单列表名 ]]"

# 顶级菜单列表
menu_list = [
    ['一级菜单第一项', timer, ''],
    ['一级菜单第二项', '', check_sys],
    ['一级菜单第三项', f3, ''],
]

# 定义一个空字典，用来存放动态创建好的菜单项(是个一个字典)
menu_dict = {}

# 定义一个变量，把一开始的顶级菜单的赋值个  current_list
current_list = menu_list

# 存放当前列表的上一层，以被下次循环时使用
up_lay_list = []

import sys

while True:
    # 循环顶级菜单列表，并且创建出一个字典
    # 把 enumerate 函数输出的序号作为这个字段的 key ，值就是每个菜单项(也是个字典)
    for idx, item in enumerate(current_list, 1):
        menu_dict.update({str(idx): {"title": item[0], "func": item[1], "next_menu": item[2]}})

    # print(menu_dict)

    # 循环这个字典打印出当前层级的菜单项和对应的序号
    for k, v in menu_dict.items():
        print(k, v['title'])

    while True:
        # 用户交互函数
        inp = input('>>:')

        # 判断是否输入了值，假如没有输入值，则跳出本层循环
        if not inp: break

        # 输入 'q' , 则系统直接退出
        if inp == 'q':
            sys.exit("系统退出")

        # 如果输入 'b' ,则返回上一层菜单
        if inp == 'b':

            # 判断记录上一层菜单的列表里是否有上一层菜单的值
            if up_lay_list:
                # 从记录上一层菜单的列表里删除最后一个元素并赋值个当前层的变量
                current_list = up_lay_list.pop()

                # 并且此时应该把动态创建菜单的字典进行情况，以便下次循环的时候重新创建新的菜单字典
                menu_dict.clear()
            break

        # 假如输入的值，不存在于菜单字典中，则退出本层循环
        if inp not in menu_dict: break

        # 以上条件都不满足，则证明输入的值是存在于菜单字典的键中
        # 那么通过外层字典的 key 渠道内层字典，随后判断当前取到
        # 的字典中是否有下一级菜单
        elif menu_dict[inp]['next_menu']:

            # 有下一级菜单，就把当前层级的菜单列表，添加到 up_lay_list 列表的最后
            up_lay_list.append(current_list)

            # 并且把当前层级的下一级菜单取出(同样是个嵌套的列表)，赋值给 current_list
            current_list = menu_dict[inp]['next_menu']

            # 同样清空当前菜单字典
            menu_dict.clear()
            break

        # 随后判断当前取到的字典中是否有下对应的函数
        elif menu_dict[inp].get('func'):
            # 得到此函数的对象
            func = menu_dict[inp].get('func')

            # 为了在打印出函数执行结果之前打印出当前菜单项目标题，所以在这里再次循环打印当前菜单的项目标题
            for k, v in menu_dict.items():
                print(k, v['title'])
            print('-' * 20)
            print()

            # 执行对应的函数
            func()

            print()
            print('-' * 20)