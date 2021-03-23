#!/usr/bin/env python3

# print('Import module')

student=[
    {'name':'Aaron','age':23}
]

def showStudent(li):
    for l in li:
        print("name:%-10sage:%-10s" % (l['name'],l['age']))

def addStudent(li):
    name=input('name:')
    age=input('age:')
    li.append({'name':name,'age':age})

def delStudent(li):
    name=input('The name you are going to delete:')
    for item in li:
        if name == item['name']:
            li.remove(item)


if __name__=='__main__':
    print('This is the entrance of the program')