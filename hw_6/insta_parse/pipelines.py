# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class InstaParsePipeline:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.db = client['insta_parse']

    def process_item(self, item, spider):
        self.collection = self.db[spider.name]
        self.collection.insert_one(item)
        return item


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        pass
        return item

    def item_completed(self, results, item, info):
        pass
        return item
