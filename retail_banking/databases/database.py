import pymongo
from .. import config
import random
class DB:
    def __init__(self):

        self._url=config.config.dburl

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

    def find(self,collectionName,filter,no_of_data="single"):
        collection= self.db[collectionName]
        if no_of_data == "many":
            return collection.find_many(filter)
        elif no_of_data=="single":
            return collection.find_one(filter)
        else:
            #for all ...
            return collection.find()
 

    def update(self,collectionName,selectionCriteria,updateData):
        collection= self.db[collectionName]
        res=collection.update_one(selectionCriteria,updateData)
        return res

    def delete(self,collectionName,filter):
        collection= self.db[collectionName]
        res=collection.find_one_and_delete(filter)
        return res



    def randIdgen(self,first):
        temp=first
        for _ in range(8):
            temp+=str(random.randint(0,9))

        return temp
