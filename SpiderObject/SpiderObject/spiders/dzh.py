import scrapy
import json
import re
from ..items import dzhNews

class StcnSpider(scrapy.Spider):
    name = 'dzh'
    allowed_domains = ['webrelease.gw.com.cn', 'detailpage.gw.com.cn']
    start_urls = ['https://webrelease.gw.com.cn/fxpd/api.php?service=getList&channel=%E5%88%B8%E5%95%86&page=1']
    custom_settings = {
        'ITEM_PIPELINES': {}
        # 'SpiderObject.pipelines.stcnPipeline': 320,
    }
    init_page=1

    def parse(self, response):
        print('>>>>>>>>>>>>>>>>>>>>>>>开始解析数据》》》》》》》》》》》')
        # print(response.text)
        dict_json = json.loads(response.text)
        data_s = dict_json['data']
        # 每页有多少条
        pageSize=len(data_s)
        print('一页有:'+str(len(data_s)))
        for i in range(0, pageSize-1):
            print(data_s[i]['Url'])

            item = dzhNews()
            item['newsTitle'] = data_s[i]['Title']
            newsUrl=data_s[i]['Url']
            # 获取到id
            newsId=re.findall(r'id=\S*?&', newsUrl)[0][3:-1]
            print(newsId)
            # 拼装新的请求获取文章具体内容
            urlContent='https://detailpage.gw.com.cn/index.php?service=getNewsContent&id='+newsId+'&version=9.13&token=NoToken'
            print(urlContent)
            item['newsLink'] = urlContent
            yield scrapy.Request(url=urlContent, meta={'item': item}, callback=self.parseNewsContent)
        # 继续滑动爬取下一页
        if self.init_page<=3:
            self.init_page=self.init_page+1
            urlNextPage='https://webrelease.gw.com.cn/fxpd/api.php?service=getList&channel=%E5%88%B8%E5%95%86&page='+str(self.init_page)
            yield scrapy.Request(url=urlNextPage, callback=self.parse)
        yield None

    def parseNewsContent(self, response):
        # 爬取每条公告的内容
        print('爬取每条公告的内容')
        item = response.meta['item']
        dict_json = json.loads(response.text)
        data_s = dict_json['Data']['Docs']
        newsCotent = data_s[0]['Content']
        # 去掉html的标签
        pattern = re.compile(r'<[^>]+>', re.S)
        newsCotents = pattern.sub('', newsCotent)
        print(newsCotents)
        item['newsContent'] = newsCotents
        yield item


def count_word(keyword, content):
    import re
    return len(re.findall(r'%s' % keyword, content))