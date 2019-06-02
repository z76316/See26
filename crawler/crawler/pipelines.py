# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import ArticleItem, PushItem

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            return self.handleArticle(item, spider)
        if isinstance(item, PushItem):
            return self.handlePush(item, spider)

    def handleArticle(self, item, spider):
        return item

    def handlePush(self, item, spider):
        return item

        # if 'title' in item.keys():
        #     item['push'] = int(item['push'])
        #     item['title'] = str(item['title'])
        #     item['href'] = str(item['href'])
        #     item['date'] = str(item['date'])
        #     item['author'] = str(item['author'])
        
        # return item
