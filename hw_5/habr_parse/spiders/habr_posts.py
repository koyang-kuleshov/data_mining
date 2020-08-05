import scrapy
from scrapy.loader import ItemLoader
from habr_parse.items import HabrParseItem, HabrAuthorItem
from habr_parse.spiders.author_info import AuthorInfoSpider


class HabrPostsSpider(scrapy.Spider):
    name = 'habr_posts'
    allowed_domains = ['habr.com']
    start_urls = ['http://habr.com/ru/top/']

    nav_pages = '//ul[@id="nav-pagess"]/li/a/@href'
    posts = '//article/h2/a/@href'

    post_data = {
        'title': '//h1/span/text()',
        'images': '//article//img/@src',
        'comments': '//h2/span[@id="comments_count"]/text()',
        'author_name': '//div[@class="user-info__links"]/a/text()',
        'author_url': '//div[@class="user-info__links"]/a/@href',
    }

    def parse(self, response):
        for url in response.xpath(self.nav_pages):
            yield response.follow(url, callback=self.parse)

        for url in response.xpath(self.posts):
            yield response.follow(url, callback=self.get_post_data)

    def get_post_data(self, response):
        item = ItemLoader(HabrParseItem(), response)
        for key, value in self.post_data.items():
            item.add_xpath(key, value)
        item.add_value('post_url', response.url)

        yield AuthorInfoSpider(item.get_value('author_url'))
        yield item.load_item()
