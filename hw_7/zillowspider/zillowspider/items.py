# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join


class ZillowspiderItem(scrapy.Item):
    _id = scrapy.Field()
    address = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
