# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand = scrapy.Field()
    model_name = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    views = scrapy.Field()
    image = scrapy.Field()
    os = scrapy.Field()
    cellular_technology = scrapy.Field()
    memory_storage = scrapy.Field()
    connectivity = scrapy.Field()
    color = scrapy.Field()
    screen_size = scrapy.Field()
    link = scrapy.Field()
    pass
