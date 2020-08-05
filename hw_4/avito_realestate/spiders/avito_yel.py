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
    start_urls = ['http://avito.ru/elan/kvartiry/prodam-ASgBAgICAUSSA8YQ']

    pagination = '//div[contains(@data-marker, "pagination-button")]/span/text()'
    ads_url = '//h3[contains(@data-marker, "item-title")]/a/@href'

    selectors = {
        'ads_title': '//h1/span/text()',
        'ads_price': '//span[contains(@itemprop, "price")]/text()',
    }

    params = '//ul[@class="item-params-list"]/li'

    pages = set()

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['yelan_realestate']
        self.collection = db['apparts']

    def parse(self, response):
        for url in response.xpath(self.pagination):
            try:
                page = int(url.extract())
            except Exception:
                continue
            else:
                if page != 1:
                    for url in response.xpath(self.ads_url):
                        yield response.follow(url, callback=self.get_ads_params)
                    yield response.follow(f'{self.start_urls[0]}?p={page}',
                                          callback=self.parse)
                else:
                    continue

    def get_ads_params(self, response):
        data = {
            'url': response.url,
        }
        for key, value in self.selectors.items():
            data[key] = response.xpath(value).extract()
        span = response.xpath(f'{self.params}/span/text()').extract()
        li = [i for i in response.xpath(f'{self.params}/text()').extract()
              if i != ' ']
        data['params'] = list()
        for key, value in zip(span, li):
            key = key.rstrip()
            data['params'].append(
                {
                    key[:len(key) - 1]: value.rstrip()
                }
            )

        data['ads_title'] = data['ads_title'][0]
        if data['ads_price'] == 'Не указана':
            data['ads_price'] == 0
        else:
            data['ads_price'] = int(data['ads_price'][0].replace(' ', ''))
        self.save_to_db(data)

    def save_to_db(self, data):
        self.collection.insert_one(data)
