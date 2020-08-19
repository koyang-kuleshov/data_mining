# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaParseItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    post_photos = scrapy.Field()
    post_pub_date = scrapy.Field()
    like_count = scrapy.Field()
