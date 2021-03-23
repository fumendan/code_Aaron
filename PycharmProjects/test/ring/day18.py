#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''格式化输出'''
'''
def foo(*args):
    print(args)
    print(args[2])
    return args

f=foo('s','d','f')
print(f)
'''
'''oop'''
'''
class A():
    def __init__(self,name,age):
        # print(self)
        self.name=name
        self.age=age

    def run(self):
        print('%s is runnging'%self.name)

class B(A):
    def __init__(self,name,age,level):
        # A.__init__(self,name,age)
        super().__init__(name,age)
        self.level=level

    def run(self):
        print('%s run to revier'%self.name)

    def jump(self):
        print('%s is jump'%self.name)

class C(B):
    def __init__(self,name,age,level,phone):
        super().__init__(name,age,level)
        self.phone=phone

    def gogo(self):
        print(self.name,self.age,self.level,self.phone)


b=B('Aaron',23,'3')
b.run()
b.jump()
c=C(b.name,b.age,b.level,'123456789')
c.gogo()
'''
'''
class A():
    def foo(self):
        print('A.foo()')
        self.bar()

    def bar(self):
        print('A.bar()')

class B(A):
    def bar(self):
        print('B.bar()')

b=B()
b.foo()
'''
'''
class A():
    def __init__(self):
        self.bar='QF'

    def bar(self):
        print('A.bar()')

a=A()
a.bar()
'''

'''
def func():
    print('from reflection func')

class Foo():
    x=10
    def __init__(self):
        self.x=100

    def bar(self):
        print('from Foo.foo x:')

print(hasattr(Foo,'x'))
print(getattr(Foo,'x'))

print(setattr(Foo,'x',9))
print('getattr:',getattr(Foo,'x'))
print('del:',delattr(Foo,'x'))
print('del after:',hasattr(Foo,'x'))
print('get bar:',getattr(Foo,'bar'))
print('isexist bar:',hasattr(Foo,'bar'))

getattr(Foo,'bar')('o')
'''
'''
import mod

inp=input('please enter something:')

print('===>mod.ff')
f=getattr(mod,inp)
f()
'''

import importlib
# m=__import__('mod')
m=importlib.import_module('mod')
print(m.foo.bar())

