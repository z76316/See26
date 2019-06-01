# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider

class NbaSpider(scrapy.Spider):
    count_page = 1
    name = 'nba'
    allowed_domains = ['www.ptt.cc/']
    start_urls = ['https://www.ptt.cc/bbs/NBA/index.html']

    def parse(self, response):
        # self.logger.info('A response from %s just arrived!', response.url)
        for q in response.css('div.r-ent'):
            item = {
                'push':q.css('div.nrec > span.hl ::text').get(),
                'title':q.css('div.title > a::text').get(),
                'href':q.css('div.title > a::attr(href)').get(),
                'date':q.css('div.meta > div.date ::text').get(),
                'author':q.css('div.meta > div.author ::text').get()
            }
            yield(item)

        next_page_url = response.css('div.action-bar > div.btn-group > a.btn::attr(href)')[3].get()

        if next_page_url and self.count_page < 3:
            self.count_page += 1
            next_page = response.urljoin(next_page_url)
        else:
            raise CloseSpider('Close it')
        
        yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)