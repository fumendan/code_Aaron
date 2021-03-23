#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''对象的引用'''
'''
import sys

print(sys.getrefcount('aa'))
print(sys.version)
print(sys.version_info)

import platform
print(platform.version())
print(platform.python_version())
'''
'''OOP面向对象编程'''
'''
class Person():
    def __init__(self,name):
        self.Name=name
        print('I am Dr.%s'%self.Name)

    @staticmethod
    def show():
        print('staticmethod')

    @classmethod
    def pp(cls):
        print(cls,'classmethod')

doctor = Person('Aaron')
# print(Person.__dict__)
# print(doctor.__dict__)
doctor.pp()
Person.pp()
Person.show()
doctor.show()

doctor.ss()
'''

import time
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # @classmethod
    @staticmethod
    def now():  # 用Date.now()的形式去产生实例,该实例用的是当前时间
        t = time.localtime()  # 获取结构化的时间格式
        return Date(t.tm_year, t.tm_mon,t.tm_mday)
        # 上面的意思是 新建一个实例，实例名没有起，但是返回了，也就是，当调用 now() 时，就会得到一个新的实例     @staticmethod

    def tomorrow():  # 用Date.tomorrow()的形式去产生实例,该实例用的是明天的时间
        t = time.localtime(time.time() + 86400)
        return Date(t.tm_year, t.tm_mon, t.tm_mday)


a = Date('1987', 11, 27)  # 自己定义时间
b = Date.now()  # 采用当前时间
c = Date.tomorrow()  # 采用明天的时间

print(a.year, a.month, a.day)
print(b.year, b.month, b.day)
print(c.year, c.month, c.day)


class Site:
    def __init__(self, name, url):
        self.name = name  # public
        self.__url = url  # private

    def who(self):
        print('name  : ', self.name)
        print('url : ', self.__url)

    def __foo(self):  # 私有方法
        print('这是私有方法')

    def foo(self):  # 公共方法
        print('这是公共方法')
        self.__foo()

x = Site('菜鸟教程', 'www.runoob.com')
x.who()  # 正常输出
x.foo()  # 正常输出
# x.__foo()  # 报错

'''
class A():
    x=1
    y=1
    # def __init__(self):
    #     self.x=2
    #     self.y=2

    def show(self):
        print('X:',self.x,'Y:',self.y)

# a=A()
# print(a.show())
'''

'''python内部类'''
'''
class outerclass:
    msg = "I am outer class"

    class interclass:
        msg = "I am inter class"

o1 = outerclass()
print(o1.msg)
i1 = o1.interclass()
print(i1.msg)

i2 = outerclass.interclass()
print(i2.msg)
'''
'''python类的重载'''
'''
class Person:
    def __init__(self, name='Bob', age=20, sex=1):
        self.name = name
        self.age = age
        self.sex = sex

    def printInfo(self):
        print("Person class:name:" + self.name + " age:" + str(self.age) + " sex:" + str(self.sex))


class Student(Person):
    def learn(self):
        print("Student class:learning...")

class collegeStudent(Student):
    def printInfo(self):
        print("collegeStudent class:college student information...")

    def learn(self):
        print("collegeStudent class:add the transaction before calling the super method...")
        super().learn()
        print("collegeStudent class:add the transaction after calling the super method...")

if __name__ == '__main__':
    stu = Student()
    stu.printInfo()
    stu.learn()
    col = collegeStudent()
    col.printInfo()
    col.learn()
'''
'''类的继承'''
'''
class MyType(type):
    def __init__(cls,*args,**kwargs):
        print('MyType.__init__',cls,*args,**kwargs)

    def __call__(cls, *args, **kwargs):
        print('MyType.__init__', cls, *args, **kwargs)
        obj=cls.__new__(cls)
        cls.__init__(obj,*args,**kwargs)
        obj.age=22
        return obj

    def __new__(typ, *args, **kwargs):
        print('MyType.__new__',typ,*args,**kwargs)
        obj=type.__new__(typ,*args,**kwargs)
        return obj
class Foo(object,metaclass=MyType):
    def __init__(self,name):
        self.name=name
        print("Foo.__init__")
    def __call__(self, *args, **kwargs):
        print("call....")

f=Foo('aaron')
print(f.name,f.age)
'''
'''
class Animal(object):
    def run(self):
        print('Animal is running…')

class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running…')

# if __name__ == '__main__':
#     cc=Cat()
#     cc.run()
'''
