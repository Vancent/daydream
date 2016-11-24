# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class GpDaydreamPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = "gameinfo"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('GP_MONGO_DB', 'gameinfo')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
#        self.db = self.client[self.mongo_db]
        self.game_tbl = self.client[self.mongo_db][self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = "gameinfo"
        spec = {}
        spec["Date"] = item["Date"]
        spec["title"] = item["title"]
        self.game_tbl.update(spec, item, upsert=True)
        return item