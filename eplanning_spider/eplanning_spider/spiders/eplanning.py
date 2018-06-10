# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if "#" == url:
                pass
            else:
                yield Request(url,callback=self.parse_application)

    def parse_application(self,response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(response.urljoin(app_url),callback=self.parse_form)

    def parse_form(self,response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '42'},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)
    def parse_pages(self, response):
        application_url = response.xpath('//td/a/@href').extract()
        for url in application_url:
            abs_url = response.urljoin(url)
            yield Request(abs_url,callback=self.parse_items)

        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        next_absolute = response.urljoin(next_page)
        yield Request(next_absolute,callback=self.parse_pages)

    def parse_items(self,response):
        agent_button = response.xpath('//*[@value="Agents"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in agent_button:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()
            address_1 = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_2 = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]
            address= ",".join(address_1+address_2)
            print(address)
            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td/text()').extract_first()
            url = response.url

            yield{
                'Name':name,
                'Address':address,
                'Phone':phone,
                'Fax':fax,
                'Email':email,
                'Url':url,
            }
        else:
            self.logger.info('Agent Button not found on page, passing invalid url.')