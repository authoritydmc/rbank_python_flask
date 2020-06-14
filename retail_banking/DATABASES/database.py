import pymongo
from retail_banking.config import config
class DB:
    def __init__(self):

        self._url=config.dburl

        if self._url==None:
            #change this url to your mongodb database for testing ....
            from retail_banking import config_internal
            self._url=config_internal.dburl
        self._client=pymongo.MongoClient(self._url)

        self.db=self._client.retail_bank

    def getdb(self):
        return self.db

    def insertCollection(self,collectionName,datainJson):
       collection= self.db[collectionName]
       collection.insert_one(datainJson)
       print("data inserted successfully ",datainJson)
    
    def RegisterUser(self):
        pass

    def find(self,collectionName,filter):
        collection= self.db[collectionName]
        res=collection.find_one(filter)
        return res

    def update(self,collectionName,selectionCriteria,updateData):
        collection= self.db[collectionName]
        res=collection.update_one(selectionCriteria,updateData)
        return res




