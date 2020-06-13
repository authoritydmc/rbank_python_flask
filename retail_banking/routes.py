#import this line in every new module you create this will give access to app with required library
#for more info check __init__.py file
from retail_banking import *
import time
from flask import redirect,render_template,url_for,json,flash

import hashlib

from retail_banking.DATABASES import customerdb as cdb



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
        


        return render_template('login.html',a="post--"+username+passhax)




@app.route('/register', methods=['get', 'post'])
def register():

    if request.method == "GET":
        return render_template('register.html')
    
    regdata={}

    regdata['ssn_id']=     request.form.get('ssn')
    regdata['name']=    request.form.get('name')
    regdata['age']=  request.form.get('age')
    regdata['state']=     request.form.get('state')
    regdata['city ']=    request.form.get('city')

    print(regdata)# Simulating database insertion

    jsondata=json.dumps(regdata)
    result,err=cdb.insertCustomerDetail(regdata)

    if result:
        flash("Customer Registered Successfully"+jsondata)
    else:
        flash("Failed to Register Customer "+err)

    return render_template('register.html')
    
    




