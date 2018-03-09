# -*- coding: utf-8 -*-
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
from pymongo import MongoClient
from shixiseng.spiders.shixi import identity

# 存到master的MongoDB
class MongoDBPipeline(object):
    def __init__(self):
        if identity=='master':
            self.client = MongoClient('127.0.0.1', 27017)
        else:
            self.client = MongoClient('39.106.155.194', 27017)
        self.shixisheng = self.client['test']['shixisheng']

    def process_item(self, item, spider):
        self.insert_to_mongodb(item)
        return item   # 返回给终端

    def insert_to_mongodb(self, item):
        self.shixisheng.insert_one({"name":item['name'], "salary":item['salary'], "location":item['location'], "xueli":item['xueli'],
                    "work":item['work'], "time":item['time'], "category":item['category'], "required":item['required']})
        # self.shixisheng.insert_one(item)

# 存到slave的Mysql
class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db='test',
                                            user='root',
                                            passwd='123456',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        try:
            tx.execute('insert into shiziseng values(%s,%s,%s,%s,%s,%s,%s,%s)',(item['name'],item['salary'],item['location'],item['xueli'],
                                                                                item['work'],item['time'],item['category'],item['required']))
            print u"写入成功"
        except Exception,e:
            print e
            print u"写入失败"

