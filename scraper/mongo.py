import pymongo
from pymongo import MongoClient

from scraper.dtos import DataSet


class MongoOperator:

    def __init__(self):
        self.client = MongoClient(
            'localhost',
            username='mongo',
            password='mongo',
            port=27017
        )
        self.database = self.client.get_database('cryptomonitor')
        self.collection = self.database.get_collection('records')

    def add_record(self, data_set: DataSet):
        self.collection.insert_one(data_set.convert_to_dict())

    def get_latest_record(self):
        return self.collection.find().sort("timestamp", pymongo.DESCENDING).limit(1)[0]
