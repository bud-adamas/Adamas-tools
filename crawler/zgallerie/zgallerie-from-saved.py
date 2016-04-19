#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import urllib
import time

# TODO(adamas): move it to a configuration file
images_path="images/"

cwd_path=os.getcwd()
saved_html_name="Stylish.html"
file_url = "file://" + cwd_path + "/" + saved_html_name


class ZgallerieSpider(scrapy.Spider):

    name = "zgallerie"

    def __init__(self):
        if not os.access(images_path, os.F_OK):
            os.mkdir(images_path)

        url_done = []

    start_urls = [
            file_url
                 ]

    def parse(self, response):
        image_list = response.xpath('//*[@id="myDiv"]/div/div/div[1]/a')

        for image in image_list:
            img_detail_url = image.xpath('@href').extract()[0]

            self.logger.info("Go to " + img_detail_url)
            yield Request(img_detail_url.replace('https', 'http'), callback=self.parse_item)

    def parse_item(self, response):
        # get the image name
        pic_id = 'ProductPic' + response.url.split('/')[-1].split('-')[1]
        image_url = response.xpath('//*[@id="' + pic_id + '"]/@src').extract()[0]
        image_name = image_url.split('/')[-1]

        # get the image url
        HiddenProductDetails = response.xpath('//*[@id="HiddenProductDetails"]').extract()[0]
        r = re.compile('.*SjZViewer\((.*)\)')
        m = r.match(HiddenProductDetails.replace('\'', '')).groups()[0]
        url_base = "".join(m.split(',')[0:2])
        url_params = "?rect=0,0,1000,1000&scl=2.315789473684211"
        url = url_base + url_params

        # download
        img_path = images_path + image_name
        url_file = open('url_file', 'a')
        url_file.write("urllib.urlretrieve(\"" + url_base + "?\" + rect + \"&\" + scl" + ", \"" + img_path + "\")\n")
        url_file.close()
        if not os.access(img_path, os.R_OK):
            time.sleep(10)
            urllib.urlretrieve(url, img_path)
            self.logger.info("Got " + image_url)
        else:
            self.logger.info(image_url + " already exists")
