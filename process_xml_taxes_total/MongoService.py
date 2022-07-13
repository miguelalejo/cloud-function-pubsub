import pymongo
from pymongo.errors import BulkWriteError,DuplicateKeyError

class MongoServiceConector:
    def __init__(self, uri, user, password):
        self.client = pymongo.MongoClient("mongodb+srv://{user}:{password}@{uri}".format(user=user,password=password,uri=uri))


    def close(self):
        self.driver.close()
     
    def find(self,bd_name,collecion,query,projection = {}):
        collection = self.client[bd_name][collecion]
        documents = collection.find(query,projection)
        return documents