# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    push = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    author = scrapy.Field()
    board = scrapy.Field()
    ip = scrapy.Field()
    date = scrapy.Field()

class PushItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_id = scrapy.Field()
    push = scrapy.Field()
    user = scrapy.Field()
    content = scrapy.Field()
    ip = scrapy.Field()
    datetime = scrapy.Field()
    