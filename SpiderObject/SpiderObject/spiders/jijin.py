# -*- coding: utf-8 -*-
import scrapy
import json
import sqlite3
import datetime
import time
from ..items import detailItem
from ..settings import FILES_STORE

class SimujijinSpider(scrapy.Spider):
    name = 'detail'
    db_file_name = 'smhbase.db'
    allowed_domains = ['yhzqjj.com']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.detailPipeline': 380, }
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
        today = datetime.date.today()
        file_path = FILES_STORE + '/' + '私募汇_' + today.strftime('%Y%m%d') + '/' + self.db_file_name
        file = open(file_path, 'r', encoding='utf-8')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(file.name)
        conn = sqlite3.connect(file.name)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('select yhcode from PRIVATE_FUNDS')
        for row in cur:
            time.sleep(5)
            # print(str(row[0]))
            detail_url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtFundDetails.do?methodCall=getFundDetails'
            data = {
                'yhcode': str(row[0])
            }
            yield scrapy.FormRequest(url=detail_url, headers=self.headers, formdata=data, callback=self.parse_detail)
        conn.close()

    def parse_detail(self, response):
        data = json.loads(response.text)
        # print(data)
        details = data['responseResults']['data']
        # print(details)
        item = detailItem()
        for detail in details:
            item['fundsName'] = detail['FUNDSNAME']
            item['mngName'] = detail['MNGCNAME']
            print(item['fundsName'])
        yield item




