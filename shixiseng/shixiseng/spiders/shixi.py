# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from shixiseng.items import ShixisengItem
import re
from redis import Redis
identity='slave'

from scrapy_redis.spiders import RedisSpider


class ShixiSpider(RedisSpider):
    if identity=='master':
        r = Redis()
        for x in range(1,77):
            url = 'https://www.shixiseng.com/interns?k=%E4%BA%A7%E5%93%81%E8%BF%90%E8%90%A5&p='+str(x)
            r.lpush('shixisheng:start_urls', url)
        exit(0)
    name = 'slave_1'
    # 爬虫从连接的redis的该集合中读取url进行爬取，如果该集合为空，那么爬虫会一直等待..
    # 手动添加方法：lpush shixisheng:start_urls url
    redis_key = 'shixisheng:start_urls'

    def parse(self, response):
        response = Selector(response)
        url_list = response.xpath("/html/body/div[1]/div[3]/div[2]/div/div[1]/ul//li")
        for x in url_list:
            url = 'https://www.shixiseng.com' + x.xpath('div[1]/div[1]/a/@href').extract()[0]
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        try:
            temp = re.findall(u'job_money cutom_font">(.*)</span>', response.body)[0].split('</span>')[0][:-5]
            l = temp.split('-')
            left = l[0].split('&#x')[1:]
            right = l[1].split('&#x')[1:]
            t = 6
            days = 6
        except:
            pass
        response = Selector(response)
        item = ShixisengItem()
        try:
            item['name'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/text()').extract()[0]
        except:
            item['name'] = u'暂无'
        try:
            item['salary'] = '10000/天'
        except:
            item['salary'] = u'暂无'
        try:
            item['location'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/span[2]/text()').extract()[0]
        except:
            item['location'] = u'暂无'
        try:
            item['xueli'] = response.xpath('/html/body/div[1]/div[2]/div[1]/div[3]/span[3]/text()').extract()[0]
        except:
            item['xueli'] = u'暂无'
        try:
            item['work'] = str(days) + "天/周"
        except:
            item['work'] = u'暂无'
        try:
            item['time'] = "实习"+str(t)+"个月"
        except:
            item['time'] = u'暂无'
        try:
            item['category'] = response.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[4]/span[3]/text()').extract()[0]
        except:
            item['category'] = u'暂无'
        try:
            item['required'] = response.xpath('string(/html/body/div[1]/div[2]/div[2]/div[1]/div[1])').extract()[0]
        except:
            item['required'] = u'暂无'
        yield item
