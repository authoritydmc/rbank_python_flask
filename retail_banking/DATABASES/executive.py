from retail_banking.DATABASES import database

DB=database.DB()

collectionName="executive"




def insertCustomerDetail(data):
    clctn=DB.getdb()[collectionName]

    clctn.create_index('ssn_id',unique=True)
    try:
        DB.insertCollection(collectionName,data)
        return True,None
    except Exception as e:
        print("exception ....",e)
        if 'duplicate key error' in str(e):
            return False,"SSN ID should be unique"
            
        return False,str(e)


    