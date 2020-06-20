import requests
import json
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Bcc
from mailjet_rest import Client
import time
from datetime import  datetime
import pytz
EMAIL_REG_EXECUTIVE=1
EMAIL_REG_CUSTOMER=2
EMAIL_OPENED_Account=3

states=[{"code": "AN","name": "Andaman and Nicobar Islands"},
{"code": "AP","name": "Andhra Pradesh"},
{"code": "AR","name": "Arunachal Pradesh"},
{"code": "AS","name": "Assam"},
{"code": "BR","name": "Bihar"},
{"code": "CG","name": "Chandigarh"},
{"code": "CH","name": "Chhattisgarh"},
{"code": "DH","name": "Dadra and Nagar Haveli"},
{"code": "DD","name": "Daman and Diu"},
{"code": "DL","name": "Delhi"},
{"code": "GA","name": "Goa"},
{"code": "GJ","name": "Gujarat"},
{"code": "HR","name": "Haryana"},
{"code": "HP","name": "Himachal Pradesh"},
{"code": "JK","name": "Jammu and Kashmir"},
{"code": "JH","name": "Jharkhand"},
{"code": "KA","name": "Karnataka"},
{"code": "KL","name": "Kerala"},
{"code": "LA","name": "Ladakh"},
{"code": "LD","name": "Lakshadweep"},
{"code": "MP","name": "Madhya Pradesh"},
{"code": "MH","name": "Maharashtra"},
{"code": "MN","name": "Manipur"},
{"code": "ML","name": "Meghalaya"},
{"code": "MZ","name": "Mizoram"},
{"code": "NL","name": "Nagaland"},
{"code": "OR","name": "Odisha"},
{"code": "PY","name": "Puducherry"},
{"code": "PB","name": "Punjab"},
{"code": "RJ","name": "Rajasthan"},
{"code": "SK","name": "Sikkim"},
{"code": "TN","name": "Tamil Nadu"},
{"code": "TS","name": "Telangana"},
{"code": "TR","name": "Tripura"},
{"code": "UK","name": "Uttarakhand"},
{"code": "UP","name": "Uttar Pradesh"},
{"code": "WB","name": "West Bengal"}]
def getState():
    return states


def isStateValid(st):
    for x in states:
        if x['name']==st:
            return True
    return False


def getTime():
    india_tz=pytz.timezone('Asia/Kolkata')
    india_date=india_tz.localize(datetime.now())
    formats='%a,%d %b %Y,%I:%M %p %Z'
    return india_date.strftime(formats)

def getTimeUTC():
    return str(time.time_ns())



def isNameValid(name):
    cnt=0
    for z in name.lower():
        if z in "abcedefghijklmnopqrstuvwxyz":
            cnt+=1
        if cnt>=3:
            return True
    return False

def sendEmailSendInBlue(data):

    url = "https://api.sendinblue.com/v3/smtp/email"
    apikey=os.environ.get('SEND_IN_BLUE_API',None)
    if apikey==None:
        import config_internal
        apikey=config_internal.SEND_IN_BLUE_API

    payload = {}
    payload["sender"]={"name":"Rbank","email":"noreply@rbank.herokuapp.com"}
    payload["to"]=[{"email":f"{data['to']}","name":f"{data['name']}"}]
    payload["htmlContent"]=data['htmlContent']
    payload["subject"]=data['subject']
    payload["bcc"]=[{"email":"rajdubeygkp@gmail.com","name":"OWNER"}]
    
    json_payload=json.dumps(payload)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'api-key': apikey
        }

    response = requests.request("POST", url, data=json_payload, headers=headers)

    print("SEND_IN_BLUE: "+response.text)

def sendEmailBysendGrid(data):
    message = Mail(
        from_email='sender.rbank@gmail.com',
        to_emails=data['to'],
        subject=data['subject'],
        html_content=data['htmlContent'])
    try:
        api=os.environ.get('SENDGRID_API_KEY',None)
        if api==None:
            import config_internal
            api=config_internal.sendgridapi
        message.bcc=Bcc('rajdubeygkp@gmail.com','owner',p=0)
        sg = SendGridAPIClient(api)
        response = sg.send(message)
        print(response.status_code)
        print("SEND_GRID",response.body)
        # print(response.headers)
    except Exception as e:
        print("at sendGrid",e)



def sendEmailByMailjet(dataz):
    api_key=os.environ.get("MAILJET_API_KEY",None)
    api_secret=os.environ.get("MAILJET_API_SKEY",None)
    if api_key==None:
        import config_internal
        api_key=config_internal.mailjet_api_key
        api_secret=config_internal.mailjet_api_skey
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "admin@rbank.herokuapp.com",
            "Name": "Rbank"
        },
        "To": [
            {
            "Email": f"{dataz['to']}",
            "Name": f"{dataz['name']}"
            }
        ],
        "Subject": f"{dataz['subject']}",
        "HTMLPart": f"{dataz['htmlContent']}"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json())


    



def sendEmail(data):
    payload={}
    payload["replyTo"]={"email":"noreply@noreply.com","name":"Admin"}
    payload["to"]=f"{data['to']}"
    payload["name"]=f"{data['name']}"

    if data['type']==EMAIL_OPENED_Account:
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!! <br><br>Account Opened at our Bank.<br><br>Account Details<br><hr><br>Account ID:  <b>{data['cust_acc_id']}</b> <br><br>SSN ID:  <b>{data['ssn_id']}</b> <br><hr><br>Thank You,<br><a href='rbank.herokuapp.com'>   Rbank </a><br>Always at your Service "
        payload["subject"]=f"Account Opened for {data['ssn_id']} @Rbank"

    elif data['type']==EMAIL_REG_CUSTOMER:
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!! Thank you for registering with us as a Customer..<br><br>Here is Your SSN ID <b>{data['ssn_id']}</b> <br><br>Thank You,<br><a href='rbank.herokuapp.com'>   Rbank </a><br>Always at your Service "
        payload["subject"]="Registered as a Customer @ Rbank"
    if data['type']==EMAIL_REG_EXECUTIVE :
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!!<br><br>Thank you on being a part of Rbank.<br><br> <br>Here is Your SSN ID:  {data['ssn_id']}   <br> <br>please Login using this ID and your password!!! <br><br>Thank You,<br><a href='rbank.herokuapp.com'>    Rbank </a><br>Always at your Service "
        payload["subject"]="Executive Registered"

    try:
        sendEmailBysendGrid(payload)
        # sendEmailByMailjet(payload)
        sendEmailSendInBlue(payload)    
    except Exception as e:
        logging.error("Exception @ sendEmail in utility")
        logging.error(str(e))
        



data={}
data['type']=EMAIL_OPENED_Account
data['ssn_id']="123456789"
data['name']="Test Customer"
data['to']="com.mailuser@gmail.com"
data['cust_acc_id']="123"
if __name__=="__main__":
    # sendEmail(data)
    print(getTime())