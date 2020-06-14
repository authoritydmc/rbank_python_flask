from retail_banking.DATABASES import database

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

def findSSN_all(filter={}):
    return DB.find(collectionSSN,filter,"all")

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