# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import ArticleItem, PushItem
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, ForeignKey
from datetime import date, datetime

class CrawlerPipeline(object):
    def __init__(self):
        self.engine = create_engine('sqlite:///ptt_nba.db', echo = False)
        self.meta = MetaData()
        self.conn = self.engine.connect()
        self.articles = Table(
            'articles', self.meta,
            Column('id', Integer, primary_key = True),
            Column('push', String),
            Column('title', String),
            Column('href', String),
            Column('author', String),
            Column('date', Date)
        )
        self.pushs = Table(
            'pushs', self.meta,
            Column('id', Integer, primary_key = True, autoincrement = True),
            Column('article_id', Integer, ForeignKey('articles.id')),
            Column('push', String),
            Column('user', String),
            Column('content', String),
            Column('datetime', DateTime)
        )


    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            return self.handleArticle(item, spider)
        if isinstance(item, PushItem):
            return self.handlePush(item, spider)

    def handleArticle(self, article, spider):
        
        article['id'] = int(article['id'])
        article['push'] = str(article['push'])
        article['title'] = str(article['title'])
        article['href'] = str(article['href'])
        article['author'] = str(article['author'])
        date1 = article['date'].split('/')
        month = int(date1[0])
        day = int(date1[1])
        article['date'] = date(2019, month, day)

        ins = self.articles.insert().values(article)
        result = self.conn.execute(ins)

        return article

    def handlePush(self, push, spider):

        push['push'] = str(push['push'])
        push['user'] = str(push['user'])
        push['content'] = str(push['content'])
        push['article_id'] = int(push['article_id'])
        date1 = push['datetime'].split('/')
        month = int(date1[0])
        date2 = date1[1].split(' ')
        day = int(date2[0])
        date3 = date2[1].split(':')
        hour = int(date3[0])
        minute = int(date3[1])
        push['datetime'] = datetime(2019, month, day, hour, minute)

        ins = self.pushs.insert().values(push)
        result = self.conn.execute(ins)

        return push

        # if 'title' in item.keys():
        #     item['push'] = int(item['push'])
        #     item['title'] = str(item['title'])
        #     item['href'] = str(item['href'])
        #     item['date'] = str(item['date'])
        #     item['author'] = str(item['author'])
        
        # return item
