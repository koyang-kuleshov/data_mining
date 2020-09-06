"""Источник: https://www.zillow.com

при старте паука передается список локаций которые необходимо обойти.

Необходимо обойти все объявления и собрать след структуру данных:

price - цена указанная в объявлении
address - поле адреса указанное в объвлении
photos - все фотографии из объявления в максимальном разрешении
( необходимо скачать и сохранить на компьютере)
"""

import re

import scrapy
from scrapy.loader import ItemLoader

from zillowspider.items import ZillowspiderItem


class ZillowSpider(scrapy.Spider):
    """Spider for scraping zillow.com"""
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/']

    def __init__(self, region: str, *args, **kwargs):
        self.start_urls = [f'{self.start_urls[0]}{region}/']
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """Main parse function"""
        real_estate = response.xpath('//a[@class="list-card-link"]/@href')
        for url in real_estate:
            yield response.follow(
                url,
                callback=self.get_real_estate_data
            )
        pages = response.xpath('//nav[@role="navigation"]/ul/li/a/@href')
        for page in pages:
            # yield response.follow(page, callback=self.parse)
            print(page)

    @staticmethod
    def get_real_estate_data(response):
        """Method for parsing real estate data card"""
        item = ItemLoader(ZillowspiderItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('address',
                       '//head/title/text()'
                       )
        item.add_xpath('price',
                       '//h3[contains(@class, "ds-price")]//span[@class="ds-value"]/text()')
        li_img = response.xpath('//ul[contains(@class, "media-stream")]/li')
        src_img = response.xpath('//ul[contains(@class, "media-stream")]/li\
                                 /button/picture/source\
                                 [contains(@type, "image/jpeg")]'
                                 )
        spam = list()
        for src in src_img:
            eggs = re.split(r'\, ', src.xpath('@srcset').get())[3]
            spam.append(re.split(r' ', eggs)[0])
        item.add_value('photos', spam)
        return item.load_item()
