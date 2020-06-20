from . import database
import time
import random
import logging
from .. import utility
try:
    DB=database.DB()
except Exception as e:
    print("*"*80)
    logging.error("Exception Occured :Possible Fix: Connect to Internet first ")
    print("*"*80)
    logging.error(e)

    exit()

collectionTransaction="transactions"

def generateTransactionID():
    return str(time.time_ns())[-11:]+str(random.randint(1000,9999))


def recordTransaction(data):
    clctn=DB.getdb()[collectionTransaction]
    clctn.create_index('trans_id',unique=True)
    try:
        data['trans_id']=generateTransactionID()
        data['transaction_time']=utility.getTime()
        data['epoch_time']=utility.getTimeUTC()
        DB.insertCollection(collectionTransaction,data)
        return True,"NO error"
    except Exception as e:
        logging.error("ERROR _TRANSACTION "+str(e))    
        return False,e


def findTransaction(filter,type="single"):
    ##filter will be used to find something ... 
    return DB.find(collectionTransaction,filter,type)

def solidTransaction(dataS,dataD):
    transfer_trans_id=generateTransactionID()
    dataS['transfer_trans_id']=transfer_trans_id
    dataD['transfer_trans_id']=transfer_trans_id
    res1,err=recordTransaction(dataS)
    res2,err=recordTransaction(dataD)
    if res1==False or res2==False:
        return False,"Failed to Commit Transaction "
    else:
        return True,"All SuccessFul"

