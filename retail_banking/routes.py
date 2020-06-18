# import this line in every new module you create this will give access to app with required library
# for more info check __init__.py file
from retail_banking import *
from . import utility
from time import gmtime, strftime
import time
from flask import redirect, render_template, url_for, json, flash

import hashlib
try:
    from .databases import customerdb as cdb
    from .databases import executive as edb
except Exception as e:
    print("Import error ",e)


@app.route('/')
def home():
    return render_template('home.html', home=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if isLoggedin():
        # redirect in case user is already logged In
        return(redirect(url_for('home')))
    if request.method == "GET":
        # show when default this url is loaded ..
        return render_template('login.html', login=True)
    else:
        # after user submit his username and password we get to this...
        uid = request.form.get('uid', "userNotFound")
        password = request.form.get('psw', "passwordNotfound")
        passhax = hashlib.sha256(password.encode()).hexdigest()

        filter = {'ssn_id': uid, 'pass': passhax}

        result = edb.find(filter)

        if result == None:
            flash("Wrong UserName or Password retry", "danger")
            return redirect(url_for('login'))
        else:
            # setup session~~~
            session_login(uid, result['name'])
            if isLoggedin():
                flash("Successfully Logged in", "success")
            else:
                flash("Can not setup session ", "danger")
            # end setup

            return redirect(url_for('home'))


@app.route('/registerExecutive', methods=['get', 'post'])
def registerExecutive():

    if request.method == "GET":
        autodata = {}
        sid = edb.getautoSSNid()
        flash("Auto generated SSN ID : "+sid)
        autodata['ssn_id'] = sid
        return render_template('registerExecutive.html', registerExecutive=True, autodata=autodata)

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['email'] = request.form.get('email')
    regdata['pass'] = hashlib.sha256(
        request.form.get('psw').encode()).hexdigest()

    regdata['creation_time'] = time.strftime(
        "%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())
    result, err = edb.register(regdata)

    if result:
        flash("Executive Registered Successfully ...    Login Now", "success")
        return redirect(url_for('login'))
    else:
        flash("Failed to Register :"+err, "danger")
        return redirect(url_for('registerExecutive'))

    return redirect('login.html')


@app.route('/registerCustomer', methods=['get', 'post'])
def registerCustomer():

    if not isLoggedin():
        # if there is no one loggedIn disallow this route
        flash("Login first to access it ", "danger")
        return redirect(url_for('home'))

    if request.method == "GET":
        autodata = {}
        sid = cdb.getautoSSNid()
        flash("Auto generated SSN ID : "+sid)
        autodata['ssn_id'] = sid
        autodata['states']=utility.getState()
        return render_template('registerCustomer.html', registerCustomer=True, autodata=autodata)

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn')
    regdata['name'] = request.form.get('name')
    regdata['age'] = request.form.get('age')
    regdata['state'] = request.form.get('state')
    # regdata['city '] = request.form.get('city')
    regdata['address'] = request.form.get('address')
    regdata['create_time']=time.strftime(
        "%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())

    print(regdata)  # Simulating database insertion

    result, err = cdb.registerSSN(regdata)

    if result:
        flash("Customer Registered Successfully", "success")
        return redirect(url_for('viewCustomerDetail')+"/"+regdata['ssn_id'])
    else:
        flash("Failed to Register Customer "+err, "danger")

    return render_template('registerCustomer.html', registerCustomer=True)


@app.route('/logout')
def logout():
    if isLoggedin():
        # log out by invalidating session
        session_logout()
        flash("You have been successfully logged out", "success")
    else:
        flash("You are already Logged out..", "success")

    return redirect(url_for('home'))

# Utility Function


def session_logout():
    session.pop('ssn_id', None)
    session.pop('username', None)


def session_login(ssn_val, username):
    session['ssn_id'] = ssn_val
    session['username'] = username


def isLoggedin():
    if 'ssn_id' in session.keys():
        return True
    else:
        return False

# Search customer by SSN ID to delete or update details
@app.route('/searchCustomer', methods=['get', 'post'])
def searchCustomer():
    if not isLoggedin():
        return redirect(url_for('login'))
    autodata = {}
    if request.method == "GET":
        if 'ssn_id' in request.args:
            autodata['ssn_id'] = request.args.get('ssn_id')
        return render_template('searchCustomer.html', searchCustomer=True, autodata=autodata)

        # when ssn_id is passed ..so

    # make a rediection while post ..
    return redirect(url_for('updateCustomer')+"/"+request.form.get('ssn_id'))


@app.route('/updateCustomer/<ssn_id>')
@app.route('/updateCustomer', methods=['get', 'post', 'update'])
def updateCustomer(ssn_id=None):

    if not isLoggedin():
        return redirect(url_for('login'))

    if request.method == "GET":
        if ssn_id == None:
            return redirect(url_for('searchCustomer'))
        else:
            # when ssn_id is passed ..so
            filter = {'ssn_id': ssn_id}

            # Retrieving details of customer
            result = cdb.findSSN(filter)
            if result:
                args = {}
                args['ssn_id'] = result['ssn_id']
                args['oldAge'] = result['age']
                args['oldAddress'] = result['address']
                args['oldName'] = result['name']
                args['oldState']=result['state']
                args['states']=utility.getState()
                return render_template('updateCustomer.html', updateCustomer=True, **args)
            else:
                flash(
                    "Unable to find customer. Try again by entering valid SSN ID.", "danger")
                return redirect(url_for('searchCustomer'))

    regdata = {}

    regdata['ssn_id'] = request.form.get('ssn_id')
    regdata['name'] = request.form.get('newName')
    regdata['age'] = request.form.get('newAge')
    regdata['address'] = request.form.get('newAddress')
    regdata['state']=request.form.get('newState')

    result, err = cdb.updateSSN(regdata)

    if result:
        flash("Customer Details Updated Successfully", "success")
        return redirect(url_for('viewCustomerDetail')+"/"+regdata['ssn_id'])

    else:
        flash("Failed to Update  Customer  Details "+err, "danger")

    return redirect(url_for('searchCustomer'))


@app.errorhandler(404)
def not_found(e):
    return render_template('error404.html')


@app.route('/viewCustomerDetail/<ssn_id>')
@app.route('/viewCustomerDetail', methods=["GET", "POST"])
def viewCustomerDetail(ssn_id=None):
    if not isLoggedin():
        return redirect(url_for('login'))

    filter = {}
    if request.method == "GET":
        if ssn_id == None:
            redirect(url_for('searchCustomer'))
        else:
            filter = {'ssn_id': ssn_id}
    else:  # if it is a post request..
        filter = {'ssn_id': request.form.get('ssn_id')}

    # Retrieving details of customer
    result = cdb.findSSN(filter)
    print("ssn is ", ssn_id)
    print(result)

    if result:
        args = {}
        args['titleDetail'] = ":Customer SSN Detail"
        args['age'] = result['age']
        args['name'] = result['name']
        args['address'] = result['address']
        args['ssn_id'] = result['ssn_id']
        args['state']=result['state']
        return render_template('viewCustomerDetail.html', viewCustomerDetail=True, **args)
    else:
        flash("Unable to find customer. Try again by entering valid SSN ID.", "danger")
        return redirect(url_for('searchCustomer'))


@app.route('/viewAllCustomer')
def viewAllCustomer():

    if not isLoggedin():
        return redirect(url_for('login'))

    customers_data = []
    for dat in cdb.findSSN_all():
        customers_data.append(dat)

    return render_template('viewAllCustomer.html', viewAllCustomer=True, datas=customers_data)


@app.route('/deleteCustomer', methods=['GET', 'POST'])
def deleteCustomer():
    if not isLoggedin():
        return redirect(url_for('login'))

    if request.method == "GET":
        if 'ssn_id' in request.args:
            ssn_id = request.args.get('ssn_id')
            result = cdb.findSSN({'ssn_id': ssn_id})

            if result:
                args = {}
                args['ssn_id'] = result['ssn_id']
                args['oldAge'] = result['age']
                args['oldAddress'] = result['address']
                args['oldName'] = result['name']
                flash(" Customer found! ", "success")
                flash("Please confirm the details before deletion.", "danger")
                return render_template('confirmDeleteCustomer.html', deleteCustomer=True, **args)

            else:
                flash("Customer not found! Please enter a valid SSN ID.", "danger")

        return redirect(url_for('searchCustomer'))

    filter = {'ssn_id': request.form.get('ssn_id')}

    result = cdb.deleteSSN(filter)

    if result:
        print(result)
        flash("Successfully deleted customer!", "success")
        return redirect(url_for('home'))
    else:
        flash("Unable to delete customer. Try again by entering valid SSN ID.", "danger")
        return redirect(url_for('searchCustomer'))


@app.route('/createAccount', methods=['get', 'post'])
def createAccount():
    if not isLoggedin():
        return redirect(url_for('login'))
    cust_acc_id=""
    autodata = {}  # data that will be passed
    if request.method == "GET":
        if 'ssn_id' in request.args:
            sid = request.args.get('ssn_id')
            if not cdb.findSSN({'ssn_id': sid}):
                # no such ssn exist return back to searchCustomer
                flash(
                    "Unable to find customer. Try again by entering valid SSN ID.", "danger")
                return redirect(url_for('searchCustomer'))

            autodata['ssn_id'] = sid

        cust_acc_id = cdb.getautoAccountid()
        flash("Auto generated Account no : "+cust_acc_id)
        autodata['cust_acc_id'] = cust_acc_id
        return render_template('createAccount.html', createAccount=True, autodata=autodata)

    # if request id POST
    data = {}

    # check if customer exists or not and return flash accordingly

    data['ssn_id'] = request.form.get('ssn_id')
    data['type'] = request.form.get('type')
    data['cust_acc_id'] = request.form.get('cust_acc_id')
    cust_acc_id=data['cust_acc_id']
    data['balance'] = 0.0
    data['create_time']=time.strftime(
        "%a,%d %b %Y %I:%M:%S %p %Z", time.gmtime())

    # print(data)
    # save data to database.
    if not cdb.findSSN({'ssn_id': data['ssn_id']}):
        flash("No such Customer Registered with SSN_ID=" +
              data['ssn_id'], "danger")
        return render_template('createAccount.html', createAccount=True, autodata={'cust_acc_id': cust_acc_id})

    result, err = cdb.createAccount(data)

    if result:
        flash(
            f"Customer Account {data['cust_acc_id']}  Successfully", "success")
        # return redirect(url_for('viewCustomerDetail')+"/"+regdata['ssn_id'])
        return redirect(url_for('home'))
    else:
        flash("Failed to Create Customer Account: "+err, "danger")

    return render_template('createAccount.html', createAccount=True, autodata=data)

@app.route('/searchAccount', methods=['get', 'post'])
def searchAccount():
    if not isLoggedin():
        return redirect(url_for('login'))
    is_redirect=False
    redirectto="home" #bydefault
    acc_id=""
    ssn=""
    result=None
    if request.method == "GET":
        if "redirect" in request.args:
            is_redirect=True
            redirectto=request.args.get("redirect")

        if 'ssn_id'  in request.args:
            ssn=request.args.get('ssn_id')

            result=cdb.findAcc_all_of_ssnid(str(ssn))
        elif 'cust_acc_id' in request.args:
            temp=cdb.findAccount({'cust_acc_id':request.args.get('cust_acc_id')})
            if temp:
                result=[temp]
                ssn=temp['ssn_id']
                acc_id=temp['cust_acc_id']
                flash("Account Found .","success")
                return redirect(url_for(redirectto)+"?cust_acc_id="+acc_id)
            else:
                flash(f"Account ID :{request.args.get('cust_acc_id')} does not exist ","danger")
                return redirect(url_for('searchAccount'))

        else:
            return render_template('searchAccount.html',searchAccount=True,is_redirect=str(is_redirect),redirectto=redirectto)
    
    else: #post requests
        ssn = request.form.get('ssn_id')
        account=request.form.get('cust_acc_id')
        if ssn=="" and account=="":
            #both are empty redirect 
            flash("Please enter Either SSN ID or Customer Account ID! ", "danger")
            return redirect(url_for('searchAccount'))
        
        is_redirect=bool(request.form.get("is_redirect"))
        redirectto=str(request.form.get("redirectto"))

        print("---->  ",is_redirect,"   --- ",redirectto,type(is_redirect),type(redirectto))
        
        if ssn!="":
            #checking of ssn will be done only hence making acc_id blank
            print("SSN NOT == ",ssn)
            acc_id=""
            is_redirect=False #make it False in case ssn id is entered..
            #first find if the ssn id is valid or not
            if not cdb.findSSN({'ssn_id':ssn}):
                flash("Invalid SSN entered! Please type correct SSN ID","danger")
                return redirect(url_for('searchAccount'))
            
            result = cdb.findAcc_all_of_ssnid(str(ssn))


        if account!="":
            print("ACC ID == ",account)
            acc_id=account
            temp=cdb.findAccount({'cust_acc_id':acc_id})
            if temp:
                result=[temp]
                ssn=temp['ssn_id']
                #found by account id hence redirect directly to particular redirection
                if is_redirect:
                    flash("Account Found ","success")
                    return redirect(url_for(redirectto)+"?cust_acc_id="+acc_id)


                

    print("*"*80)
    print("found accounts->",result)
    print("*"*80)

    if result:
        account_data = []
        for data in result:
                account_data.append(data)
                print(data)

        flash("Successfully found Account!", "success")
        return render_template('viewAllAccount.html', datas=account_data,cust_ssn_id=ssn)
    else:
        if acc_id!="":
            flash("Could not find the account! Please enter valid  Account ID", "danger")
        else:
            flash("Could not find any Customer With that SSN ID! Please enter valid  SSN ID", "danger")

        return redirect(url_for('searchAccount'))


@app.route('/deleteAccount', methods=['GET', 'POST'])
def deleteAccount():
    if not isLoggedin():
        return redirect(url_for('login'))

    if request.method == "GET":
        if 'cust_acc_id' in request.args:
            cust_acc_id = request.args.get('cust_acc_id')

            # find account no and details using ssn_id
            print("ACC ID :", cust_acc_id)
            # result = cdb.findAccount({'cust_acc_id': cust_acc_id})
            result = cdb.findAccount({'cust_acc_id':cust_acc_id})

            if result:
                args = {}
                args['ssn_id'] = result['ssn_id']
                args['cust_acc_id'] = result['cust_acc_id']
                args['type'] = result['type']
                args['balance'] = result['balance']
                flash("Please confirm the details before deletion.", "danger")
                return render_template('confirmDeleteAccount.html', deleteAccount=True, **args)
            else:
                flash("Customer not found! Please enter a valid SSN ID.", "danger")

        return redirect(url_for('searchAccount'))

    filter = {'cust_acc_id': request.form.get('accID')}
    print("ACC ID ::::", request.form.get('accID'))
    result = cdb.deleteAccount(filter)
    print("result ", result)
    if result:
        print("Delete ACC:---->",result)
        flash("Successfully deleted account! :"+filter['cust_acc_id'], "success")
        return redirect(url_for('searchAccount')+"?ssn_id="+result['ssn_id'])
    else:
        flash("Unable to delete customer. Try again by entering valid SSN ID.", "danger")
        return redirect(url_for('searchAccount'))


@app.route('/deposit',methods=['GET','POST'])
def deposit():
    if not isLoggedin():
        return redirect(url_for('login'))
    cust_acc_id=""
    if request.method=="GET":
        if "cust_acc_id" in request.args:
            cust_acc_id=request.args.get('cust_acc_id')
            result=cdb.findAccount({'cust_acc_id':cust_acc_id})
            if result:
                return render_template('deposit.html',deposit=True,data=result)
#if nothing matches in GET atlast goto searchAccount route
        return redirect(url_for('searchAccount')+"?redirect=deposit")

    ###FOR POST >>>MAKING TRANSACTION NOW...

    data={}

    data['cust_acc_id']=request.form.get('cust_acc_id')
    data['transaction_type']="credit"
    data['amount']=request.form.get('amount')
    data['remark']="self deposit"
    data['executive_ssn_id']=session.get('ssn_id')
    data['balance']=request.form.get('balance')
    result,err=cdb.deposit(data)
    if result:
        flash(f"Amount {data['amount']} deposited Successfully to Account ID :{data['cust_acc_id']}","success")
        return redirect(url_for('home'))
    else:
        flash(f"Error in Transaction :{err}","danger ")
        return redirect(url_for('home'))






@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
    if not isLoggedin():
        return redirect(url_for('login'))
    cust_acc_id=""
    if request.method=="GET":
        if "cust_acc_id" in request.args:
            cust_acc_id=request.args.get('cust_acc_id')
            result=cdb.findAccount({'cust_acc_id':cust_acc_id})
            if result:
                return render_template('withdraw.html',deposit=True,data=result)
#if nothing matches in GET atlast goto searchAccount route
        return redirect(url_for('searchAccount')+"?redirect=withdraw")

    ###FOR POST >>>MAKING TRANSACTION NOW...

    data={}

    data['cust_acc_id']=request.form.get('cust_acc_id')
    data['transaction_type']="debit"
    data['amount']="-"+request.form.get('amount')
    data['remark']="self withdrawl"
    data['executive_ssn_id']=session.get('ssn_id')
    data['balance']=request.form.get('balance')

    result,err=cdb.withdraw(data)
    if result:
        flash(f"Amount {data['amount']} Withdrawn Successfully from  Account ID :{data['cust_acc_id']}","success")
        return redirect(url_for('home'))
    else:
        flash(f"Error in Transaction :{err}","danger ")
        return redirect(url_for('home'))


@app.route("/transfer",methods=["GET","POST"])
def transferMoney():
    if not isLoggedin():
        return redirect(url_for('login'))

    if request.method=="GET":
        return render_template('transferMoney.html')
    ###for post get the datass

    amount=request.form.get('amount_transferred')
    source_acc=request.form.get('source_acc_no')
    dest_acc=request.form.get('target_acc_no')
    result,err=cdb.transfer(source_acc,dest_acc,amount,session.get('ssn_id'))
    if result:
        flash(f"From Account: {source_acc} transferred Rs. {amount} Successfully to {dest_acc} ","success")
    else:
        flash(f"Failed To transfer Money "+str(err),"danger")
    return redirect(url_for('home'))

@app.route('/viewTransaction')
def viewTransaction():
    if not isLoggedin():
        return redirect(url_for('login'))
    cust_id=""
    trans_id=""
    TRANS_DATA=False

    if request.method=="GET":
        if 'cust_acc_id' in request.args :
            cust_id=request.args.get('cust_acc_id')
        if 'trans_id' in request.args:
            trans_id=request.args.get('trans_id')

        if cust_id=="" and trans_id=="":
            flash("Please Enter Either Customer Account ID or Transaction Id ","danger")
            return render_template('searchTransaction.html')
        if cust_id!="":
            TRANS_DATA=cdb.findAllTransaction(cust_id)
            trans_id==""
        elif trans_id!="":
            TRANS_DATA=cdb.findTransaction({'trans_id':trans_id})
            if TRANS_DATA:
                cust_id=TRANS_DATA['cust_acc_id']
                TRANS_DATA=[(TRANS_DATA)]
        else:
            return render_template('searchTransaction.html')
  
    if TRANS_DATA:
        return render_template('viewAllTransaction.html',datas=TRANS_DATA,cust_acc_id=cust_id)
    else:
        if trans_id=="":
            flash(f"No Transaction Exist for Account id {cust_id}","danger")
        else:
            flash(f"Transaction {trans_id} Doesn't Exist","danger")

        return redirect(url_for('home'))


    
