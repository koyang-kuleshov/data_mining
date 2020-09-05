"""Источник: https://www.zillow.com

при старте паука передается список локаций которые необходимо обойти.

Необходимо обойти все объявления и собрать след структуру данных:

price - цена указанная в объявлении
address - поле адреса указанное в объвлении
photos - все фотографии из объявления в максимальном разрешении
( необходимо скачать и сохранить на компьютере)
"""

import scrapy
from scrapy.loader import ItemLoader

from zillowspider.items import ZillowspiderItem


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/']

    def __init__(self, region: str, *args, **kwargs):
        self.start_urls = [f'{self.start_urls[0]}{region}/']
        super().__init__(*args, **kwargs)

    def parse(self, response):
        real_estate = response.xpath('//a[@class="list-card-link"]/@href')
        for url in real_estate:
            yield response.follow(
                url,
                callback=self.get_real_estate_data
            )
        pages = response.xpath('//nav[@role="navigation"]/ul/li/a/@href')
        for page in pages:
            # yield response.follow(page, callback=self.parse)
            # print(page)
            pass

    def get_real_estate_data(self, response):
        item = ItemLoader(ZillowspiderItem(), response)
        item.add_value('url', response.url)
        item.add_xpath('address',
                       '//head/title/text()'
                       )
        item.add_xpath('price', '//h3[contains(@class, "ds-price")]//span[@class="ds-value"]/text()')
        return item.load_item()
