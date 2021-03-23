#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 迭代器
'''
li=[x+1 for x in range(10)]
it=iter(li)
print(next(it))
print('it:',it)
print('li:',li)
'''
# 生成器
'''
import sys

def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1

f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成


while True:
    try:
        print(next(f), end=" ")
    except StopIteration:
        sys.exit()
'''

def add(n, i):
    return n + i

def test():
    for i in range(4):
        yield i

g = test() # [0,1,2,3]

for n in [1,10]:
    g = (add(n, i) for i in g)
    # n=1   g=(n+i for i in g)
    # n=10  g=(n+n+i for i in g)=(20,21,22,23)

# 结果？
print(list(g))