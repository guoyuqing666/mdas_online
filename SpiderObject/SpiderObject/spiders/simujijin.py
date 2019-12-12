# -*- coding: utf-8 -*-
import scrapy
import zipfile
import os
import zipfile
# import time
import json
import urllib
from ..items import jiJinItem


class SimujijinSpider(scrapy.Spider):
    name = 'simujijin'
    allowed_domains = ['yhzqjj.com']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.SimujijinPipeline': 350, }
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
        # 私募基金公司连接
        url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtJjglr.do?methodCall=getNewestFileV1'
        data = {
            'bothKnowStr': 'B68B99858D0523DD202CE9B9FCEDC870'
        }
        yield scrapy.FormRequest(url=url, headers=self.headers, formdata=data, callback=self.parse)

    def parse(self, response):
        print(response.text)
        item = jiJinItem()
        dict_json = json.loads(response.text)
        fileName = dict_json['responseResults']['fileName']
        url = 'https://www.yhzqjj.com/yhzqjjApp/yhwz/report/android/smhzip/' + fileName
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<' + url + '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        item['fileName'] = fileName
        item['file_url'] = [url]
        return item
    # def parse_zip(self, response):
    #     print(response.body)
        # # os.chdir('D:\pythonSpider\scrapy\Simu100')
        # dir = 'D:\pythonSpider\scrapy\Simu100'
        # work_path = os.path.join(dir, data)
        # urllib.request.urlretrieve(item, work_path)
        # extracting = zipfile.ZipFile(data)
        # extracting.extractall('D:\pythonSpider\scrapy\Simu100')
        # extracting.close()
        # with zipfile.ZipFile(data) as f:
        #     data = tf.compat.as_str(f.read(f.namelist()[0])).split()
        #     print(data)
        # return data

