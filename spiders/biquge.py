import scrapy
from BiqugeProject.items import ChapterItem,NovelInfoItem


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    # allowed_domains = ['www.xbiquge.la']
    start_urls = ['https://www.xbiquge.la/93/93737/']

    def parse(self, response):
        # 爬取小说名字和作者
        name = response.xpath('//div[@id="info"]/h1/text()').extract_first()
        author = response.xpath('//div[@id="info"]/p[1]/text()').extract_first()
        yield NovelInfoItem(name=name,author=author)

        # 爬取章节名称和章节地址
        a_list = response.xpath('//div[@id="list"]//a')

        # 章节序号
        orderNum = 1
        for a in a_list:
            chapter_name = a.xpath('./text()').extract_first()
            chapter_url = 'https://www.xbiquge.la/' + a.xpath('./@href').extract_first()
            yield scrapy.Request(url=chapter_url,callback=self.parse_text,meta={'chapter_name':chapter_name,'orderNum':orderNum})
            orderNum += 1

    # 爬取一个章节页面
    def parse_text(self,response):
        chapter_name = response.meta['chapter_name']
        chapter_order = response.meta['orderNum']

        text = ''.join(response.xpath('//div[@id="content"]/text()').extract())

        yield ChapterItem(text=text,chapter_name=chapter_name,chapter_order=chapter_order)
