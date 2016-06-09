# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LVRItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    currency_code = scrapy.Field()
    price = scrapy.Field()
    keywords = scrapy.Field()
    category = scrapy.Field()
    sku = scrapy.Field()
    photos = scrapy.Field()
    url = scrapy.Field()
