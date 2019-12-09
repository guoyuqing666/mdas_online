# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

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