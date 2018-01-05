# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class MongoDBPipeline(object):

    def __init__(self): 
        #establish connection to MongoDB database
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        #put the data in, depending on the name of the site
        self.collection = self.db[item['site']]
        self.collection.update({'name': item['name']}, dict(item), upsert=True) #not insert because want to modify if already existing
        return item
