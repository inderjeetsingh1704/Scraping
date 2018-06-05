# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy.http import FormRequest

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
        h1_tag = response.xpath('//h1/a/text()').extract()
        tags = response.xpath('//*[@class = "tag-item"]/a/text()').extract()
        print(h1_tag)
        print(tags)
