# -*- coding: utf-8 -*-
#author:Haochun Wang

# -*- coding: utf-8 -*-
#author:Haochun Wang

import scrapy
from scrapy import *
import urllib2
a = urllib2.urlopen("http://au.ugg.com")
print a.read()
'''
class UggSpider(scrapy.Spider):
    name = "ugg"
    allowed_domains = ["au.ugg.com"]
    start_urls = [
        "https://au.ugg.com/sale/women"
    ]

    def parse(self, response):
        selector1 = Selector(response)
        namesp = selector1.xpath('*').extract()
        #namesp = selector1.xpath('//div[@class="prices"]').extract()
        #pricesp = selector1.xpath('//span[@class="Price"]').extract()
        #namesplitlst = str(namesp).split(', ')
        with open('2.txt', 'a+') as b:
            b.writelines(str(namesp))

        #正则表达式必知必会
        #.extract()
'''