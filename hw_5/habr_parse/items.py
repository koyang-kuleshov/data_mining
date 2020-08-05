import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def clean_comment(value):
    spam = list()
    for el in value:
        spam.append(el.strip())
    return spam


class HabrParseItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    comments = scrapy.Field(
        input_processor=MapCompose(clean_comment),
        # input_processor=TakeFirst(),
        # output_processor=MapCompose(str.strip)
        output_processor=TakeFirst()
        )
    author_name = scrapy.Field(output_processor=TakeFirst())
    author_url = scrapy.Field(output_processor=TakeFirst())
    post_url = scrapy.Field(output_processor=TakeFirst())


class HabrAuthorItem(scrapy.Item):
    _id = scrapy.Field()
    info = scrapy.Field()
    name = scrapy.Field()
    author_url = scrapy.Field()
    nickname = scrapy.Field()
    contact = scrapy.Field()
