# -*- coding: utf-8 -*-
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class StfPipeline(object):
    def process_item(self, item, spider):
        for i, decisao in enumerate(item):
            item[i] = re.sub('')
        return item
