from . import database
import time
import random
import logging
DB=database.DB()

collectionTransaction="transactions"

def generateTransactionID():
    return str(time.time_ns())[-7:]+str(random.randint(1000,9999))


def recordTransaction(data):
    clctn=DB.getdb()[collectionTransaction]
    print("recording transaction--->",data)
    clctn.create_index('trans_id',unique=True)
    try:
        data['trans_id']=generateTransactionID()
        data['transaction_time']=time.strftime(
        "%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())
        DB.insertCollection(collectionTransaction,data)
        return True,"NO error"
    except Exception as e:
        # print("exception ....",e) 
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

