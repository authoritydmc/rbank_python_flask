from retail_banking.DATABASES import database
import random

DB=database.DB()

collectionSSN="customerSSN"
collectionAccount="customerAccount"




def registerSSN(data):
    clctn=DB.getdb()[collectionSSN]

    clctn.create_index('ssn_id',unique=True)
    try:
        DB.insertCollection(collectionSSN,data)
        return True,None
    except Exception as e:
        print("exception ....",e)
        if 'duplicate key error' in str(e):
            return False,f":A Customer with  SSN_ID={data['ssn_id']} already exist"
        return False,str(e)


def findSSN(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionSSN,filter)
    return res
def findAccount(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionAccount,filter)
    return res

def findSSN_all(filter={}):
    return DB.find(collectionSSN,filter,"all")

def findAcc_all(filter={}):
    return DB.find(collectionAccount,filter,"all")

def updateSSN(data):
    print("update using these values ",data)
    # ssn_id=data['ssn_id']
    # data.pop('ssn_id',None)
    updatedict={"$set":data}
    print(updatedict)
    try:
        res=DB.update(collectionSSN,{'ssn_id':data['ssn_id']},updatedict)
        if res:
            return True,None
        else:
            return False,"Can not Update to Database"
    except Exception as e:
        return False,"Error Occured : "+str(e)

def deleteSSN(filter):
    return DB.delete(collectionSSN,filter)


def createAccount(data):
    clctn=DB.getdb()[collectionAccount]

    clctn.create_index('cust_acc_id',unique=True)
    try:
        DB.insertCollection(collectionAccount,data)
        return True,None
    except Exception as e:
        print("exception ....",e)
        if 'duplicate key error' in str(e):
            return False,f":A Customer with  Account no ={data['cust_acc_id']} already exist"
        return False,str(e)


def getautoAccountid():
    cust_id=""
    while True:
        cust_id=DB.randIdgen("1")
        filter = {'cust_acc_id': cust_id}
        if not findAccount(filter):
            break
    return cust_id

def getautoSSNid():
    ssn_id=""
    while True:
        ssn_id=DB.randIdgen("5")
        filter = {'ssn_id': ssn_id}
        if not findSSN(filter):
            break
    return ssn_id

def deleteAccount(filter):
    return DB.delete(collectionAccount,filter)


