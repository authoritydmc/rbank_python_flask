from . import database
import random
import logging
DB=database.DB()

collectionName="executive"




def register(data):
    clctn=DB.getdb()[collectionName]

    clctn.create_index('ssn_id',unique=True)
    try:
        DB.insertCollection(collectionName,data)
        return True,None
    except Exception as e:
        logging.error(e)
        if 'duplicate key error' in str(e):
            return False,"Executive already Registered"
            
        return False,str(e)


def find(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionName,filter)
    return res

def getautoSSNid():
    ssn_id=""
    while True:
        ssn_id=DB.randIdgen("9")
        filter = {'ssn_id': ssn_id}
        if not find(filter):
            break
    return ssn_id