import scrapy


class AvitoYelSpider(scrapy.Spider):
    name = 'avito_yel'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/elan/kvartiry']

    def parse(self, response):
        pass
