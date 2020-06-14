# import this line in every new module you create this will give access to app with required library
# for more info check __init__.py file
from retail_banking import *
<<<<<<< HEAD
from time import gmtime, strftime
=======

from time import gmtime,strftime
>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
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
    if isLoggedin():
        #redirect in case user is already logged In
        return(redirect(url_for('home')))
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
            flash("Wrong UserName or Password retry", "danger")
            return redirect(url_for('login'))
        else:
<<<<<<< HEAD
            flash("Successfully Logged in", "success")

            # setup session~~~

            session['ssn_id'] = username
            session['logged_in'] = True

            # end setup

=======
            ###setup session~~~
            session_login(username)
            if isLoggedin():
                flash("Successfully Logged in","success")
            else:
                flash("Can not setup session ","danger")
            ##end setup

>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
            return redirect(url_for('home'))


@app.route('/registerExecutive', methods=['get', 'post'])
def registerExecutive():

    if request.method == "GET":
        return render_template('registerExecutive.html', registerExecutive=True)

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['email'] = request.form.get('email')
    regdata['pass'] = hashlib.sha256(
        request.form.get('psw').encode()).hexdigest()
<<<<<<< HEAD
    regdata['creation_time'] = time.strftime(
        "%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())
    result, err = edb.register(regdata)

    if result:
        flash("Executive Registered Successfully ...    Login Now", "success")
        return redirect(url_for('login'))
    else:
        flash("Failed to Register :"+err, "danger")
=======

    regdata['creation_time']=time.strftime("%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())
    result, err = edb.register(regdata)

    if result:  
        flash("Executive Registered Successfully ...    Login Now","success")
        return redirect(url_for('login'))
    else:
        flash("Failed to Register :"+err,"danger")
>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
        return redirect(url_for('registerExecutive'))
      
    return redirect('login.html')


@app.route('/registerCustomer', methods=['get', 'post'])
def registerCustomer():
    
    if not isLoggedin():
        #if there is no one loggedIn disallow this route
        flash("Login first to access it ","danger")
        return redirect(url_for('home'))


    if request.method == "GET":
        return render_template('registerCustomer.html')

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['age'] = request.form.get('age')
    regdata['state'] = request.form.get('state')
    regdata['city '] = request.form.get('city')
    regdata['address']=request.form.get('address')

    print(regdata)  # Simulating database insertion

    jsondata = json.dumps(regdata)
    result, err = cdb.registerSSN(regdata)

    if result:
        flash("Customer Registered Successfully"+jsondata)
    else:
        flash("Failed to Register Customer "+err)

    return render_template('registerCustomer.html')


<<<<<<< HEAD
# Search customer by SSN ID to delete or update details
@app.route('/searchCustomer', methods=['get', 'post'])
def searchCustomer():
    if not session['logged_in']:
=======
@app.route('/logout')
def logout():
    if isLoggedin():
        #log out by invalidating session
        session_logout()
        flash("You have been successfully logged out","success")
    else:
        flash("You are already Logged out..","success")


    return redirect(url_for('home'))

###Utility Function

def session_logout():
    session.pop('ssn_id',None)
def session_login(ssn_val):
    session['ssn_id']=ssn_val
def isLoggedin():
    if 'ssn_id' in session.keys():
        return True
    else :
        return False

# Search customer by SSN ID to delete or update details
@app.route('/searchCustomer', methods=['get', 'post'])
def searchCustomer():
    if not isLoggedin():
>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
        return redirect(url_for('login'))

    if request.method == "GET":
        return render_template('searchCustomer.html')

    filter = {'ssn_id': request.form.get('ssn_id')}

    # Retrieving details of customer
    result = cdb.findSSN(filter)
<<<<<<< HEAD

    if result:
        flash("Customer Found. Now you can update the details.", "success")
        return render_template('updateCustomer.html')
=======
    print(result)

    if result:
            ###creating argument that will be passed ...
        args={}
        args['ssn_id']=result['ssn_id']
        args['oldAge']=result['age']
        args['oldAddress']=result['address']
        args['oldName']=result['name']

        flash("Customer Found. Now you can update the details.", "success")
        return render_template('updateCustomer.html',**args)
>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
    else:
        flash("Unable to find customer. Try again by entering valid SSN ID.", "danger")
        return redirect(url_for('searchCustomer'))

@app.route('/updateCustomer', methods=['get', 'post', 'update'])
def updateCustomer():

<<<<<<< HEAD
    if not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == "GET":
        return redirect('searchCustomer')

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


@app.route('/logout')
def logout():

    if 'ssn_id' in session.keys() and session['logged_in'] == True:
        # log out by invalidating session

        session.pop('ssn_id', None)

        session['logged_in'] = False

        flash("You have been successfully logged out", "success")
    return redirect(url_for('home'))
=======
    if not isLoggedin():
        return redirect(url_for('login'))

    if request.method == "GET":
        return redirect(url_for('searchCustomer'))

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn_id')
    regdata['name'] = request.form.get('newName')
    regdata['age'] = request.form.get('newAge')
    regdata['address'] = request.form.get('newAddress')

    print(regdata)  # Simulating database insertion

    result, err = cdb.updateSSN(regdata)

    if result:
        flash("Customer Details Updated Successfully")

    else:
        flash("Failed to Update  Customer  Details "+err)

    return redirect(url_for('searchCustomer'))

>>>>>>> 8a1a85ff5a585fff30e75e188b0ed5ad634b03e5
