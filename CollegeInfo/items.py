# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class scrapedInfo(scrapy.Item):
    site = scrapy.Field()
    name = scrapy.Field()
    rank = scrapy.Field()
    location = scrapy.Field()
    cost = scrapy.Field()
    icon = scrapy.Field()
    link = scrapy.Field()
