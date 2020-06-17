from retail_banking.DATABASES import database,customerdb,transactiondb,executive
from retail_banking import app,routes

# print('__file__={0:<35} |\n__name__={1:<20} |\n__package__={2:<20}'.format(__file__,__name__,str(__package__)))
if __name__=="__main__":    
    app.run(host='0.0.0.0',debug=True)

