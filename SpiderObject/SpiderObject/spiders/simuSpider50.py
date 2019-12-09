import scrapy
from SpiderObject.items import SimuItem
import json
import time

class SiMu(scrapy.Spider):
    name = 'simu'
    allowed_domains = ['yhzqjj.com']

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
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

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





