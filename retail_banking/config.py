import os
class config:
    dburl=os.environ.get('mongourl',None)
    
