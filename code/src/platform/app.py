import requests
import sys
import hashlib
import datetime
sys.path.append('./models')


from flask import Flask, render_template, request, redirect, session, json
from authenticateModel import *
from werkzeug import generate_password_hash, check_password_hash
from email_pyfile import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc'

master_url = 'http://localhost:5003'

@app.route('/')
def main():
   return render_template('CodeEditor.html')

def createHTMLString(string):
    string = string.replace("\r\n", "<br />")
    return string.replace("\n", "<br />")

@app.route('/Submit',methods=['POST','GET'])
def signUp():
    _code = request.form['code']
    _language = request.form['language']
    #_input = request.form['input']
    _input = ""
    # validate the received values
    print _code
    print _language
    print _input

    r = requests.post(master_url+'/master', data=json.dumps({'code':_code, 'language':_language, 'input':_input}), headers={'Content-Type' : 'application/json'})
    responce = str(r.text)
    return render_template('CodeEditor.html',output = responce)
    #return json.dumps({'compilation_res':createHTMLString(responce)})

@app.route('/login', methods = ['GET','POST'])
def login():
    msg = []
    if request.method == 'GET':
        if 'username' in session:
            return redirect("http://localhost:8080/" + session['username'], code=302)
        return render_template('Login.html',errors = msg)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        errors = validateLogin(email,password)
        if len(errors) == 0:
            username = getUsernameFromEmail(email)
            session['username'] = username
            return redirect("http://localhost:8080/" + session['username'], code=302)
        else:
            return render_template('Login.html',errors = errors)

@app.errorhandler(404)
def page_not_found(e):
    msg = "Page not Found.!"
    return render_template('404.html',error = "Sorry", h1tag_msg = msg), 404

@app.errorhandler(500)
def server_not_found(e):
    msg = "Page not Found.!"
    return render_template('404.html',error = "Sorry", h1tag_msg = msg), 500

@app.route('/<username>',methods = ['GET'])
def logged_in(username):
    msg = "Page not found.!"
    if 'username' in session:
        if session['username'] != username:
            return render_template('404.html', error = "Sorry", h1tag_msg = msg)
        elif session['username'] == username:
            return render_template('CodeEditor.html')
    else:
        return redirect("http://localhost:8080/", code=302)

@app.route('/<username>/Logout',methods = ['GET'])
def logout(username):
    msg = "Page not found.!"
    if session['username'] == username:
        session.pop('username',None)
        return redirect("http://localhost:8080/", code=302)
    elif session['username'] != username:
        return render_template('404.html', error = "Sorry", h1tag_msg = msg)

@app.route('/SignUp',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'username' in session:
            return redirect("http://localhost:8080/" + session['username'], code=302)
        else:
            return render_template('SignUp.html')
    elif request.method == 'POST':
        
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmPassword']

        errors = validateRegistration(email,username,password,confirmpassword);

        if len(errors) == 0:
            m = hashlib.sha256()
            #d = bytes(str(datetime.datetime.now()),'utf-8')
            d = bytes(str(datetime.datetime.now()))
            m.update(d)
            key = m.hexdigest()
            isSuccess = register(email,username,password,key)
            body = "Click on the following link to activate your account..! \n" \
                    "http://localhost:8080/activate" + "?email=" + email + "&id=" + key
            subject = "Activate Your Account"
            mail(email,body,subject)    
            if isSuccess:
                return redirect("http://localhost:8080/Congratulation?success=register", code=302)
            else:
                return "Error"
        else:
            return render_template('SignUp.html',errors = errors)

@app.route('/Congratulation',methods = ['GET'])
def success():
    if 'username' in session:
        return redirect("http://localhost:8080/" + session['username'], code=302)
    else:
        if request.args.get('success').lower() == 'register':
            msg = "You have Successfully Registered. Please check your mail and activate your account :-)"
            return render_template('Success.html',h2tag_msg = msg)
        elif request.args.get('success').lower() == 'mailsent':
            msg = "Mail has been sent successfully. Please check your email :-)"
            return render_template('Success.html',h2tag_msg = msg)
        elif request.args.get('success').lower() == 'accountactivated':
            msg = "You have been successfully activated your account :-)"
            return render_template('Success.html',h2tag_msg = msg)
        elif request.args.get('success').lower() == 'changepassword':
            msg = "Your password changed successfully. Now you can login :-)"
            return render_template('Success.html',h2tag_msg = msg)
        else:
            msg = "Sorry, bad request."
            return render_template('404.html', error="404", h1tag_msg = msg)

@app.route('/ForgotPassword',methods = ['GET','POST'])
def forgot_password():
    if request.method == 'GET':
        if 'username' in session:
            return redirect("http://localhost:8080/" + session['username'], code=302)
        else:
            return render_template('ForgotPassword.html')
    elif request.method == 'POST':
        email = request.form['email']
        m = hashlib.sha256()
        d = bytes(str(datetime.datetime.now()))
        m.update(d)
        key = m.hexdigest()

        forgotPasswordDetails(email,key)
        isRegister = isRegistered("email",email)
        errors = ['Email Id is not registered.!']
        if isRegister == True:
            body = "Click on the following link to change your password..! \n" \
                    "http://localhost:8080/ChangePassword" + "?email=" + email + "&id=" + key + "&pass=forgot"
            subject = "Change Password Request"
            mail(email,body,subject)
            return redirect("http://localhost:8080/Congratulation?success=mailsent", code=302)
        else:
            return render_template('ForgotPassword.html', errors = errors) 
    else:
        msg = "Sorry, bad request."
        return render_template('404.html',error = "404", h1tag_msg = msg)

@app.route('/activate',methods = ['GET'])
def activate():
    if 'username' in session:
        return redirect("http://localhost:8080/" + session['username'], code=302)
    else:
        email = request.args.get('email')
    
        id = request.args.get('id')
        key = getActivationKey(email)
    
        if key == id:
            activateEmail(email)
            return redirect("http://localhost:8080/Congratulation?success=accountactivated", code=302)
        else:
            msg = "Somthing thing went wrong. Plase copy link correctly."
            return render_template('404.html', error = "Sorry", h1tag_msg = msg)

@app.route('/ChangePassword',methods = ['GET','POST'])
def change_password():
    if request.method == 'GET':
        if 'username' in session:
            return redirect("http://localhost:8080/" + session['username'], code=302)
        else:
            email = request.args.get('email')
    
            id = request.args.get('id')
            key = getKeyForChangePassword(email)
            isKeyValid = isKeyExpired(email)
            if isKeyValid == 0:
                return "Bad Request"
            else:
                if key == id:
                    return render_template('ChangePassword.html')
                else:
                    msg = "Somthing thing went wrong. Plase copy link correctly."
                    return render_template('404.html', error = "Sorry", h1tag_msg = msg)
    elif request.method == 'POST':
        email = request.args.get('email')
        key = request.args.get('id')
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if password == confirmPassword:
            changePassword(email, password, key)
            return redirect("http://localhost:8080/Congratulation?success=changepassword", code=302)
        else:
            msg = "Somthing thing went wrong. Please try again."
            return render_template('404.html', error = "Sorry", h1tag_msg = msg)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080)
