# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 小说信息
class NovelInfoItem(scrapy.Item):

    name = scrapy.Field()
    author = scrapy.Field()

class ChapterItem(scrapy.Item):

    # 序列号 -- 排序依据
    chapter_order = scrapy.Field()
    chapter_name = scrapy.Field()
    text = scrapy.Field()


