import requests
import json
import logging


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



def sendEmail(data):
    url = "https://api.sendinblue.com/v3/smtp/email"
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'api-key': "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"
        }


    payload={}
    payload['sender']={"name":"Rbank","email":"noreply@noreply.com"}
    payload["replyTo"]={"email":"noreply@noreply.com","name":"Admin"}
    payload["to"]=[{"email":f"{data['senderId']}","name":f"{data['name']}"}]

    if data['type']==EMAIL_OPENED_Account:
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!! <br><br>Account Opened at our Bank.Below are your Account Details<br><br>Account ID:  {data['cust_acc_id']} <br><br>SSN ID:  {data['ssn_id']} <br><br>Thank You,<br><a href='rbank.herokuapp.com'>Rbank </a>,Always at your Service "
        payload["subject"]=f"Account Opened for {data['ssn_id']} @Rbank"

    elif data['type']==EMAIL_REG_CUSTOMER:
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!! Thank you on registering with us as a Customer..<br><br>Here is Your SSN ID {data['ssn_id']} <br><br>Thank You,<br><a href='rbank.herokuapp.com'>Rbank </a>,Always at your Service "
        payload["subject"]="Registered as a Customer @ Rbank"
    if data['type']==EMAIL_REG_EXECUTIVE :
        payload["htmlContent"]=f"Dear {data['name']},<br> <br>Congratulation !!!<br><br>Thank you on being a part of Rbank.<br><br> <br>Here is Your SSN ID:  {data['ssn_id']}   <br> <br>please Login using this ID and your password!!! <br><br>Thank You,<br><a href='rbank.herokuapp.com'>Rbank </a>,Always at your Service "
        payload["subject"]="Executive Registered"

    try:
        json_payload=json.dumps(payload)
        print(json_payload)

        response = requests.request("POST", url, data=json_payload, headers=headers)

        print(response.text)
    except :
        logging.error("Exception @ sendEmail in utility")
        


# data={}
# data['type']=EMAIL_REG_CUSTOMER
# data['ssn_id']="123456789"
# data['name']="Test Customer"
# data['senderId']="rajdubeygkp@gmail.com"
# data['cust_acc_id']="123"

def isNameValid(name):
    cnt=0
    for z in name.lower():
        if z in "abcedefghijklmnopqrstuvwxyz":
            cnt+=1
        if cnt>=3:
            return True
    return False
