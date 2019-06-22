# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from ..items import ArticleItem, PushItem

class GossipingSpider(scrapy.Spider):
    count_page = 1
    name = 'gossiping'
    allowed_domains = ['www.ptt.cc/']
    
    # start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']

    # [臉書]
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/search?q=%5B%E8%87%89%E6%9B%B8%5D']

    def parse(self, response):
        yield scrapy.Request(self.start_urls[0], cookies={'over18': '1'}, callback = self.after_over18, dont_filter = True)
        

    def after_over18(self, response):
        
        if response.css('div.r-ent'):
            
            article = ArticleItem()
            board = response.css('#topbar > a.board::text').get()

            for q in response.css('div.r-ent'):
                
                # skip the deleted article
                if str(q.css('div.meta > div.author ::text').get()) == '-':
                    continue

                article_url = q.css('div.title > a::attr(href)').get()
                article_id = article_url[article_url.find('M.')+2 : article_url.find('A.')-1]

                article['id'] = article_id
                article['push'] = q.css('div.nrec > span.hl ::text').get()
                article['title'] = q.css('div.title > a::text').get()
                article['href'] = 'www.ptt.cc' + str(q.css('div.title > a::attr(href)').get())
                article['author'] = q.css('div.meta > div.author ::text').get()
                article['board'] = board
                article['date'] = q.css('div.meta > div.date ::text').get().strip()
                

                yield(article)
                
                test_url = response.urljoin(q.css('div.title > a::attr(href)').get())
                yield scrapy.Request(test_url, callback = self.after_over18, dont_filter = True)

            next_page_url = response.css('div.action-bar > div.btn-group > a.btn::attr(href)')[3].get()

            if next_page_url and self.count_page < 3:
                self.count_page += 1
                next_page = response.urljoin(next_page_url)
                yield scrapy.Request(next_page, callback = self.after_over18, dont_filter = True)
            else:
                raise CloseSpider('Close it')
            
        
        if response.css('div.push'):
            
            push = PushItem()
            article_url = response.css('#main-content > span.f2 > a::text').get()
            article_id = article_url[article_url.find('M.')+2 : article_url.find('A.')-1]
            year = response.css('#main-content > div:nth-child(4) > span.article-meta-value ::text').get().strip().split(' ')[-1]
            
            for q in response.css('div.push'):

                push['article_id'] = article_id
                push['push'] = q.css('div.push > span.push-tag ::text').get().strip()
                push['user'] = q.css('div.push > span.push-userid ::text').get().strip()
                push['content'] = q.css('div.push > span.push-content ::text').get().strip(': ')
                ip_datetime = q.css('div.push > span.push-ipdatetime ::text').get().strip().split(' ')
                push['ip'] = ip_datetime[0]
                push['datetime'] = year + '/' + ip_datetime[1] + ' ' + ip_datetime[2]

                yield(push)