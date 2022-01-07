# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import xlsxwriter
import os
class EarnfindScraperPipeline(object):
    def __init__(self):
            #Instantiate API Connection
            self.files = {}
            # print ">>>>>> Initialize pipeline."

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline


    def spider_opened(self, spider):
        filepath = 'output_rest.xlsx'
        if os.path.isfile(filepath):
            os.remove(filepath)
        self.workbook = xlsxwriter.Workbook(filepath, {'strings_to_urls': False})
        self.sheet = self.workbook.add_worksheet('feuil1')
        # data = spider.models
        # flag = True
        self.headers = ['Nom du produit', 'EAN', 'Marque', 'Modèle', 'Couleurs', 'Type de produit', 'Description', 'Chemin', 'Eanfind link']
        self.index = 0
        for col, val in enumerate(self.headers):
            self.sheet.write(self.index, col, val)
        self.index+=1
    def spider_closed(self, spider):
        pass
        # filepath = 'output.xlsx'
        # if os.path.isfile(filepath):
        #     os.remove(filepath)
        # workbook = xlsxwriter.Workbook(filepath)
        # sheet = workbook.add_worksheet('feuil1')
        # data = spider.models
        # flag =True
        # headers = []
        # for index, value in enumerate(data):
        #     if flag:
        #         for col, val in enumerate(value.keys()):
        #             headers.append(val)
        #             sheet.write(index, col, val)
        #         flag = False
        #     for col, key in enumerate(headers):
        #         sheet.write(index+1, col, value[key])
        #
        self.workbook.close()



    def process_item(self, item, spider):
        # self.exporter.export_item(dict(item))
        # file = self.files[spider]
        # file.write(",")
        for col, key in enumerate(self.headers):
            self.sheet.write(self.index, col, item[key])
        self.index += 1
        return item
