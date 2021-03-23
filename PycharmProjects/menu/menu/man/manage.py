#!/usr/bin/env python3
# coding=utf-8

import sys
from conf import settings

def man():
    menu_dict = {}
    current_list = settings.menu_list
    up_lay_list = []

    while True:
        for idx, item in enumerate(current_list, 1):
            menu_dict.update({str(idx):{'title':item[0],'func':item[1],'next_menu':item[2]}})

        for k, v in menu_dict.items():
            print(k,v['title'])

        while True:
            inp=input('##=>:')
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
                func()
                print('-'*20)