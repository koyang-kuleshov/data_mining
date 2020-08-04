import scrapy


class HabrParseItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()
    comments = scrapy.Field()
    autor_name = scrapy.Field()
    autor_url = scrapy.Field()
    post_url = scrapy.Field()
