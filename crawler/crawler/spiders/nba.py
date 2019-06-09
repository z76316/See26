# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from ..items import ArticleItem, PushItem

class NbaSpider(scrapy.Spider):
    count_page = 1
    name = 'nba'
    allowed_domains = ['www.ptt.cc/']
    start_urls = ['https://www.ptt.cc/bbs/NBA/index.html']
    # start_urls = ['https://www.ptt.cc/bbs/NBA/M.1559464767.A.257.html']

    def parse(self, response):
        
        if response.css('div.r-ent'):
            
            article = ArticleItem()
            
            for q in response.css('div.r-ent'):
                
                # skip the deleted article
                if str(q.css('div.meta > div.author ::text').get()) == '-':
                    continue
                
                # items = {
                #     'push':q.css('div.nrec > span.hl ::text').get(),
                #     'title':q.css('div.title > a::text').get(),
                #     'href':q.css('div.title > a::attr(href)').get(),
                #     'date':q.css('div.meta > div.date ::text').get(),
                #     'author':q.css('div.meta > div.author ::text').get()
                # }

                article_url = q.css('div.title > a::attr(href)').get()
                article_id = article_url[article_url.find('M.')+2 : article_url.find('A.')-1]

                article['id'] = article_id
                article['push'] = q.css('div.nrec > span.hl ::text').get()
                article['title'] = q.css('div.title > a::text').get()
                article['href'] = 'www.ptt.cc' + str(q.css('div.title > a::attr(href)').get())
                article['date'] = q.css('div.meta > div.date ::text').get().strip()
                article['author'] = q.css('div.meta > div.author ::text').get()

                yield(article)
                
                test_url = response.urljoin(q.css('div.title > a::attr(href)').get())
                yield scrapy.Request(test_url, callback = self.parse, dont_filter = True)

            next_page_url = response.css('div.action-bar > div.btn-group > a.btn::attr(href)')[3].get()

            if next_page_url and self.count_page < 3:
                self.count_page += 1
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback = self.parse, dont_filter = True)
            else:
                raise CloseSpider('Close it')
            
        
        if response.css('div.push'):
            
            push = PushItem()
            article_url = response.css('#main-content > span.f2 > a::text').get()
            article_id = article_url[article_url.find('M.')+2 : article_url.find('A.')-1]
            
            for q in response.css('div.push'):
                # push = {
                #     'push':q.css('div.push > span.push-tag ::text').get(),
                #     'user':q.css('div.push > span.push-userid ::text').get(),
                #     'content':q.css('div.push > span.push-content ::text').get(),
                #     'datetime':q.css('div.push > span.push-ipdatetime ::text').get(),
                #     'article_id':article_id
                # }

                push['push'] = q.css('div.push > span.push-tag ::text').get().strip()
                push['user'] = q.css('div.push > span.push-userid ::text').get().strip()
                push['content'] = q.css('div.push > span.push-content ::text').get().strip(': ')
                push['datetime'] = q.css('div.push > span.push-ipdatetime ::text').get().strip()
                push['article_id'] = article_id

                yield(push)

            # raise CloseSpider('Close it')