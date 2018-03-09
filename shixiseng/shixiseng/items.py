# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShixisengItem(scrapy.Item):
    name = scrapy.Field()       # 职位名
    salary = scrapy.Field()     # 待遇
    location = scrapy.Field()   # 地点
    xueli = scrapy.Field()      # 学历要求
    work = scrapy.Field()       # 工作时间
    time = scrapy.Field()       # 实习时长
    category = scrapy.Field()   # 工作类别
    required = scrapy.Field()   # 职位要求
