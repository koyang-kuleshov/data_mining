import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def clean_comment(value):
    spam = list()
    for el in value:
        spam.append(el.strip())
    return spam

def make_info_text(lst):
    # spam = ''
    # for el in lst:
    #     print(el)
    #     print(type(el))
        # spam += f'{el} '
    # spam = [el.rstrip().lstrip() for el in lst if el.strip() != ""]
    return lst.lstrip().rstrip()


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
    author_contact = scrapy.Field()
    author_url = scrapy.Field(output_processor=TakeFirst())
