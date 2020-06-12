from retail_banking import app
import hashlib

@app.route('/')
def home():
    # return render_template(url_for('retail_banking.home'))
    return "home"


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        #show when default this url is loaded ..
        return render_template('login.html',a="getr")
    else:
        # after user submit his username and password we get to this...
        email=request.form.get('email',None)
        password=request.form.get('psw',None)
        
        return render_template('login.html',a="post--"+email+"---"+hashlib.sha256(b'{password}').hexdigest())







