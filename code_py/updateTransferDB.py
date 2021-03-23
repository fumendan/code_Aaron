#!/usr/bin/env python3
# -*- encoding:utf-8
import sqlite3
import sys

if len(sys.argv)==3:
	dataOld=sys.argv[1]
	dataNew=sys.argv[2]
else:
	print("Usage:",sys.argv[0],"old.db new.db")
	sys.exit()

#dataOld = sys.argv[1]  # 旧版本的数据库，有数据，需要修改表结构
#dataNew = sys.argv[2]  # 新版本的数据库，无数据
# tableList = ['T_COL_USER', 'T_DIR_CLEAR', 'T_DIR_COL', 'T_DIR_PROXY', 'T_GLOBALINFO', 'T_SEND_USER']

'''
显示两个数据库中所有表结构的差异

dataOld 旧版本数据库文件路径
dataNew 新版本数据库文件路径
'''

olddb = sqlite3.connect(dataOld)
oldCur = olddb.cursor()
oldCur.execute("select name from sqlite_master where type='table'")
oldTables = oldCur.fetchall()
oldTables = [line[0] for line in oldTables]

newdb = sqlite3.connect(dataNew)
newCur = newdb.cursor()
newCur.execute("select name from sqlite_master where type='table'")
newTables = newCur.fetchall()
newTables = [line[0] for line in newTables]

# 两个数据库中表名的并集
tableList = set(oldTables) | set(newTables)


# 比较两边列属性是否都相同，证明两表的表结构是否相同
def tabIsSame(oldCur, newCur, tab_name):
    oldCur.execute("PRAGMA table_info({})".format(tab_name))
    newCur.execute("PRAGMA table_info({})".format(tab_name))
    return set([old[1:] for old in oldCur.fetchall()]) == set([new[1:] for new in newCur.fetchall()])


# 传入两个list，比较两个表的列属性
def colIsSame(oldCol, newCol):
    oldcopy = oldCol.copy()
    newcopy = newCol.copy()
    for oitem in oldCol:
        # 字段属性一样，从列表移除
        if oitem in newCol:
            oldcopy.remove(oitem)
            newcopy.remove(oitem)
    # 列表中包含的字段属性不一样，打印输出
    print("\toldcol====>", oldcopy)
    print("\tnewcol====>", newcopy)


# 根据表名，查询旧新两边的列属性，返回两个列表
def tabColList(oldCur, newCur, tab_name):
    oldCur.execute("PRAGMA table_info({})".format(tab_name))
    newCur.execute("PRAGMA table_info({})".format(tab_name))
    return [old[1:] for old in oldCur.fetchall()], [new[1:] for new in newCur.fetchall()]


# 表结构整体对比
print("列属性元组：(名,类型(长度),NOT NULL,默认值,PRIMARY KEY)，空值为1，主键为1")
for tab_name in tableList:
    if tabIsSame(oldCur, newCur, tab_name):
        # 两库对应的表结构一样
        print(tab_name, 'is ok')
    elif tab_name in oldTables and tab_name not in newTables:
        # 旧表需要删除
        print(tab_name, "in the old database")
    elif tab_name not in oldTables and tab_name in newTables:
        # 新表需要创建
        print(tab_name, "in the new database")
    else:
        # 两库对应的表不一样,需要修改字段属性
        print(tab_name, 'is no')
        oldCol, newCol = tabColList(oldCur, newCur, tab_name)
        colIsSame(oldCol, newCol)
print("程序显示Transfer对比结果完成！")

