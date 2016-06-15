# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SermonItem(scrapy.Item):
    title = scrapy.Field()
    date_preached = scrapy.Field()
    scripture = scrapy.Field()
    ref = scrapy.Field()
    link = scrapy.Field()
