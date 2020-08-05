from itemadapter import ItemAdapter
from pymongo import MongoClient


class HabrParsePipeline:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.db = client['habr_parse']

    def process_item(self, item, spider):
        return item

    def save_to_mongodb(self, item, spider):
        self.collection = self.db[spider.name]
        self.collection.insert_one(item)
        return item
