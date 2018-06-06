# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json


class SubjectsSpider(scrapy.Spider):
    name = 'subjects'
    allowed_domains = ['class-central.com']
    start_urls = ['https://www.class-central.com/subjects']

    def __init__(self,subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//*[contains(@title,"'+self.subject+'")]/@href').extract_first()
            yield Request(response.urljoin(subject_url),callback=self.parse_subject)
        else:                
            subjects = response.xpath('//*[@class="show-all-subjects view-all-courses"]/@href').extract()
            for subject in subjects:
                yield Request(response.urljoin(subject),callback=self.parse_subject)

    def parse_subject(self,response):
        courses = response.xpath('//tr[@itemscope]')
        for course in courses:
            course_link = course.xpath('.//a[@itemprop="url"]/@href').extract_first()
            try:
                course_metadata = json.loads(course.xpath('.//a[@itemprop="url"]/@data-track-props').extract_first())
                course_name = course_metadata['clickMetadata']['course']
                course_provider = course_metadata['clickMetadata']['provider']
                course_institution = course_metadata['clickMetadata']['institution']

                yield {
                    'Name':course_name,
                    'Link':course_link,
                    'Provider':course_provider,
                    'Institution':course_institution
                }
            except:
                pass
        
        next_page_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        absolute_path = response.urljoin(next_page_url)
        yield Request(absolute_path,callback=self.parse_subject)

            