#!/usr/bin/env python3
# coding=utf-8

from lib import func_lib

# Three level menu
check_log_menu = [
    ['Three_level_menu1', func_lib.f31, ''],
    ['Three_level_menu2', func_lib.f32, ''],
]

# Two level menu
check_sys = [
    ['Two_level_menu2', '',check_log_menu],
]

# First level menu
menu_list = [
    ['First_level_menu1', func_lib.timer, ''],
    ['First_level_menu2', '', check_sys],
    ['First_level_menu3', func_lib.f3, ''],
]
