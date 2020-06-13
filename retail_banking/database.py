import pymongo
from config import Config

class DB:
    def __init__(self):

        self._url=Config.MONGODB_URL

        if self._url==None:
            #change this url to your mongodb database for testing ....
            # self._url="mongodb+srv://DBUSER:pass123@cluster0-l63ew.mongodb.net/retail_bank?retryWrites=true&w=majority"
            self._url="mongodb+srv://predator:pred123@cluster0-cgsrf.mongodb.net/retail_banking?retryWrites=true&w=majority"
        self._client=pymongo.MongoClient(self._url)

        self.db=self._client['retail_banking']

    def getdb(self):
        return self.db


