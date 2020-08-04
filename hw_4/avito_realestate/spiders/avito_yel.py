"""
обойти пагинацию
извлечь и обойти все страницы объявлений

из самого объявления извлечь следующие данные:
Заголовок объявления
Url объявления
стоимость(если указана)
список характеристик квартиры ( которые сразу под фото)
"""
import scrapy
from pymongo import MongoClient


class AvitoYelSpider(scrapy.Spider):
    name = 'avito_yel'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/elan/kvartiry']
    selectors = {
        'pagination': '//div[contains(@data-marker, "pagination-button")]/span',
        'ads_url': '//h3[contains(@data-marker, "item-title")]/a/@href',
        'ads_title': '//h1/span/text()',
        'ads_price': '//span[contains(@itemprop, "price")]/text()',
        'ads_params_li': '//ul.item-params-list/li/text()',
        'ads_params_span': '//ul.item-params-list/li/span/text()'
    }

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['yelan_realestate']
        self.collection = db['kvartiry']

    def parse(self, response):
        # for url in response.xpath(self.selectors['pagination']):
        #     print(url)
        print('*' * 40)

        for url in response.xpath(self.selectors['ads_url']):
            yield response.follow(url, callback=self.get_ads_params)

    def get_ads_params(self, response):
        # print(response.xpath(self.selectors['ads_title']).extract())
        # print(response.xpath(self.selectors['ads_price']).extract_first())
        print(response.xpath(self.selectors['ads_params_span']).extract())
        # for param in response.xpath(self.selectors['ads_params_li']):
            # li = param.extract()
            # print(param)
            # print(f'{li}', param.xpath('span/text()').extract())

        print('*' * 40)

    def save_to_db(self, data):
        self.collection.insert_one(data)
