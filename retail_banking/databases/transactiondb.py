from . import database
import time
import random
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
        data['trans_id']=str(time.time_ns())[-5:]+str(random.randint(0,10000))
        DB.insertCollection(collectionTransaction,data)
        return True,None
    except Exception as e:
        print("exception ....",e)     
        return e


def findTransaction(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionTransaction,filter)
    return res
