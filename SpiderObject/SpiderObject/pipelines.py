# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import os
import csv

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline

class TextPipeline(object):
    def __init__(self):
        self.limit= 50
    def process_item(self, item, spider):
        if item['text']:
            if len(item['text'])>self.limit:
                item['text']=item['text'][0:self.limit].rstrip()+'...'
            return item
        else:
            return DropItem('Missing Text')

class MyfilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for url in item["file_urls"]:
            yield scrapy.Request(url)

    def file_path(self, request, response=None, info=None):
        today = datetime.date.today()
        path = '/qhjg/' + today.strftime('%Y%m%d') + '/' + today.strftime('%Y%m%d') + '_FutureDataDelsettle.xls'
        return path

# class stcnPipeline(object):
#     def process_item(self, item, spider):
#         return item

class stcnPipeline(object):

    def __init__(self):
        today = datetime.date.today()
        store_path = os.path.dirname(__file__) + '\\stcn\\' + today.strftime('%Y%m%d') + '\\'

        store_file =os.path.dirname(__file__)+'\\stcn\\'+today.strftime('%Y%m%d') + '\\'+ today.strftime('%Y%m%d') + '_stcn.csv'
        file_dir=os.path.split(store_file)[0]
        print(file_dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.file=open(store_file,'w')
        data = "{},{},{},{},{},{}\n".format('公告标题', '发布日期', '文章链接', '文章内容','关注同业客户出现频次','关注预测信息出现频次')
        self.file.write(data)

    def process_item(self,item,spider):
        if len(item['newsContent']) > 300:
            item['newsContent'] = item['newsContent'][0:300].rstrip() + '...'
        self.file.write("{},{},{},{},{},{}\n".format(item['newsTitle'], item['newsDate'], item['newsLink'], item['newsContent'],item['newsClientCapture'],item['newsActionCapture']))
        return item

    def close_spider(self,spider):
        self.file.close()


class SimuPipeline(object):
    def open_spider(self, spider):
        self.fo = open('50亿以上的私募证券基金公司.csv', 'a')
        data = "{},{},{}\n".format('私募基金管理人名称', '登记时间', '登记编号')
        self.fo.write(data)

    def process_item(self, item, spider):
        data = "{},{},{}\n".format(item['MNGCNAME'], item['REGISTDATE'], item['MNGID'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.close()

class Simu100Pipeline(object):
    def open_spider(self, spider):
        self.fo = open('100亿以上的私募证券基金公司.csv', 'a')
        data = "{},{},{}\n".format('私募基金管理人名称', '登记时间', '登记编号')
        self.fo.write(data)

    def process_item(self, item, spider):
        data = "{},{},{}\n".format(item['MNGCNAME'], item['REGISTDATE'], item['MNGID'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.close()

class SimujijinPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        url = item['file_url'][0]
        print('开始下载文件》》》》》》》》》》》')
        print(str(url))
        yield scrapy.Request(str(url), meta={'item': item})
    def file_path(self, request, response=None, info=None):
        """
        重命名模块
        :param request:
        :param response:
        :param info:
        :return:path
        """
        item = request.meta['item']
        path = item['fileName']
            # os.path.join('D:\pythonSpider\scrapy\Simu100', ''.join([file_name]))
        print(path)
        return path