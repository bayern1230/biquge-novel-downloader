# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ChapterItem,NovelInfoItem
import sqlite3
import datetime
import json
import re

class txtPipeline:
    '''写入TXT文件'''
    def __init__(self):
        super(txtPipeline, self).__init__()
        self.name = ''
        self.author = ''

    def open_spider(self,spider):
        self.chapter_list = []

    def process_item(self, item, spider):

        if type(item) == NovelInfoItem:
            # 写入小说基本信息
            self.name = item['name']
            self.author = item['author']
        else:
            # 将内容添加进列表
            self.chapter_list.append(item)

        return item

    def close_spider(self,spider):
        # 如果没有采集到数据，则退出函数
        if not self.name:
            print('----------------')
            print("没有爬取名字或作者")
            print('----------------')
            return

        # 对列表进行排序
        self.chapter_list.sort(key=lambda i:i['chapter_order'])

        with open('{} - {}.txt'.format(self.name,self.author),'w',encoding='utf-8') as f:
            # 写入小说基本信息
            f.write("{} - 作者：{}".format(self.name,self.author))
            f.write('\n\n\n')

            # 写入小说章节内容
            for i in self.chapter_list:
                # 当文章标题不为数字开头时，直接写入标题
                if not re.match(r'^\d+',i['chapter_name']):
                    f.write(i['chapter_name'])
                # 当文章标题为数字开头时，加上汉字标题
                else:
                    f.write('第%s章'%i['chapter_order']+'  '+i['chapter_name'])
                f.write('\n\n\n')
                f.write(i['text'])
                f.write('\n\n\n')

class jsonPipeline:
    '''写入json文件'''
    def open_spider(self,spider):
        self.fp = open('笔趣阁JSON文件.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        d = dict(item)
        self.fp.write(json.dumps(d,ensure_ascii=False))

    def close_spider(self,spider):
        self.fp.close()

class sqlitePipeline:
    '''写入数据库'''
    def open_spider(self,spider):
        self.conn = sqlite3.connect('text.db')
        self.cursor = self.conn.cursor()

        # 创建表
        self.cursor.execute('''Create table if not exists Chapters(
        ChapterName         text,
        ChapterText         text,
        Time                text
        )''')
        self.conn.commit()

    def process_item(self,item,spider):

        # 插入数据
        self.cursor.execute('''Insert Into Chapters (ChapterName,ChapterText,Time)
                values ('{}','{}','{}')'''.format(item['chapter_name'], item['text'], str(datetime.datetime.now())))
        self.conn.commit()

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()