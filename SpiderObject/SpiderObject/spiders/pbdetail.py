# -*- coding: utf-8 -*-
import scrapy
import json
import sqlite3
import datetime
from ..items import pbItem
from ..settings import FILES_STORE

class SimujijinSpider(scrapy.Spider):
    name = 'pbdetail'
    db_file_name = 'smhbase.db'
    allowed_domains = ['yhzqjj.com']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.pbdetailPipeline': 390}
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
        todayyyyyyy = today.strftime('%Y-%m-%d')
        # print(todayyyyyyy)
        # print(datetime.date.today().strftime('%Y-%m-%d'))
        file = open(file_path, 'r', encoding='utf-8')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(file.name)
        conn = sqlite3.connect(file.name)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('select trusteeid from TRUSTEES')
        for row in cur:
            print(str(row[0]))
            detail_url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtJjglr.do?methodCall=HeadOfficeBranch'
            data = {
                'count': '50',
                'pubdate': str(todayyyyyyy),
                'yhtrusteecode': str(row[0]),
            }
            yield scrapy.FormRequest(url=detail_url, headers=self.headers, formdata=data, callback=self.parse_detail)
        conn.close()

    def parse_detail(self, response):
        data = json.loads(response.text)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~获取数据啦啦啦啦啦啦啊~~~~~~~~~~~~~~~~~~~~~~~~~")
        details = data['responseResults']['data']
        # print(details)
        for detail in details:
            item = pbItem()
            item['fundsName'] = detail['FUNDSNAME']
            item['mngName'] = detail['MNGCNAME']
            item['registDate'] = detail['REGISTDATE']
            print(item['fundsName'])
            yield item




