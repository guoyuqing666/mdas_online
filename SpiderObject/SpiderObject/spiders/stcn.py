import scrapy
import time
from ..items import stcnNews

class StcnSpider(scrapy.Spider):
    name = 'stcn'
    allowed_domains = ['company.stcn.com']
    start_urls = ['http://company.stcn.com/']
    custom_settings = {
        'ITEM_PIPELINES': {'SpiderObject.pipelines.stcnPipeline':320,}
        # 'SpiderObject.pipelines.stcnPipeline': 320,
    }

    def parse(self, response):

        #爬取文章标题，文章时间，文章内容链接
        ## 第一篇文章(默认只筛选今日)
        todayDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        firstNewsTitle = response.selector.xpath('//dd[@class="tit"]/a/text()').extract()
        firstNewsDate = response.selector.xpath('//dd[@class="sj"]/text()').extract()
        firstNewsLink = response.selector.xpath('//dd[@class="tit"]/a//@href').extract()

        item = stcnNews()
        item['newsTitle'] = firstNewsTitle[0]
        item['newsDate'] = firstNewsDate[0]
        item['newsLink'] = firstNewsLink[0]

        print(todayDate)
        print(firstNewsDate[0].strip())
        if(todayDate == firstNewsDate[0].strip()):
            next = item['newsLink']
            url = response.urljoin(next)
            print("aaaaaa", url)
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parseNewsContent)

        ## 后面的文章(默认只筛选今日)
        newsTitle = response.selector.xpath('//li/p/a/text()').extract()
        newsDate = response.selector.xpath('//li/p[@class="sj"]/text()').extract()
        newsLink = response.selector.xpath('//li/p/a//@href').extract()
        # print(newsTitle)
        # print(len(newsTitle))
        for i in range(0,len(newsTitle)):
            item = stcnNews()
            item['newsTitle'] = newsTitle[i]
            item['newsDate'] = newsDate[i]
            item['newsLink'] = newsLink[i]
            if (todayDate == newsDate[i].strip()):
                # 遍历今日公告获取内容
                next = item['newsLink']
                url = response.urljoin(next)
                print("aaaaaa",url)
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parseNewsContent)


        newsTitle_1 = newsTitle[1]
        newsDate_1 = newsDate[1]
        newsLink_1 = newsLink[1]
        print(newsTitle_1, newsDate_1, newsLink_1)
        print(firstNewsTitle, firstNewsDate, firstNewsLink)
        yield None

    def parseNewsContent(self, response):
        # 爬取每条公告的内容
        print('爬取每条公告的内容')
        NewsPaper = response.selector.xpath('//div[@class="txt_con"]/p/text()').extract()
        newsContent=''.join(NewsPaper)
        print(newsContent)
        item = response.meta['item']
        item['newsContent'] = newsContent
        # 对标题和内容进行关键词出现频次统计
        newsClientNo=0
        newsActionNo=0
        keywordsClient=['平安','车企','药品']
        keywordsAction=['IPO','融资','涨幅','增发']
        for keywordClient in keywordsClient:
            countTempClient=count_word(keywordClient,newsContent)
            newsClientNo=newsClientNo+countTempClient

        for keywordAction in keywordsAction:
            countTempAction=count_word(keywordAction,newsContent)
            newsActionNo=newsActionNo+countTempAction


        item['newsClientCapture'] = newsClientNo
        item['newsActionCapture'] = newsActionNo
        yield item

def count_word(keyword, content):
    import re
    return len(re.findall(r'%s' % keyword, content))

