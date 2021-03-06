# -*- coding: utf-8 -*-
import scrapy
import datetime

from ..items import ExamplesItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.czce.com.cn/cn/jysj/jscs/H770303index_1.htm']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.MyfilesPipeline': 300,}
    }

    def parse(self, response):
        today = datetime.date.today()
        # oneday = datetime.timedelta(days=1)
        # yesterday = today - oneday
        # download_url = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/2019/' + today.strftime('%Y%m%d') + '/FutureDataDelsettle.xls'  # 解析得到要下载的url
        urls = ['FutureDataDelsettle.xls', 'FutureDataClearParams.xls']
        for url in urls:
            download_url = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/2019/20191210/' + url  # 解析得到要下载的url
            item = ExamplesItem()
            item['file_urls'] = [download_url]
            yield item