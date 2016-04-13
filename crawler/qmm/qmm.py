#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import re
import urllib

url_done = []

class MySpider(scrapy.Spider):
    def __init__(self):
        pass

    name = "qiushimm"

    start_urls = ["http://www.qiushimm.com/tag/gif/page/40",
                 ]

    def parse(self, response):
        img_tags = response.xpath('//*/div/p/img')

        for img_tag in img_tags:
            img_url = img_tag.xpath('@src').extract()[0]
            img_alt = img_tag.xpath('@alt').extract()[0]
            #print(img_url + " @ " + img_alt)
            urllib.urlretrieve(img_url, img_url.split('/')[-1])

        for url_selector in response.xpath("//*/div[11]/div/a/@href"):
            url = url_selector.extract()
            if url not in url_done:
                url_done.append(url)
                yield Request(url, callback=self.parse)
