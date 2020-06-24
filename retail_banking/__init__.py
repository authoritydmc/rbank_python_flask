from flask import Flask,render_template,url_for,request,session
import logging
import os
app=Flask(__name__)
app.secret_key=os.environ.get("APP_SECRET_KEY",None)
if app.secret_key==None:
    from . import config_internal
    app.secret_key=config_internal.APP_SECRET_KEY
