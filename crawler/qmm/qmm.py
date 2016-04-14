#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib

images_path="images/"
url_done = []

class MySpider(scrapy.Spider):

    name = "qiushimm"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

    start_urls = [
            "http://www.qiushimm.com/",                 # static files
            "http://www.qiushimm.com/tag/gif",   # dynamic files
                 ]

    def parse(self, response):
        img_tags = response.xpath('//*/div/p/img')

        for img_tag in img_tags:
            img_url = img_tag.xpath('@src').extract()[0]
            img_alt = img_tag.xpath('@alt').extract()[0]
            urllib.urlretrieve(img_url, images_path + img_url.split('/')[-1])
            self.logger.info("Got " + img_url)

        for url_selector in response.xpath("//*/div[11]/div/a/@href"):
            url = url_selector.extract()
            if url not in url_done:
                url_done.append(url)
                yield Request(url, callback=self.parse)
