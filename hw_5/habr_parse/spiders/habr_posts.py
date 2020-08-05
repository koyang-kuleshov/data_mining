"""
Источник https://habr.com/
****задача: Обойти ленту статей, зайти в каждую статью и извлеч следующие данные:

заголовок
сслыки на все изображения которые есть в статье
количество комментариев
информация о авторе ссылка и имя
внимание необходимо использовать Item и ItemLoader

стурктура item для поста следующая:
- title
- images
- comments
- autor_name
- autor_url
- post_url

получив данные о авторе сохранить данные о авторе, и вам необходмо зайти на его
страницу и обойти все его статьи.

таким образом у вас будет item для авторов, структуру необходимо спроектировать
вам, необходимо получить всю информацию в блоке ИНФОРМАЦИЯ, Имя, url, nicname и
всю возможную контактную информацию
полученые айтемы необходимо сохранять в базе данных MONGO в отдельных коллекциях для статей, и авторов.
"""
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

        yield item.load_item()
