# -*- coding: utf-8 -*-
import datetime
import pymongo
from SharkAPAMP import settings


class Mongodb(object):
    """Mongobd的CURD"""

    def __init__(self, *args, **kwargs):
        self.mongo_host = settings.MONGO_HOST
        self.mongo_port = int(settings.MONGO_PORT)
        self.mongo_db = settings.MONGO_DB
        self.mongo_collection = settings.MONGO_COLLECTION
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port, maxPoolSize=100)
        self.db = self.client[self.mongo_db]
        self.col = self.db[self.mongo_collection]

    def insert(self, content):
        return self.col.insert_one(content).inserted_id

    def find_all(self):
        """
        返回是个可迭代的游标对象
        :return:
        """
        return self.col.find()

    def find_one(self, filter_dict):
        """
        用于查询单个文档
        :param filter_dict:
        :return:
        """
        return self.col.find_one(filter_dict)

    def filter_one(self,filter_dict, fields_dict):
        return self.col.find_one(filter_dict, fields_dict)

    def update(self, id_obj, up_content_dict):
        return self.col.update({"_id": id_obj}, {"$set": up_content_dict})

    def push(self, id_obj, array_key, array_value):
        return self.col.update({"_id": id_obj}, {"$push": {array_key: array_value}})


