# -*- coding: utf-8 -*-
import scrapy
from ..items import CnstockItem


'''
爬取中国证券网证券公司公告
author: rjq
'''
class CnstockSpider(scrapy.Spider):
    name = 'cnstock'
    allowed_domains = ['ggjd.cnstock.com']
    start_urls = ['http://ggjd.cnstock.com/company/scp_ggjd/tjd_ggkx']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.CnstockPipeline': 370}
    }

    def parse(self, response):
        
        '''
        STEP 1.获取并解析公告内容
        '''
        # 获取当日日期                
#        today=datetime.date.today() 
#        oneday=datetime.timedelta(days=1) 
#        yesterday=today-oneday 
#        yesterDate = time.strftime('%m-%d', yesterday)
#        print(yesterDate)
              
        # 获取公告标题、日期、链接、内容
        announTitle = response.selector.xpath('//li/h2/a/@title').extract()
        announDate = response.selector.xpath('//li/p[@class="info"]/span[@class="time"]/text()').extract()
        announLink = response.selector.xpath('//li/h2/a/@href').extract()
        announContent = response.selector.xpath('//li/p[@class="des"]/text()').extract()

#        sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
#        print(type(announTitle.text.encode(announTitle.encoding))
#        print(announTitle.encode(announTitle.encoding).decode('utf-8'),announDate,announLink,announContent)
#        print(announTitle)
#        print(len(announTitle))
#        f = open('news.txt', mode='a+')
        for i in range(0,len(announTitle)):
            item = CnstockItem()
#            announTitle[i] = announTitle[i].encode("latin1")
            item['announTitle'] = announTitle[i]
            announDate[i] = announDate[i][0:6]
            item['announDate'] = announDate[i]
            item['announLink'] = announLink[i]
            item['announContent'] = announContent[i]
            
#            f.write(announTitle[i]+'\n')
#        f.close()

            # 判断是否为今天
#            if (todayDate == announDate[i].strip()):                
            yield item
           
        
        '''
         STEP 2.翻页爬取
        
        '''

'''
class CnstockSpider(scrapy.Spider):
    name = 'cnstock'
    allowed_domains = ['cnstock.com']
    start_urls = ['http://cnstock.com/']

    def parse(self, response):        
        #print(response,type(response)) # 对象
        #print(response.text)
        
#        j_waterfall_list = response.xpath('//*[@id="j_waterfall_list"]')
        
        # 去子孙中找div并且id=content-list
        f = open('news.log', mode='a+', encoding='UTF-8')
        j_waterfall_list = response.xpath('//*[@id="j_waterfall_list"]/li[@class="newslist"]')
#        print(j_waterfall_list.text)
        
        for newslist in j_waterfall_list:
#            text = newslist.xpath('.//a/text()').extract_first()#取第一个a标签的文本
            title = newslist.xpath('.//a/@title').extract_first()
            href = newslist.xpath('.//a/@href').extract_first()#取第一个标签的href属性
#            sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='UTF-8')
            print(title, href)#strip()去除空格
            f.write(href+'\n')
        f.close()
'''