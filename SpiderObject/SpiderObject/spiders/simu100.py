# -*- coding: utf-8 -*-
import scrapy
import time
import json
from ..items import SimuItem


class Simu100Spider(scrapy.Spider):
    name = 'simu100'
    allowed_domains = ['yhzqjj.com']
    current_page = 1
    custom_settings = {
        'ITEM_PIPELINES': { 'SpiderObject.pipelines.Simu100Pipeline':340,}
    }
    headers = {
        'Host': 'www.yhzqjj.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=t7zZxnTZDh7U4-qMF9tpLwyEYmNt3eAQKBougD4ClifbAYuDWkBP!1533519278',
        'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9n',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Connection': 'keep-alive',
        'User_Agent': 'SiMuHui/20180207 (iPhone; iOS 13.2; Scale/2.00)'
    }

    def start_requests(self):
        # 100亿以上私募基金公司连接
        url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtMng.do?methodCall=getMngByFundType'
        print('开始爬取数据第' + str(self.current_page) + '页的数据》》》》》》》》》》》》》》》》》》')
        data = {
            'count': '30',
            'fundtype': '1',
            'page': str(self.current_page),
            'scalecode': '4'
        }
        yield scrapy.FormRequest(url=url, headers=self.headers, formdata=data, callback=self.parse)

    def parse(self, response):
        print('>>>>>>>>>>>>>>>>>>>>>>>开始解析数据》》》》》》》》》》》')
        # print(response.text)
        dict_json = json.loads(response.text)
        data_s = dict_json['responseResults']['data']
        for data in data_s:
            item = SimuItem()
            item['MNGCNAME'] = data['MNGCNAME']
            item['REGISTDATE'] = data['REGISTDATE']
            item['MNGID'] = data['MNGID']
            yield item
        if data_s:
                time.sleep(5)
                url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtMng.do?methodCall=getMngByFundType'
                self.current_page += 1
                data = {
                    'count': '30',
                    'fundtype': '1',
                    'page': str(self.current_page),
                    'scalecode': '4'
                }
                print('开始爬取数据第' + str(self.current_page) + '页的数据》》》》》》》》》》》》》》》》》》')
                yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)
        else:
            print("数据爬取完毕！")
