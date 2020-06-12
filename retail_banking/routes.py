#import this line in every new module you create this will give access to app with required library
#for more info check __init__.py file
from retail_banking import *


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
        return render_template('login.html',a="post--"+username+"-"+password+"--"+hashlib.sha256(password.encode()).hexdigest())







