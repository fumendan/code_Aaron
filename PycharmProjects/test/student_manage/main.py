#!/usr/bin/env python3

import sys
import student_manage.student as stu
# import echo as stu

# print(stu.student)
# stu.addStudent(stu.student)
# stu.showStudent(stu.student)

def func_help():
    print('''
add     Add a student information
del     Delete a student's information
show    Display a student information
help    Print this help message
exit    End procedure
''')

func_list=['add','del','show','help','exit']

func_help()

while True:
    inp=input('Input function code:').strip()
    if not inp:
        continue
    if inp not in func_list:
        print('You enter the error, please retype.')
    if inp == 'add':
        stu.addStudent(stu.student)
    if inp == 'del':
        stu.delStudent(stu.student)
    if inp == 'show':
        stu.showStudent(stu.student)
    if inp == 'help':
        func_help()
    if inp == 'exit':
        sys.exit('system exit')

