# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import os
import time
import csv
from typing import TextIO

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from .settings import FILES_STORE
import zipfile


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
        path = '/qhjg/' + today.strftime('%Y%m%d') + '/' + today.strftime('%Y%m%d') + '_' + str(request).split("/")[-1][:-1]
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
        today = datetime.date.today()
        store_file = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d')
        if not os.path.exists(store_file):
            os.mkdir(store_file)
        csv_file = store_file + '/' + today.strftime('%Y%m%d') + '_50亿以上的私募证券基金公司.csv'
        self.fo = open(csv_file, 'a')
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
        today = datetime.date.today()
        store_file = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d')
        if not os.path.exists(store_file):
            os.mkdir(store_file)
        csv_file = store_file + '/' + today.strftime('%Y%m%d') + '_100亿以上的私募证券基金公司.csv'
        self.fo = open(csv_file, 'a')
        data = "{},{},{}\n".format('私募基金管理人名称', '登记时间', '登记编号')
        self.fo.write(data)

    def process_item(self, item, spider):
        data = "{},{},{}\n".format(item['MNGCNAME'], item['REGISTDATE'], item['MNGID'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.close()

class SimujijinPipeline(FilesPipeline):
    temp_path = ''
    def get_media_requests(self, item, info):
        url = item['file_url'][0]
        print('开始下载文件》》》》》》》》》》》')
        print(str(url))
        yield scrapy.Request(str(url), meta={'item': item})

    def file_path(self, request, response=None, info=None):
        # today = datetime.date.today()
        item = request.meta['item']
        path = item['fileName'][0]
        self.temp_path = path
        return path

    def item_completed(self, results, item, info):
        today = datetime.date.today()
        zip_path = FILES_STORE + '/' + self.temp_path
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        print(zip_path)
        db_file_path = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d')
        if not os.path.exists(db_file_path):
            os.mkdir(db_file_path)
        zip_file = zipfile.ZipFile(zip_path)
        print(zip_file)
        zip_list = zip_file.namelist()  # 得到压缩包里所有文件
        print(zip_list)
        # print('文件名啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊')
        for f in zip_list:
            file = zip_file.extract(f, db_file_path)  # 循环解压文件到指定目录
        zip_file.close()  # 关闭文件，必须有，释放内存

class detailPipeline(object):
    def open_spider(self, spider):
        today = datetime.date.today()
        store_file = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d') + '/' + today.strftime('%Y%m%d') + '_基金公司名称.csv'
        self.fo = open(store_file, 'a')
        data = "{},{}\n".format('基金名称', '基金管理人名称')
        self.fo.write(data)

    def process_item(self, item, spider):
        data = "{},{}\n".format(item['fundsName'], item['mngName'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.flush()
        self.fo.close()


class ZsxiazaiPipeline(FilesPipeline):
    downloadBaseUrl = 'http://xinpi.cs.com.cn/new/file/'

    def get_media_requests(self, item, info):
        for data in item['rows']:
            yield scrapy.Request(self.downloadBaseUrl + data['cell'][4], meta={'data': data})

    def file_path(self, request, response=None, info=None):
        data = request.meta['data']
        today = datetime.date.today()
        novel_name = "/zs/"+today.strftime('%Y%m%d')+ '/'+today.strftime('%Y%m%d')+'/'+data['cell'][3]+data['cell'][4][data['cell'][4].index('.'):]
        return '%s' % novel_name

    def item_completed(self, results, item, info):
        return item


class CnstockPipeline(object):

    def __init__(self):
        today = datetime.date.today()
        store_path = os.path.dirname(__file__) + '\\cnstock\\' + today.strftime('%Y%m%d') + '\\'
        store_file_csv = os.path.dirname(__file__) + '\\cnstock\\' + today.strftime('%Y%m%d') + '\\' + today.strftime(
            '%Y%m%d') + '_cnstock.csv'
        store_file_txt = os.path.dirname(__file__) + '\\cnstock\\' + today.strftime('%Y%m%d') + '\\' + today.strftime(
            '%Y%m%d') + '_cnstock.txt'
        file_dir_csv = os.path.split(store_file_csv)[0]

        print(file_dir_csv)

        if not os.path.exists(file_dir_csv):
            os.makedirs(file_dir_csv)

        self.file = open(store_file_csv, 'w')
        data = "{},{},{},{}\n".format('公告标题', '发布日期', '文章链接', '文章内容')
        self.file.write(data)

        self.file1 = open(store_file_txt, 'w')
        data_txt = "{},{}\n".format('公告标题', '文章内容')
        self.file1.write(data_txt)

    def process_item(self, item, spider):
        if len(item['announContent']) > 300:
            item['announContent'] = item['announContent'][0:300].rstrip() + '...'
        self.file.write(
            "{},{},{},{}\n".format(item['announTitle'], item['announDate'], item['announLink'], item['announContent']))
        self.file1.write(
            "{}\n{}\n".format(item['announTitle'], item['announContent']))

        return item



    def close_spider(self, spider):
        self.file.close()

class pbdetailPipeline(object):
    def open_spider(self, spider):
        today = datetime.date.today()
        store_file = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d') + '/' + today.strftime('%Y%m%d') + '_PB公司名称.csv'
        self.fo = open(store_file, 'a')
        data = "{},{},{}\n".format('私募基金名称', '备案时间', 'PB证券公司')
        self.fo.write(data)

    def process_item(self, item, spider):
        data = "{},{},{}\n".format(item['fundsName'], item['registDate'], item['mngName'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.close()