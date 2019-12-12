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