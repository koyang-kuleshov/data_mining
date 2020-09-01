"""Источник: https://www.zillow.com

при старте паука передается список локаций которые необходимо обойти.

Необходимо обойти все объявления и собрать след структуру данных:

price - цена указанная в объявлении
address - поле адреса указанное в объвлении
photos - все фотографии из объявления в максимальном разрешении
( необходимо скачать и сохранить на компьютере)
"""

import scrapy


class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['http://www.zillow.com/']

    def parse(self, response):
        pass
