#!/usr/bin/env python3

# globals locals global
'''
def getx():
    print('getx==>',locals())
    global x
    x+=1
    print('getx===>',locals())

x=1
print('x:',x)
getx()
print('x==>',x)
print('glocals=>',globals())
'''
# closure function
'''
def f1():
    x=1
    def f2():
        y=2
        def f3():
            print(x,'==',y)
        print('y==>',y)
        return f3
    print('x==>',x)
    return f2

f1()()()
'''

