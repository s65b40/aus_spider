# -*- coding: utf-8 -*-
#author:Haochun Wang

import scrapy
import re
from scrapy import *
import re, sys
import requests

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # Bank of China currency website
html = requests.get(url).content.decode('utf8')
a = html.index('<td>澳大利亚元</td>')  # get the position of AUS dollar
s = html[a:a + 300]  # narrow down the range
rate_res = float(re.findall('<td>(.*?)</td>', s)[3]) * 0.01  # Regex get the currency


class ChemistSpider(scrapy.Spider):
    name = "chemistwarehouse"
    allowed_domains = ["www.chemistwarehouse.com.au"]
    start_urls = [
        "http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse",
        "http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse?page=2",
        "http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse?page=3",
        "http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse?page=4",
        "http://www.chemistwarehouse.com.au/Shop-Online/587/Swisse?page=5",

        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=2",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=3",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=4",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=5",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=6",
        "http://www.chemistwarehouse.com.au/Shop-Online/513/Blackmores?page=7",

        "http://www.chemistwarehouse.com.au/Shop-Online/660/Nature-s-Way",
        "http://www.chemistwarehouse.com.au/Shop-Online/660/Nature-s-Way?page=2",
        "http://www.chemistwarehouse.com.au/Shop-Online/660/Nature-s-Way?page=3",
        "http://www.chemistwarehouse.com.au/Shop-Online/660/Nature-s-Way?page=4",

        "http://www.chemistwarehouse.com.au/Shop-Online/722/Healthy-Care",
        "http://www.chemistwarehouse.com.au/Shop-Online/722/Healthy-Care?page=2",
        "http://www.chemistwarehouse.com.au/Shop-Online/722/Healthy-Care?page=3",
        "http://www.chemistwarehouse.com.au/Shop-Online/722/Healthy-Care?page=4",
        "http://www.chemistwarehouse.com.au/Shop-Online/722/Healthy-Care?page=5",

        "http://www.chemistwarehouse.com.au/Shop-Online/2128/Bio-Island"
    ]

    def parse(self, response):
        selector1 = Selector(response)
        name_space = selector1.xpath('//a[@class="product-container"]/@href').extract()
        price_space = selector1.xpath('//span[@class="Price"]').extract()
        pricesv = selector1.xpath('//div[@class="prices"]').extract()
        #print pricesv
        price_split_list = str(price_space).split(',')
        #p1 = r"(?<=u\''/buy'/\d+/).+?(?=\')"
        #pattern1 = re.compile(p1)
        p2 = r"(?<=u\'<span class=\"Price\">).+?(?=</span>\')"
        pattern2 = re.compile(p2)
        name_res_lst = []     # 商品名列表 product name list
        price_res_lst = []    # 价格列表 price list
        discount_res_lst = [] # 折扣列表 discount list
        for i in name_space:
            #name = re.search(pattern1, i)
            #name_res_lst.append(name.group(0)[1:])
            name_res_lst.append(i[11:])

        for j in price_split_list:
            price = re.search(pattern2, j)
            price_res_lst.append(price.group(0))

        for i in pricesv:
            u = i.split('class="Price">')
            price_item = float(u[1].split('\n')[0][1:])
            if 'class="Save"' in u[1]:
                #print 'yes'
                save_item = float(u[1].split('SAVE')[1].split('</span>')[0].strip(' ').strip('\n')[1:])
                #print save_item
                discount = '%.1f' % (price_item / (price_item + save_item) * 10)
                #print discount
                discount_res_lst.append(discount)
            else:
                discount_res_lst.append(10)
        for k in range(len(name_res_lst)):
            with open("res_tmp.txt", "a+") as b:
                b.writelines(name_res_lst[k] + ', '+price_res_lst[k].split(' ')[0] + ', ' +
                             str((float(price_res_lst[k].split(' ')[0][1:]) + 10) * (rate_res + 0.3))
                             + ', ' + str(discount_res_lst[k]) + '\n')

        #正则表达式必知必会
        #.extract()