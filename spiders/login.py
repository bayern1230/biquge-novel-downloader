import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la/']

    def parse(self, response):
        infos = response.xpath('//div/@class').extract()


        print('++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++')
        print(infos)
        print('++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++')
