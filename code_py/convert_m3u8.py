#!/usr/bin/env/python
#_*_coding:utf-8_*_
#Data:2017-10-02
#Auther:苏莫
#Link:http://blog.csdn.net/lingluofengzang
#PythonVersion:python2.7
#filename:convert_m3u8.py
 
import os
import sys
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
# 检查文件路径及文件是否正确
def check_path_file(_path, _file):
 
    # 判断路径是否存在
    # os.path.isdir(path)  判断路径是否为目录
    # os.path.isabs(path)  判断是否为绝对路径
    if os.path.isdir(_path) or os.path.isabs(_path):
        # 判断文件是否存在
        # os.path.join(path1[, path2[, ...]])  把目录和文件名合成一个路径
        # os.path.exists(path)  路径存在则返回True,路径损坏返回False
        if os.path.exists(os.path.join(_path, _file)):
            print u'>>>[-] 目标文件已经存在。'
            exit(0)
 
        return True
 
    else:
        print u'>>>[-] 路径不存在。'
        exit(0)
 
# 更改后缀名为[.ts]
def change_file_name(_path):
 
    # 获取路径下的文件名
    files = os.listdir(_path)
 
    for filename in files:
        # 文件名分割 文件名称+后缀
        portion = os.path.splitext(filename)
        if portion[1] != '.m3u8' or portion[1] == '':
            newname = portion[0]+".ts"
            # 切换到文件所在路径
            os.chdir(_path)
            # 更换文件后缀
            os.rename(filename,newname)
 
    return True
 
# 对[.ts]文件进行排序
def sort_file(_path, num = '1'):
 
    if num == '1':
        change_file_name(_path)
    file_lists = os.listdir(_path)
 
    file_list = []
 
    for file in file_lists:
        portion = os.path.splitext(file)
        if portion[1] == '.ts':
            file_list.append(int(portion[0]))
 
    file_list.sort()
    return file_list
 
# 合并文件
def convert_file(_path, files, filename):
 
    tmp = []
    for file in files:
        tmp.append(str(file) + '.ts')
    # 合并ts文件
    os.chdir(_path)
    shell_str = '+'.join(tmp)
    shell_str = 'copy /b '+ shell_str + ' ' + filename
    os.system(shell_str)
    # 删除ts和m3u8文件
    os.system('del /Q *.ts')
    os.system('del /Q *.m3u8')
 
if __name__ == '__main__':
 
    print '-' * 60 + '\n'
    print u'将m3u8格式的视频转换成mp4格式'.center(60) + '\n'
    print '-' * 60
 
    try:
 
        _path = raw_input(unicode('>>>[+] 请输入m3u8视频所在目录\n>>>[+] ').encode('utf-8'))
        _file = raw_input(unicode('>>>[+] 请输入mp4的文件名\n>>>[+] ').encode('utf-8'))+'.mp4'
        print u'>>>[+] 是否需要将m3u8视频后缀名转换为[.ts]'
        num = raw_input('>>>[+] Yes:1 No:2\n>>>[+] [1]')
 
        flag = check_path_file(_path, _file)
 
        if flag:
            if num == '2':
                files = sort_file(_path, num)
            else:
                files = sort_file(_path)
            print '-' * 60
            convert_file(_path, files, _file)
 
    except Exception as e:
        print e
