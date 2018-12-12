# -*- coding: utf-8 -*-
import scrapy


class Gto365Spider(scrapy.Spider):
    name = 'gto365'
    allowed_domains = ['gto365.com']
    start_urls = ['http://gto365.com/']

    def parse(self, response):
        pass
