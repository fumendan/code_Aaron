#!/usr/bin/env python3
# coding=utf-8

def start(func):
    def wrapper():
        print('*'*20)
        func()
        print('*'*20)
    return wrapper