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
            return False,"Already Registered"
            
        return False,str(e)


def find(filter):
    res=DB.find(collectionName,filter)
    return res