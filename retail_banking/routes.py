# import this line in every new module you create this will give access to app with required library
# for more info check __init__.py file
from retail_banking import *
import time
from flask import redirect, render_template, url_for, json, flash

import hashlib

from retail_banking.DATABASES import customerdb as cdb
from retail_banking.DATABASES import executive as edb


@app.route('/')
def home():
    return render_template('home.html', home=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        # show when default this url is loaded ..
        return render_template('login.html', login=True)
    else:
        # after user submit his username and password we get to this...
        username = request.form.get('uid', "userNotFound")
        password = request.form.get('psw', "passwordNotfound")
        passhax = hashlib.sha256(password.encode()).hexdigest()

        filter = {'ssn_id': username, 'pass': passhax}

        result = edb.find(filter)

        if result == None:
            flash("Wrong UserName or Password retry","danger")
            return redirect(url_for('login'))
        else:
            flash("Successfully Logged in","success")
            return redirect(url_for('home'))



@app.route('/registerExecutive', methods=['get', 'post'])
def registerExecutive():

    if request.method == "GET":
        return render_template('registerExecutive.html',registerExecutive=True)

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['email'] = request.form.get('email')
    regdata['pass'] = hashlib.sha256(
        request.form.get('psw').encode()).hexdigest()

    result, err = edb.register(regdata)

    if result:
        flash("Executive Registered Successfully ...    Login Now")
        return redirect(url_for('login'))
    else:
        flash("Failed to Register :"+err)
        return redirect(url_for('registerExecutive'))
    return redirect('login.html')


@app.route('/registerCustomer', methods=['get', 'post'])
def registerCustomer():

    if request.method == "GET":
        return render_template('registerCustomer.html')

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['age'] = request.form.get('age')
    regdata['state'] = request.form.get('state')
    regdata['city '] = request.form.get('city')

    print(regdata)  # Simulating database insertion

    jsondata = json.dumps(regdata)
    result, err = cdb.registerSSN(regdata)

    if result:
        flash("Customer Registered Successfully"+jsondata)
    else:
        flash("Failed to Register Customer "+err)

    return render_template('registerCustomer.html')
