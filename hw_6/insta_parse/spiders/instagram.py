"""
Источник https://www.instagram.com
Создать паука который при запуске получает список имен идентификаторов
пользователей,

Обходит ленту постов пользователя,
собирает монго бд со след структурой:

user_name - имя пользвоателя
user_id - айдишник пользователя
post_photos - все фото из поста
post_pub_date - дата публикации поста
like_count - количество лайков поста
Внимание, фото надо скачивать и сохранять, в бд надо хранить как ссылку на фото
так и путь куда сохранено фото
"""
import scrapy
from scrapy.loader import ItemLoader
import re
import json


from insta_parse.items import InstaParseItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    __login_url = 'https://www.instagram.com/accounts/login/ajax/'

    def __init__(self, login: str, passwd: str, parse_users: list,
                 *args, **kwargs):
        self.login = login
        self.passwd = passwd
        self.parse_users = parse_users
        super().__init__(*args, **kwargs)

    def parse(self, response):
        token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.__login_url,
            method='POST',
            callback=self.im_login,
            formdata={
                'username': self.login,
                'enc_password': self.passwd,
            },
            headers={
                'X-CSRFToken': token
            }
        )

    def im_login(self, response):
        data = response.json()
        if data['authenticated']:
            for user_name in self.parse_users:
                yield response.follow(f'/{user_name}',
                                      callback=self.get_user_data,
                                      cb_kwargs={'user_name': user_name}
                                      )

    def get_user_data(self, response, user_name):
        item = ItemLoader(InstaParseItem(), response)
        item.add_value('user_name', user_name)
        item.add_value('user_id', self.fetch_user_id(
            response.text,
            user_name
            )
        )
        return item.load_item()

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        token = matched.split(':').pop().replace(r'"', '')
        return token

    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        pattern = r'{\"id\":\"\d+\",\"username\":\"' + username + '\"}'
        matched = re.search(
            pattern,
            text
        ).group()
        return json.loads(matched).get('id')
