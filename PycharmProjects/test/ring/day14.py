#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''python 3 操作数据库'''

#连接memcached
'''
import memcache
mc=memcache.Client(
    [
        ('192.168.122.4:11211',2),
        # ('10.18.44.178:11211',1),
    ],debug=True)
# mc.set('li',['a','b','c','d'])
mc.set_multi({'a':'a1','b':'b1','c':'c3'})
# mc.add('name','yingying')
# print(mc.get('li'))
print(mc.get('b'))
print(mc.get_multi('b'))
'''
#连接redis
'''
import redis

r=redis.Redis(host='192.168.122.247',port=6379)
r.set('name','Aaron')
r.set('li',['a','b','c','d'])
print(r.get('name'))
print(r.get('name').decode('utf-8'))
print(r.get('li').decode('utf-8'))
'''
#连接mongodb
'''
from pymongo import MongoClient
from bson.objectid import ObjectId

cl=MongoClient('10.18.44.159',27017)

# db=cl.mydb # 创建数据库mydb
# myset=db.myset # 创建集合myset
# myset_id=myset.insert_id #获取集合id

print('*'*20)
print('all databases name:',cl.database_names())
db=cl.pp
print('databases',db)
myset=db.myset
# set_id=myset.insert({'go':'gogo','run':'runrun'})
# print('get someting by id:',myset.find_one({'_id':set_id}))
print('pp.myset:',myset.find_one())
print('*'*20)
# for i in myset.find({'go':'gogo'}):
for i in myset.find():
    if i['_id'] == ObjectId('5ad1ae2d21c2510f6e79e71e'):
        myset.remove(i)
    print(i)
print('json count:',myset.count())
'''

import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='webtest')
cursor=conn.cursor()
effect_row = cursor.execute("select * from student")
print(cursor)
print(effect_row)
for i in cursor.fetchall():
    print(i)
