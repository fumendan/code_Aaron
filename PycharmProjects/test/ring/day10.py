#!/usr/bin/env python3
__auth__='Aaron'
__date__='2018-04-10'

# def foo():
#     print('hello world')
#     print('Aaron')
#     print('glocals:', globals())

# foo()
# print('locals:',locals())

# def f1():
#     def f2():
#         print('f1.f2()')
#     f2()

# f1()

# x=1
# def f1():
#     def f2():
#         print(x)
#     return f2
#
# x=1000
# def f3(func):
#     global x
#     x=2
#     func()
#
# print('x:',x)
# f3(f1())
# print('x:',x)

# x=1
# def answer():
#     print('*'*10,'x:',x)
#
# def run_somthing(arg):
#     global x
#     x=3
#     arg()
#
# x=4
# run_somthing(answer)
# print('x',x)
'''
def add_func(x,y):
    print(x+y)
    return x*y

def run_somting(func,x,y):
    return func(x,y)

def show(i):
    print('==>',i,'<==')

show(run_somting(add_func,4,6))
'''
'''
def outer(arg):
    def inner():
        return 'I am bibaohanshu:{}'.format(arg)
    return inner

f1=outer("hello")
print(f1())
'''
'''
def use_login(name):
    def show():
        return '==>'+name+'<=='
    return show()
# 1.动态生成
# 2.可以使用外部作用于而且非全局作用域的变量
print(use_login('aaron'))
'''
'''
def f1():
    x=1
    y=3
    def f2():
        z=5
        print(locals())
        print(globals())
        nonlocal x
        x+=1
        print(x)
        # print('y:',y)
    return f2

f=f1()
f()
'''
'''
def inner():
    print('    ===name===')
    print("==laozhang.space==")

def show(func):
    def ww():
        print('*'*20)
        func()
        print('*'*20)
    return ww

@show
def ff():
    print('###Aaron###')

ff()

# inner=show(inner)
# inner()
'''
'''
def page(x,y):
    print('I got it')
    print('x:',x,'y:',y)

def pp(func):
    def ww(a,b):
        print('#'*20)
        func(a,b)
        print('#'*20)
        return func(a,b)
    return ww

page=pp(page)
page(4,6)
'''
'''
def pp(func):
    def wrapper(a):
        if a == 'root':
            print('#'*20)
            func()
            print('#'*20)
        else:
            print('no')
    return wrapper
#
# page=pp(page)
# page('root')
# @pp
# def page(x):
#     print('I got it. x:',x)
#
# page('root')

@pp
def go():
    print('I got it. name:')

go('root')
'''

