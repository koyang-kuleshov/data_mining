from itemadapter import ItemAdapter
from pymongo import MongoClient


class HabrParsePipeline:

    def process_item(self, item, spider):
        return item


class HabrSaveToMongoDBPipeline:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017')
        self.db = client['habr_parse']

    def process_item(self, item, spider):
        self.collection = self.db[f'{type(item).__name__}s']
        self.collection.insert_one(item)
        return item
