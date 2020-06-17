from flask import Flask,render_template,url_for,request,session

app=Flask(__name__)
app.secret_key="123124124nfnefn"

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))