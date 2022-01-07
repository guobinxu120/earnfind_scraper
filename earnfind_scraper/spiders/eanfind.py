# -*- coding: utf-8 -*-
from scrapy import Spider, Request
# from urlparse import urlparse
import sys
# import re, os, requests, urllib
from scrapy.utils.response import open_in_browser
from collections import OrderedDict
import time
from xlrd import open_workbook
from shutil import copyfile
import json, re, csv
from scrapy.http import FormRequest
from scrapy.http import TextResponse
# def download(url, destfilename):
#     if not os.path.exists(destfilename):
#         print "Downloading from {} to {}...".format(url, destfilename)
#         try:
#             r = requests.get(url, stream=True)
#             with open(destfilename, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()
#         except:
#             print "Error downloading file."
#
# def readExcel(path):
#     wb = open_workbook(path)
#     result = []
#     for sheet in wb.sheets():
#         number_of_rows = sheet.nrows
#         number_of_columns = sheet.ncols
#         herders = []
#         for row in range(0, number_of_rows):
#             values = OrderedDict()
#             for col in range(number_of_columns):
#                 value = (sheet.cell(row,col).value)
#                 if row == 0:
#                     herders.append(value)
#                 else:
#
#                     values[herders[col]] = value
#             if len(values.values()) > 0:
#                 result.append(values)
#
#     return result


class AngelSpider(Spider):
    name = "earnfind_all"
    start_urls = ['https://www.eanfind.fr/marques-populaires']

    use_selenium = False


    models = []

    count = 0
    # //////// angel headers and cookies////////////
    headers = {
                'Host': 'angel.co',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cookie': 'intercom-id-og2vxfl5=1ca11f39-d87c-40ce-a608-a220d8e5e980; ajs_anonymous_id=%226b6ea0b7-b64f-4e85-b717-4b60c9912784%22; _ga=GA1.2.567149796.1514406722; _gid=GA1.2.1678712760.1514864845; ajs_group_id=null; ajs_user_id=%227305367%22; _angellist=a71a277ab05568d2fe069eb936c75c05; amplitude_idangel.co=eyJkZXZpY2VJZCI6IjU5MWU0NTQwLWI2YmItNGRjNi1iZGZiLTUwMTk0OTI4Nzg3ZVIiLCJ1c2VySWQiOiI3MzA1MzY3Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTE1MDg3MTAzNDk0LCJsYXN0RXZlbnRUaW1lIjoxNTE1MDg4MDM1MjYwLCJldmVudElkIjoyMDEsImlkZW50aWZ5SWQiOjI1NCwic2VxdWVuY2VOdW1iZXIiOjQ1NX0=; _gat=1',
                'If-None-Match': 'W/"b42e1a728069ee24c32f7b180e165727"',
                # 'X-CSRF-Token': '6mr8EeXtLQurR32ZwHcDHEEKHoL544riKhvqVv5NMQtdpaWeXnvlIUXW3cjZj7uzzEuZhqnvfqfh+zbWhnj6RQ==',
                # 'X-Requested-With': 'XMLHttpRequest'
            }
    cookies = {'_angellist' :'a71a277ab05568d2fe069eb936c75c05'}

    headers = ['Nom du produit', 'EAN', 'Marque', 'Modèle', 'Couleurs', 'Type de produit', 'Description', 'Chemin', 'Eanfind link']

    def parse(self, response):
        urls = response.xpath('//div[@class="letterFilter"]/a/@href').extract()
        for i, url in enumerate(urls):
            if i < 8: continue
            yield Request(url, self.parse1)
            # break
    def parse1(self, response):
        urls = response.xpath('//ul[@class="top-result"]/li/a/@href').extract()
        for url in urls:
            yield Request(url, self.parse2)
            # break

    def parse2(self, response):
        urls = response.xpath('//ul[@class="search-result moz"]/li/a/@href').extract()
        for url in urls:
            yield Request(url, self.finalparse)
        next_url = response.xpath('//i[@class="icon-angle-right"]/parent::span/parent::li/@data-page').extract_first()
        if next_url:
            url = response.url.split('/&filters:page=')[0] + '/&filters:page={}'.format(next_url)
            yield Request(url, self.parse2)
    def finalparse(self, response):
        item = OrderedDict()
        for header in self.headers:
            item[header] = ''
        item['EAN'] = response.xpath('//meta[@itemprop="gtin13"]/@content').extract_first()
        item['Nom du produit'] = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        item['Marque'] = response.xpath('//a[@itemprop="brand"]/text()').extract_first()
        item['Modèle'] = response.xpath('//span[@itemprop="mpn"]/text()').extract_first()
        colors = response.xpath('//span[@class="colorGroup"]/@title').extract()
        color_list = []
        for color in colors:
            color_list.append(color.split('(')[0])
        item['Couleurs'] = ','.join(color_list)
        item['Type de produit'] = response.xpath('//input[@id="tp"]/@value').extract_first()
        item['Description'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        if item['Description']:
            pass
        item['Chemin'] = ' > '.join(response.xpath('//ul[@class="breadcrumb_ligne"]/li/a/text()').extract())
        item['Eanfind link'] = response.url

        self.count+=1
        print(self.count)

        # self.models.append(item)
        yield item

