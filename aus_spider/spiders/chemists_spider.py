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
url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # 网址
html = requests.get(url).content.decode('utf8')  # 获取网页源码（中间涉及到编码问题,这是个大坑，你得自己摸索）
a = html.index('<td>澳大利亚元</td>')  # 取得“新西兰元”当前位置
s = html[a:a + 300]  # 截取新西兰元汇率那部分内容（从a到a+300位置）
rateres = float(re.findall('<td>(.*?)</td>', s)[3]) * 0.01  # 正则获取

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
        "http://www.chemistwarehouse.com.au/Shop-Online/660/Nature-s-Way?page=4"
    ]

    def parse(self, response):
        selector1 = Selector(response)
        namesp = selector1.xpath('//a[@class="product-container"]/@href').extract()
        pricesp = selector1.xpath('//span[@class="Price"]').extract()

        pricesplitlst = str(pricesp).split(',')
        #p1 = r"(?<=u\''/buy'/\d+/).+?(?=\')"
        #pattern1 = re.compile(p1)
        p2 = r"(?<=u\'<span class=\"Price\">).+?(?=</span>\')"
        pattern2 = re.compile(p2)
        name_res_lst = []
        price_res_lst = []
        for i in namesp:
            #name = re.search(pattern1, i)
            #name_res_lst.append(name.group(0)[1:])
            name_res_lst.append(i[11:])

        for j in pricesplitlst:
            price = re.search(pattern2, j)
            price_res_lst.append(price.group(0))

        for k in range(len(name_res_lst)):
            with open("res_tmp.txt", "a+") as b:
                b.writelines(name_res_lst[k]+', '+price_res_lst[k].split(' ')[0] + ', ' +
                             str((float(price_res_lst[k].split(' ')[0][1:]) + 10) * (rateres + 0.3)) +'\n')

        #正则表达式必知必会
        #.extract()