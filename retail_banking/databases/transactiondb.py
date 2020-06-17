from . import database
import time
import random
import logging
DB=database.DB()

collectionTransaction="transactions"

def isworking(t="it is working"):
    print('__file__={0:<35} |\n__name__={1:<20} |\n__package__={2:<20}'.format(__file__,__name__,str(__package__)))

    return "yes it is "


def recordTransaction(data):
    clctn=DB.getdb()[collectionTransaction]
    print("recording transaction--->",data)
    clctn.create_index('trans_id',unique=True)
    try:
        data['trans_id']=str(time.time_ns())[-6:]+str(random.randint(1000,9999))
        DB.insertCollection(collectionTransaction,data)
        return True,None
    except Exception as e:
        # print("exception ....",e) 
        logging.error("ERROR _TRANSACTION"+str(e))    
        return e


def findTransaction(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionTransaction,filter)
    return res
