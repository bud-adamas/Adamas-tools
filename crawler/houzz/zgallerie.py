#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib
import time

# TODO(adamas): move it to a configuration file
images_path="images/"

root_url = 'http://www.zgallerie.com'

class ZgallerieSpider(scrapy.Spider):

    name = "zgallerie"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

        url_done = []

    start_urls = [
            #"http://www.zgallerie.com/ViewAll.aspx?N=2000040",
            "file:///home/adamas/tmp/adamas-tools/crawler/zgallerie/Stylish.html"
                 ]

    def parse(self, response):
        image_list = response.xpath('//*[@id="myDiv"]/div/div/div[1]/a')

        for image in image_list:
            img_detail_url = image.xpath('@href').extract()[0]
            image_url = "http:" + image.xpath('img/@src').extract()[0]

            img_path = images_path + img_detail_url.split('.')[0] + "-s.jpg"
            #urllib.urlretrieve(image_url, img_path)
            #self.logger.info("Got " + image_url)

            dest_url = root_url + img_detail_url
            #pic_id = 'ProductPic' + img_detail_url.split('.')[0].split('-')[1]

            self.logger.info("Go to " + img_detail_url)
            time.sleep(10)
            yield Request(img_detail_url.replace('https', 'http'), callback=self.parse_item)

    def parse_item(self, response):
        pic_id = 'ProductPic' + response.url.split('/')[-1].split('-')[1]
        image_url = response.xpath('//*[@id="' + pic_id + '"]/@src').extract()[0]
        image_name = image_url.split('/')[-1]

        HiddenProductDetails = response.xpath('//*[@id="HiddenProductDetails"]').extract()[0]
        r = re.compile('.*SjZViewer\((.*)\)')
        m = r.match(HiddenProductDetails.replace('\'', '')).groups()[0]
        url = "".join(m.split(',')[0:2]) + "?rect=0,0,1000,1000&scl=2.315789473684211"

        img_path = images_path + image_name
        if not os.access(img_path, os.R_OK):
            urllib.urlretrieve(url, img_path)
            self.logger.info("Got " + image_url)
        else:
            self.logger.info(image_url + " already exists")
