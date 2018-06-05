# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.loader import ItemLoader
from quotes_spider.items import QuotesSpiderItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    #allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self,response):
        token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        return FormRequest.from_response(response,
                                         formdata={'csrf_token': token,
                                                   'password': 'foo',
                                                   'username':'foo'},
                                         callback=self.scrape_homepage)

    def scrape_homepage(self, response):
        open_in_browser(response)
        l = ItemLoader(item= QuotesSpiderItem(),response=response)
        h1_tag = response.xpath('//h1/a/text()').extract()
        tags = response.xpath('//*[@class = "tag-item"]/a/text()').extract()
        
        l.add_value('h1_tag',h1_tag)
        l.add_value('tags',tags)

        return l.load_item()
