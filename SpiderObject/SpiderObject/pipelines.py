# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import os

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