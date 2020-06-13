import pymongo
from retail_banking.config import config
class DB:
    def __init__(self):

        self._url=config.dburl

        if self._url==None:
            #change this url to your mongodb database for testing ....
            self._url="mongodb+srv://DBUSER:pass123@cluster0-l63ew.mongodb.net/retail_bank?retryWrites=true&w=majority"
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



