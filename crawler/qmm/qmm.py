#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib

# the directory to hold the images
# TODO(adamas): move these to a configuration file
images_path="images/"


class QmmSpider(scrapy.Spider):

    name = "qiushimm"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

        # the crawled pages, only valid at this class scope.
        # as these pages are generated dynamically.
        url_done = []

    start_urls = [
            "http://www.qiushimm.com/",                 # static files
            "http://www.qiushimm.com/tag/gif",          # dynamic files
                 ]

    def parse(self, response):
        # extract the list of <img> tag
        img_tags = response.xpath('//*/div/p/img')

        for img_tag in img_tags:
            # the *src* and *alt* attribute
            img_url = img_tag.xpath('@src').extract()[0]
            img_alt = img_tag.xpath('@alt').extract()[0]

            # Download the file.
            # TODO(adamas): de-duplicate
            # TODO(adamas): seperate this into these steps in another thread(or process):
            #   1. add this url to a table in database,
            #   2. download the file pointed by the url, got from the table,
            #   3. check the content of the file, to decide if it succeed,
            #   4. if succeed, mark the table and go on,
            #       otherwise try it later.
            urllib.urlretrieve(img_url, images_path + img_url.split('/')[-1])
            self.logger.info("Got " + img_url)

        # go to other pages
        for url_selector in response.xpath("//*/div[11]/div/a/@href"):
            url = url_selector.extract()
            if url not in self.url_done:
                self.url_done.append(url)
                yield Request(url, callback=self.parse)
