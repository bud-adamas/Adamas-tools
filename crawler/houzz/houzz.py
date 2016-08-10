#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib
import time

# TODO(adamas): move it to a configuration file
images_path="images/"

root_url = 'http://www.houzz.com'

class HouzzSpider(scrapy.Spider):

    name = "houzz"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

        url_done = []

    start_urls = [
            "http://www.houzz.co.uk/photos/artwork-and-prints",
                 ]

    def parse(self, response):
        image_list = response.xpath('//*[@id="browseSpacesContext"]/div/div/div/div/a')

        for image in image_list:
            img_detail_url = image.xpath('@href').extract()[0]

            self.logger.info("Go to " + img_detail_url)
            time.sleep(1)
            yield Request(img_detail_url, callback=self.parse_item)

        # next page
        yield Request(response.xpath('//*[@class="navigation-button next"]')[-1].xpath('@href').extract()[0], callback=self.parse)

    def parse_item(self, response):
        image_url = response.xpath('//*[@id="mainImage"]').xpath('@src').extract()[0]
        image_name = image_url[image_url.rfind('/')+1:]

        img_path = images_path + image_name
        if not os.access(img_path, os.R_OK):
            urllib.urlretrieve(image_url, img_path)
            self.logger.info("Got " + image_url)
        else:
            self.logger.info(image_url + " already exists")
