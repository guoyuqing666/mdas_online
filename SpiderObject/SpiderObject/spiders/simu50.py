import scrapy
from ..items import SimuItem
import json
import time

class SiMu(scrapy.Spider):
    name = 'simu50'
    allowed_domains = ['yhzqjj.com']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.SimuPipeline':330,}
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
        #————————50亿以上管理规模——————————————
        url = 'https://www.yhzqjj.com/yhzqjjApp/smt/report/smtMng.do?methodCall=getMngByFundType'
        print('开始爬取数据》》》》》》》》》》》》')
        for page in range(1, 4):
            current_page = page
            data = {
                'count': '30',
                'fundtype': '1',
                'page': str(current_page),
                'scalecode': '5'
            }
            time.sleep(5)
            yield scrapy.FormRequest(url=url, headers=self.headers, formdata=data, callback=self.parse)

    def parse(self, response):
        print('>>>>>>>>>>>>>>>>>>>>>>>开始解析数据》》》》》》》》》》》')
        print(response.text)
        dict_json = json.loads(response.text)
        data_s = dict_json['responseResults']['data']
        for data in data_s:
            item = SimuItem()
            item['MNGCNAME'] = data['MNGCNAME']
            item['REGISTDATE'] = data['REGISTDATE']
            item['MNGID'] = data['MNGID']
            yield item





