#!/usr/bin/env python3

# print jiujiu chengfa biao
def jiu(x,y):
    print('%s*%s=%-4s' % (x,y,x*y),end="")

if __name__=='__main__':
    for i in range(1,10):
        for j in range(1,i+1):
            jiu(j,i)
        print()