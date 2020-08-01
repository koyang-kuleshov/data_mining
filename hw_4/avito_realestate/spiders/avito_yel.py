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
        'ads_title': '//h1/span',
        'ads_price': '//span[contains(@itemprop, "price")]',
        'ads_params': '//ul.item-params-list/li'
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
            yield self.get_ads_params(url)

    def get_ads_params(self, response):
        print(response.xpath(self.selectors['ads_title']))
        print('*' * 40)

    def save_to_db(self, data):
        self.collection.insert_one(data)
