# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import os

from ..items import *
from ..settings import FILES_STORE


class ZsggSpider(scrapy.Spider):
    name = 'zsgg'
    today = datetime.date.today()#就是这种%Y-%m-%d格式os.getcwd()
    dat = today.strftime('%Y/%#m/%#d')
    dat0 = today.strftime('%Y-%m-%d')

    baseUrl='http://xinpi.cs.com.cn//new/search.ashx?t=b&st={st}&et={et}&c={c}&q=公告&m=&s=&p=1'
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.ZsxiazaiPipeline':360},
        'DEFAULT_REQUEST_HEADERS': {
            'x-requested-with': 'XMLHttpRequest',
            'referer': 'http://xinpi.cs.com.cn/',
        },
        'USER_AGENT' : {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Sa'}
    }

    def start_requests(self):

        map={
            '国泰君安证券股份有限公司': "601211", '招商证券股份有限公司': "600999", '国海证券股份有限公司': "000750",
            '方正证券股份有限公司': '601901', '光大证券股份有限公司': '601788','东方证券股份有限公司': '600958',
            '东海证券股份有限公司': '832970','广发证券股份有限公司':'000776','海通证券股份有限公司':'600837',
            '申万宏源证券有限公司':'000166','太平洋证券股份有限公司':'601099','浙商证券股份有限公司': '601878',
            '中国银河证券股份有限公司': '601881','中信证券股份有限公司': '600030',
        }
        for k in map.keys():
            yield scrapy.Request(self.baseUrl.format(c=map[k],st=self.today,et=self.today),callback=self.parse)

    def parse(self, response):
        page_url = 'http://xinpi.cs.com.cn/new/file/'

        item = ZsNoticeItem()
        item["rows"] = json.loads(response.text)['rows']

        for notice in json.loads(response.text)['rows']:
            item['name'] = notice['cell'][2]
            item['title'] = notice['cell'][3]
            item['file_urls'] = page_url+ notice['cell'][4]
            today = datetime.date.today()
            path = FILES_STORE + '\\zs\\' + today.strftime('%Y%m%d') + '\\'

            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + today.strftime('%Y%m%d') + '_zsgg.csv', 'a', encoding='utf-8-sig') as f:
                data0 = "{},{},{}\n".format(item['name'], item['title'], item['file_urls'])
                print(data0)
                f.write(data0)

        yield item