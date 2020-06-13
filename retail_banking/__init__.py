from flask import Flask,render_template,url_for,request
from retail_banking import *
from config import Config

app=Flask(__name__)


app.secret_key=Config.SECRET_KEY

# Setting the database and configuration using Config class in config.py file
app.config.from_object(Config)
