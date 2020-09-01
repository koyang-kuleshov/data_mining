import scrapy
from scrapy.loader import ItemLoader
from habr_parse.items import HabrParseItem, HabrAuthorItem


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
        'author_url': '//div[@class="user-info__links"]/a[contains(@class, "user-info__nickname")]/@href'
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
            if key == 'author_url':
                url = response.xpath(value)[0]
                yield response.follow(url, callback=self.get_author_info)

        item.add_value('post_url', response.url)
        yield item.load_item()

    def get_author_info(self, response):
        selectors = {
            'author_fullname': '//h1/a[contains(\
                @class, "user-info__fullname")]/text()',
            'author_nickname': '//h1/a[contains(\
                @class, "user-info__nickname")]/text()',
            'author_info': '//div[contains(@class, "profile-section__about-text")]//text()',
            'author_contact': '//ul[contains(@class, "defination-list")]/li/span//text()',
        }

        item = ItemLoader(HabrAuthorItem(), response)
        for key, value in selectors.items():
            item.add_xpath(key, value)
        item.add_value('author_url', response.url)

        author_posts = f'{response.url}posts/'
        yield response.follow(author_posts, callback=self.parse)
        yield item.load_item()
