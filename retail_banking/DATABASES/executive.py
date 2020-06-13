from retail_banking.DATABASES import database

DB=database.DB()

collectionName="executive"




def register(data):
    clctn=DB.getdb()[collectionName]

    clctn.create_index('ssn_id',unique=True)
    try:
        DB.insertCollection(collectionName,data)
        return True,None
    except Exception as e:
        print("exception ....",e)
        if 'duplicate key error' in str(e):
            return False,"Executive already Registered"
            
        return False,str(e)


def find(filter):
    ##filter will be used to find something ... 
    res=DB.find(collectionName,filter)
    return res