#!/usr/bin/env python

import scrapy
from scrapy.http import Request

import os
import re
import shutil
import time
import urllib

# TODO(adamas): move it to a configuration file
images_dir="images"

root_url = 'http://www.houzz.com'

class HouzzSpider(scrapy.Spider):

    name = "houzz"

    def __init__(self):
        if not os.access(images_dir, os.F_OK):
            os.mkdir(images_dir)

        # counter
        self.page_counter = 0
        self.image_counter = 0

        # hash set
        self.page_urls_bucket = []
        self.image_urls_bucket = []

        # the urls thest had been crawled
        crawled_urls = []

        # map that associate the image description url and image url
        self.image_map = {}

    start_urls = [
            "http://www.houzz.com/photos/artwork",
                 ]

    def parse(self, response):
        self.page_counter += 1
        self.logger.info("the " + str(self.page_counter) + " pages")
        image_list = response.xpath('//*[@id="browseSpacesContext"]/div/div/div/div/a/div[1]/img')

        for image in image_list:
            image_url = image.xpath('@src').extract()[0]
            image_desc_url = response.xpath('//*[@id="browseSpacesContext"]/div[1]/div[1]/div[2]/a').xpath('@href').extract()[0]
            self.image_map[image_desc_url] = image_url

            if image_desc_url in self.image_urls_bucket:
                continue
            else:
                self.image_urls_bucket.append(image_desc_url)
            self.logger.info("Go to " + image_url)
            yield Request(image_desc_url, callback=self.parse_desc)

        # next page
        for url in response.xpath('//*[@id="paginationBar"]/li/a').xpath('@href').extract():
            if url in self.page_urls_bucket:
                continue
            else:
                self.page_urls_bucket.append(url)
            self.logger.info("Got page " + url)
            yield Request(url, callback=self.parse)

    def parse_desc(self, response):
        self.image_counter += 1
        self.logger.info("the " + str(self.image_counter) + " images")

        attribute_count = int(float(response.xpath('count(//*[@id="hzProductInfo"]/*/*/div[2]/dl/dd)').extract()[0]))
        xpath_str = '//*[@id="hzProductInfo"]/*/*/div[2]/dl/'

        manufacturer = ""
        material = ""

        for i in range(1, attribute_count+1):
            key = response.xpath(xpath_str+"/dt["+str(i)+"]/text()").extract()[0].strip()
            #value = "".join(response.xpath(xpath_str+"/dd["+str(i)+"]/span//text()").extract()).strip()
            #self.logger.info("key is " + key)

            if key == "Manufactured By":
                manufacturer = "".join(response.xpath(xpath_str+"/dd["+str(i)+"]/span//text()").extract()).strip()
                self.logger.info("Get Manufactured, " + manufacturer)
            elif key == "Materials":
                material = "".join(response.xpath(xpath_str+"/dd["+str(i)+"]//text()").extract()).strip()
                self.logger.info("Get Materials, " + material)

        if len(manufacturer) == 0:
            self.logger.info("manufacturer is null. url is " + response.url)
            self.logger.info("   \n\n\n")
        if len(material) == 0:
            self.logger.info("material is null. url is " + response.url)
            self.logger.info("   \n\n\n")

        self.download_image(self.image_map[response.url], manufacturer, material)

    def download_image(self, url, manufacturer, material):
        # replace the original url to the new one
        url_parts = re.match("(.*)-w\d+-h\d+-(.*)", url).groups()
        prefix = url_parts[0]
        postfix = url_parts[1]
        image_url = prefix + "-w1200-h1200-" + postfix

        # extract file name from the url
        image_name = image_url[image_url.rfind('/')+1:]

        # the direct to put this image in, and its full path
        image_dir = images_dir + "/" + manufacturer + "/" + material
        image_path = image_dir + "/" + image_name

        # check if the directory exists
        if not os.access(image_dir, os.R_OK|os.W_OK):
            os.makedirs(image_dir)

        # if the image already exists in the images_dir, move it
        already_download_image = images_dir + os.sep + image_name
        if os.access(already_download_image, os.F_OK):
            shutil.move(already_download_image, image_path)

        # check if the image exists, if not, download
        if not os.access(image_path, os.F_OK):
            urllib.urlretrieve(image_url, image_path)
            self.logger.info("Got " + image_url)
        else:
            self.logger.info(image_url + " already exists")
