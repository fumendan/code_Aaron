#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''推导式'''
'''
number_thing = (number for number in range(1,6) if number%2==1)

print(number_thing.__next__())
print(number_thing.__next__())
print(number_thing.__next__())

a_set = (number for number in range(1,100) if number%3==1)
print(a_set)
print(a_set.__next__())
print(a_set.__next__())
print(a_set.__next__())
print(a_set.__next__())
print('ssssssssss',next(a_set))
'''
'''异常'''
'''
try:
    x=e+2
except NameError as e:
    print(e)

try:
    inp=input('please inoput something:')
    a=int(inp)
    print(a)
except Exception as e:
    print(e)
else:
    print('ok')
finally:
    print('okokoko')
'''

'''
import traceback

print('ok')
try:
    1 + 'a'
except TypeError as e:
    print(e)
    print('*' * 30)
    traceback.print_exc()
    print('*' * 20)

print('ok')
'''

class Student:
    # count=0
    def __init__(self,name,age,phone):
        self.name=name
        self.age=age
        self.phone=phone
        # Student.count+=1

    def getStu(self):
        return self

'''
if __name__ == '__main__':
    ss=Student('Aaron',23,'1234567890')
    dd=Student('murongjin',24,'123456')
    print(dd.getStu().name)
    print(dd.getStu().age)
    print(dd.getStu().phone)
    print(Student.count)
'''


class SS(Student):
    def __init__(self,name,age,phone,address):
        Student.__init__(self,name,age,phone)
        self.address=address

    def getSS(self):
        return self

if __name__ == '__main__':
    bb=SS('aaron',22,'1234567','ainidajie')
    cc=bb.getSS()
    print(cc)
    print(cc.name)
    print(cc.age)
    print(cc.phone)
    print(cc.address)
