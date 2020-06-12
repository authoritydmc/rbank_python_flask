#import this line in every new module you create this will give access to app with required library
#for more info check __init__.py file
from retail_banking import *
from retail_banking import database

import hashlib

@app.route('/')
def home():
    return render_template('home.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        #show when default this url is loaded ..
        return render_template('login.html',a="getr")
    else:
        # after user submit his username and password we get to this...
        username=request.form.get('uid',"userNotFound")
        password=request.form.get('psw',"passwordNotfound")
        passhax=hashlib.sha256(password.encode()).hexdigest()
        
        db=database.DB().getdb()
        # 

        cluster=db["login"]
        doc={"user":username,"pass":passhax}
        cluster.insert_one(doc)

        return render_template('login.html',a="post--"+username+passhax)







