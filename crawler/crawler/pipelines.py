# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        item['push'] = int(item['push'])
        item['title'] = str(item['title'])
        item['href'] = str(item['href'])
        item['date'] = str(item['date'])
        item['author'] = str(item['author'])
        return item
