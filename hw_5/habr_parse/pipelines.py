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
        if 'author_fullname' not in item.fields.keys():
            self.collection = self.db[spider.name]
        else:
            self.collection = self.db['author_info']
        self.collection.insert_one(item)
        return item
