import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from BiqugeProject.items import NovelInfoItem,ChapterItem


class Biquge1Spider(CrawlSpider):
    name = 'biquge_1'
    # allowed_domains = ['www.xbiquge.la']
    start_urls = ['https://www.xbiquge.la/91/91203/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//div[@id="list"]//dd[1]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=r'//div[@class="bottem1"]/a[4]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        chapter_name = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        text = '\n'.join(response.xpath('//div[@id="content"]/text()').extract())
        book = ChapterItem(text=text,chapter_name=chapter_name)
        yield book
