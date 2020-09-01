import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def clean_comment(value):
    spam = list()
    for el in value:
        spam.append(el.strip())
    return spam


def make_info_text(lst):
    return lst.lstrip().rstrip()


def clean_contact_list(value):
    spam = value.lstrip().rstrip()
    if spam:
        return spam


class HabrParseItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    comments = scrapy.Field(
        input_processor=MapCompose(clean_comment),
        output_processor=TakeFirst()
        )
    author_name = scrapy.Field(output_processor=TakeFirst())
    author_url = scrapy.Field(output_processor=TakeFirst())
    post_url = scrapy.Field(output_processor=TakeFirst())


class HabrAuthorItem(scrapy.Item):
    _id = scrapy.Field()
    author_fullname = scrapy.Field(output_processor=TakeFirst())
    author_nickname = scrapy.Field(output_processor=TakeFirst())
    author_info = scrapy.Field(
        input_processor=MapCompose(make_info_text),
        output_processor=Join()
    )
    author_contact = scrapy.Field(
        input_processor=MapCompose(clean_contact_list),
        output_processor=Join()
    )
    author_url = scrapy.Field(output_processor=TakeFirst())
