from . import database
import random
import logging
DB=database.DB()
from .. import utility
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


def updateDetail(filter,data):
    # ssn_id=data['ssn_id']
    # data.pop('ssn_id',None)
    updatedict={"$set":data}
    try:
        res=DB.update(collectionName,filter,updatedict)
        if res:
            return True,"Updated Successfully"
        else:
            return False,"Can not Update to Database update@edb"
    except Exception as e:
        return False,"Error Occured : "+str(e)
def update_logintime(ssn_id):
    try:
        ct=utility.getTime()
        f=  {"ssn_id":str(ssn_id)}
        print("LAST_LOGIN",updateDetail(f,{"last_login":ct}))
    except Exception as e:
        print("ERROR @ EDB 57",e)


