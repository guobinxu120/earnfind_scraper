# # -*- coding: utf-8 -*-
# from scrapy import Spider, Request
# from urlparse import urlparse
# import sys
# import re, os, requests, urllib
# from scrapy.utils.response import open_in_browser
# from collections import OrderedDict
# import time
# from xlrd import open_workbook
# from shutil import copyfile
# import json, re, csv
# from scrapy.http import FormRequest
# from scrapy.http import TextResponse
# def download(url, destfilename):
#     if not os.path.exists(destfilename):
#         # print "Downloading from {} to {}...".format(url, destfilename)
#         # try:
#             r = requests.get(url, stream=True)
#             with open(destfilename, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#                         f.flush()
#         # except:
#             # print "Error downloading file."
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
#
#
# class AngelSpider(Spider):
#     name = "earnfind"
#     start_urls = 'https://www.eanfind.fr/chercher/'
#
#     use_selenium = False
#
#
#     models = readExcel("Model_veille.xlsx")
#
#
#     # //////// angel headers and cookies////////////
#     headers = {
#                 'Host': 'angel.co',
#                 'Connection': 'keep-alive',
#                 'Cache-Control': 'max-age=0',
#                 'Upgrade-Insecure-Requests': '1',
#                 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                 'Accept-Encoding': 'gzip, deflate, sdch, br',
#                 'Accept-Language': 'en-US,en;q=0.8',
#                 'Cookie': 'intercom-id-og2vxfl5=1ca11f39-d87c-40ce-a608-a220d8e5e980; ajs_anonymous_id=%226b6ea0b7-b64f-4e85-b717-4b60c9912784%22; _ga=GA1.2.567149796.1514406722; _gid=GA1.2.1678712760.1514864845; ajs_group_id=null; ajs_user_id=%227305367%22; _angellist=a71a277ab05568d2fe069eb936c75c05; amplitude_idangel.co=eyJkZXZpY2VJZCI6IjU5MWU0NTQwLWI2YmItNGRjNi1iZGZiLTUwMTk0OTI4Nzg3ZVIiLCJ1c2VySWQiOiI3MzA1MzY3Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNTE1MDg3MTAzNDk0LCJsYXN0RXZlbnRUaW1lIjoxNTE1MDg4MDM1MjYwLCJldmVudElkIjoyMDEsImlkZW50aWZ5SWQiOjI1NCwic2VxdWVuY2VOdW1iZXIiOjQ1NX0=; _gat=1',
#                 'If-None-Match': 'W/"b42e1a728069ee24c32f7b180e165727"',
#                 # 'X-CSRF-Token': '6mr8EeXtLQurR32ZwHcDHEEKHoL544riKhvqVv5NMQtdpaWeXnvlIUXW3cjZj7uzzEuZhqnvfqfh+zbWhnj6RQ==',
#                 # 'X-Requested-With': 'XMLHttpRequest'
#             }
#     cookies = {'_angellist' :'a71a277ab05568d2fe069eb936c75c05'}
#
#     # f2 = open('./total.csv')
#     # csv_items = csv.DictReader(f2)
#     # validate_mails = []
#     # for row in csv_items:
#     #     validate_mails.append(row)
#
#
#     def start_requests(self):
#         for i, infor in enumerate(self.models):
#             if infor['Price - (France)'] == "" and infor['Lowest price'] == "":
#                 yield Request(self.start_urls + str(int(infor['EAN'])), callback=self.parse, meta={'order':i})
#
#     def parse(self, response):
#         order_num = response.meta['order']
#         id = response.xpath('//input[@id="esin"]/@value').extract_first()
#         fr_tags = response.xpath('//tr[@class="linkOut "]')
#
#         lowest_fr = ''
#         lowest_fr_link = ''
#         if len(fr_tags) > 0:
#             lowest_fr = fr_tags[0].xpath('.//td[@class="center"]/@data-price').extract_first()
#             fr_url = fr_tags[0].xpath('./@data-l').extract_first()
#             lowest_fr_link = 'https://www.eanfind.fr/go/' + fr_url
#
#         country_tags = response.xpath('//div[@class="ruler"]/div')
#         for country_tag in country_tags:
#             country = country_tag.xpath('./@data-country').extract_first()
#             price = country_tag.xpath('.//span[@class="price"]/text()').extract_first()
#             if country != "FR" and price and price != "":
#                 frmdata = {"action": "product/ajax.loadCountryPrice", "country": country, "esin": id}
#                 url = "https://www.eanfind.fr/ajax.php"
#                 yield FormRequest(url, callback=self.global_parse, formdata=frmdata, meta={'order':order_num})
#                 break
#         self.models[order_num]['Price - (France)'] = lowest_fr
#         self.models[order_num]['Link to French Lowest price'] = lowest_fr_link
#
#
#         # lowest_country = response.xpath('//div[@class="ruler"]/div[1]/@data-country').extract_first()
#         # # lowest_global_link = lowest_fr_link.replace('-FR-', "-"+lowest_country+"-")
#         # if len(fr_url.split(":")) > 0 :
#         #     frmdata = {"action": "product/ajax.loadCountryPrice", "country": lowest_country, "esin": id}
#         #     url = "https://www.eanfind.fr/ajax.php"
#         #     yield FormRequest(url, callback=self.global_parse, formdata=frmdata, meta={'order':order_num})
#
#
#     def global_parse(self, response):
#         order_num = response.meta['order']
#         data = json.loads(response.body)
#         if data['etat'] == "success":
#             resp = TextResponse(url="dddd",
#                                 body=data['content'],
#                                 encoding='utf-8')
#
#             fr_tags = resp.xpath('//tr[@class="linkOut "]')
#             lowest_fr = ''
#             lowest_fr_link = ''
#             fr_url = ""
#             if len(fr_tags) > 0:
#                 lowest_fr = fr_tags[0].xpath('.//td[@class="center"]/@data-price').extract_first()
#                 fr_url = fr_tags[0].xpath('./@data-l').extract_first()
#                 lowest_fr_link = 'https://www.eanfind.fr/go/' + fr_url
#
#             self.models[order_num]['Lowest price'] = lowest_fr
#             self.models[order_num]['Link to Lowest price'] = lowest_fr_link
#
