from flask import Flask,render_template,url_for,request

app=Flask(__name__)

print("loaded init")
app.secret_key="123124124nfnefn"
