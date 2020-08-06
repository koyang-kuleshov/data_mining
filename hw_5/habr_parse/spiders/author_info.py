"""
получив данные о авторе сохранить данные о авторе,
и вам необходмо зайти на его страницу и обойти все его статьи.

таким образом у вас будет item для авторов, структуру
необходимо спроектировать вам, необходимо получить всю
информацию в блоке ИНФОРМАЦИЯ, Имя, url, nicname и
всю возможную контактную информацию
полученые айтемы необходимо сохранять в базе данных
MONGO в отдельных коллекциях для статей, и авторов.
"""
import scrapy
from scrapy.loader import ItemLoader
from habr_parse.items import HabrAuthorItem


class AuthorInfoSpider(scrapy.Spider):
    name = 'author_info'
    allowed_domains = ['habr.com']
    # start_urls = ['https://habr.com/ru/users/SLY_G/']

    selectors = {
        'author_fullname': '//h1/a[contains(\
            @class, "user-info__fullname")]/text()',
        'author_nickname': '//h1/a[contains(\
            @class, "user-info__nickname")]/text()',
        'author_info': '//div[contains(@class, "profile-section__about-text")]\
        //text()',
        'author_contact': '//ul[contains(@class, "defination-list")]/li/span/\
        text()',
    }

    def __init__(self, start_url):
        if start_url.find('//') > 0:
            # self.start_url = [start_url]
            self.start_urls = ['https://habr.com/ru/users/SLY_G/']
        else:
            self.start_urls = [f'https://habr.com/ru{start_url}']

    def parse(self, response):
        item = ItemLoader(HabrAuthorItem, response)
        for key, value in self.selectors.items():
            item.add_xpath(key, value)
        item.add_value('author_url', response.url)

        yield item.load_item()
