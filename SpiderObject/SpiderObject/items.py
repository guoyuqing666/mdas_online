# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text =scrapy.Field()
    author=scrapy.Field()
    tags = scrapy.Field()

class ExamplesItem(scrapy.Item):
    file_urls=scrapy.Field()
    files=scrapy.Field()

class SimuItem(scrapy.Item):
    MNGCNAME = scrapy.Field()
    REGISTDATE = scrapy.Field()
    MNGID = scrapy.Field()

class stcnNews(scrapy.Item):
    newsTitle =scrapy.Field()
    newsDate =scrapy.Field()
    newsLink =scrapy.Field()
    newsContent =scrapy.Field()
    newsClientCapture =scrapy.Field()
    newsActionCapture=scrapy.Field()

class SimuItem(scrapy.Item):
    MNGCNAME = scrapy.Field()
    REGISTDATE = scrapy.Field()
    MNGID = scrapy.Field()


class jiJinItem(scrapy.Item):
    file_url = scrapy.Field()
    file = scrapy.Field()
    fileName = scrapy.Field()

class dzhNews(scrapy.Item):
    newsTitle =scrapy.Field()
    newsLink =scrapy.Field()
    newsContent =scrapy.Field()

class ZsNoticeItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    rows=scrapy.Field()

class CnstockItem(scrapy.Item):
    announTitle =scrapy.Field()
    announDate =scrapy.Field()
    announLink =scrapy.Field()
    announContent =scrapy.Field()

class detailItem(scrapy.Item):
    fundsName = scrapy.Field()
    mngName = scrapy.Field()


class pbItem(scrapy.Item):
    fundsName = scrapy.Field()
    mngName = scrapy.Field()
    registDate = scrapy.Field()




