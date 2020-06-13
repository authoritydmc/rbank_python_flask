import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd45g45iu3y4893n545rc398r2r28r'

    MONGODB_URL = "mongodb+srv://predator:pred123@cluster0-cgsrf.mongodb.net/retail_banking?retryWrites=true&w=majority"