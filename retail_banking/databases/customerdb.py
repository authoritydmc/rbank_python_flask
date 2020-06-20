from . import database
import random
import logging
from . import transactiondb  as tdb

    

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
        logging.error(e)
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
def findAcc_all_of_ssnid(ssn_id):
    return DB.find(collectionAccount,{"ssn_id":ssn_id},"many")

def updateSSN(data):
    # ssn_id=data['ssn_id']
    # data.pop('ssn_id',None)
    updatedict={"$set":data}
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
        logging.error(e)
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

def make_transaction(data,type):
    updatedict={}
    #all the required Data
    trans_data=data

    updatedict["$inc"]={"balance":float(data['amount'])} #negate the amount so decrease
   
    trans_data['balance']=float(trans_data['balance'])+float(trans_data['amount'])
    
    

    try:
        res=DB.update(collectionAccount,{'cust_acc_id':data['cust_acc_id']},updatedict)
        res_rec_tr,err_rec_trans=tdb.recordTransaction(trans_data)
        
        if res:
            return True,"No error @make_transaction"
        else:
            return False,"Can not Record this Transaction"
    except Exception as e:
        return False,str(e)

def deposit(data):
    try:
        if float(data['amount'])<1:
            return False,"Minimum amount should be Rs 1 to deposit"
    except :
        return False,"Occur occured ,while making Depositing the money.."
    return make_transaction(data,"credit")
    
def withdraw(data):
    try:
        if float(data['balance'])+float(data['amount']) <0:
            return False,"Not Sufficient Balance in account to withdraw"
    except :
        return False,"error occured while withdrawing money"
    return make_transaction(data,"debit")


def findAllTransaction(cust_id):
    return tdb.findTransaction({"cust_acc_id":cust_id},"many")

def findTransaction(filter):
    res=tdb.findTransaction(filter)
    return res

def transfer(source_acc,dest_acc,amount,exe_sid):
    if source_acc==dest_acc:
        return False,"Error: Source Account and Destination Account is Same"
    res1=findAccount({'cust_acc_id':source_acc})
    if res1==None:
        return False,"Error: Couldn't Find Source Account"

    if float(amount)>float(res1['balance']):
        return False,"Error: Insufficient Balance in Source Account"
    
    res2=findAccount({'cust_acc_id':dest_acc})
    if res2==None:
        return False,"Error: Couldn't Find Destination Account"


    #all sanity check passed ..Now make Transfer

    dataS={}
    dataD={}

    transfer_id=tdb.generateTransactionID()

    dataS['cust_acc_id']=source_acc
    dataS['transaction_type']="debit"
    #negative amount
    dataS['amount']="-"+str(amount)
    dataS['remark']="Transferred to "+str(dest_acc)
    dataS['executive_ssn_id']=exe_sid
    dataS['balance']=res1['balance']
    dataS['transfer_id']=transfer_id



    dataD['transfer_id']=transfer_id
    dataD['cust_acc_id']=dest_acc
    dataD['transaction_type']="credit"
    dataD['amount']=str(amount)
    dataD['remark']="Received From "+str(source_acc)
    dataD['executive_ssn_id']=exe_sid
    dataD['balance']=res2['balance']
    res1,err1=withdraw(dataS)
    result2,err2=deposit(dataD)

    if res1==True and res2==True:
        return True,"No error @ make transfer"
    elif res1==False:
        return res1,err1
    else:
        return result2,err2