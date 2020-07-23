"""
- images (список изображений в теле статьи)
- text (текст статьи)
"""
from bs4 import BeautifulSoup as bs
import requests
import json
from random import randint

from pymongo import MongoClient

DOMAIN = 'https://geekbrains.ru'
URL = 'https://geekbrains.ru/posts'


class GbBlogParse:

    def __init__(self):
        self.posts_urls = set()
        self.pagination_urls = set()
        self.__done_urls = set()
        client = MongoClient('mongodb://localhost:27017')
        db = client['gb_blog']
        self.collection = db['posts']

    def get_page_soup(self, url):
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        return soup

    def run(self, url=None):
        url = url or URL
        soup = self.get_page_soup(url)
        self.pagination_urls.update(self.get_pagination(soup))
        spam = self.get_posts_urls(soup)
        self.posts_urls.update(spam)
        self.get_post_data(spam)

        for url in tuple(self.pagination_urls):
            if url not in self.__done_urls:
                self.__done_urls.add(url)
                self.run(url)

    def get_pagination(self, soup):
        ul = soup.find('ul', attrs={'class': 'gb__pagination'})
        a_list = [f'{DOMAIN}{a.get("href")}'
                  for a in ul.find_all('a') if a.get("href")]
        return a_list

    def get_posts_urls(self, soup):
        posts_wrap = soup.find('div', attrs={'class': 'post-items-wrapper'})
        a_list = [f'{DOMAIN}{a.get("href")}'
                  for a in posts_wrap.find_all('a',
                                               attrs={
                                                   'class': 'post-item__title'
                                               }
                                               )
                  ]
        return a_list

    def get_post_data(self, urls):
        for url in urls:
            data = {}
            eggs = self.get_page_soup(url)
            data['title'] = eggs.head.title.string
            data['post_url'] = url
            author = eggs.find(itemprop='author')
            data['writer_name'] = author.string
            data['writer_url'] = f'{DOMAIN}{author.parent.attrs["href"]}'
            tags = eggs.find_all(attrs={'class': 'small'})
            data['tags_urls'] = [f'{DOMAIN}{tag.get("href")}' for tag in tags
                                 if tag.get("href")]
            images = eggs.find_all(itemprop='articleBody')
            data['images'] = [f'{image.img.get("src")}'
                              for image in images if image.img.get("src")]
            data['text'] = eggs.find(itemprop='articleBody').string

            self.save_to_db(data)

    def save_to_db(self, data):
        self.collection.insert_one(data)


if __name__ == '__main__':
    parser = GbBlogParse()
    parser.run()
