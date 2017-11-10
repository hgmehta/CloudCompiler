import requests
import sys, parse
import hashlib
import datetime
import base64
import random
import socket, ast
from uuid import getnode

reload(sys)
sys.path.append('./dependancies/')
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template, request, redirect, session, json
from authenticateModel import *
from werkzeug import generate_password_hash, check_password_hash

from email_pyfile import *
from activity import *
from filemanager import *
from service import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc'

hostname = socket.gethostname()
AppAddress = socket.gethostbyname(hostname)
port = 8080
domain = "http://" + AppAddress + ":" + str(port) + "/"

master_url = 'http://localhost:5003'

@app.route('/temp')
def temp():
    conn = connectTolog()
    cursor = getFromActivityLog(session['id'])
    for row in cursor:
        print "filename = ", row[0]
        print "Language = ", row[1]
        print "Time = ", row[2]
        print "Compilation Status = ", row[3]
        print "Runtime Status = ", row[4]
        print "Duration = ", row[5]
        print "Memory Uasge = ", row[6], "\n"
    conn.close()
    return "Connected Database"

@app.route('/<username>/activity', methods = ['GET'])
def loginActivity(username):
    if 'username' in session:
        if session['username'] == username:
            if 'id' in request.args:
                if len(request.args.get('id')) != 32:
                    msg = "Bad request"
                    return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)
                else:
                    table = ["Filename", "Language", "Time", "Compilation Status", "Runtime Status", "Duration (s)", "Memory  Usage"]
                    userActivity = list(getFromActivityLog(request.args.get('id')))
                    return render_template('LoginActivity.html', domain = domain, username = session['username'], activities = userActivity, activityType = "user", table = table)
            else:
                table = ["Date", "IP", "Platform", "Browser", "Actions"]
                Allactivities = list(getFromLoginlog(session['username']))
                return render_template('LoginActivity.html', domain = domain, username = session['username'], activities = Allactivities, activityType = "login", table = table)
        else:
            msg = "Bad request"
            return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)
    else:
        return redirect(domain, code=302)
@app.route('/')
def main():
   return render_template('home.html',domain = domain)

@app.route('/guest', methods=['GET','POST'])
def guestcompiler():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(domain + session['username'] + "/codeeditor",code = 302)
        else:
            languages = retriveLanguages()
            return render_template('_CodeEditor.html',domain = domain,username = 'guest', languages = languages)
    elif request.method == 'POST':
        _code = request.form['code']
        _language = request.form['language']
        _input = request.form['input']
        _username = 'guest'
        response, languages, _, _, exe_time = compile(_code, _language, _username, _input)
        return render_template('_CodeEditor.html',domain = domain,username = 'guest',languages = languages, output = response, code = _code, input = _input, language = _language, executionTime=exe_time)
    else:
        languages = retriveLanguages()
        return render_template('_CodeEditor.html',domain = domain, languages = languages)

@app.route('/perform',methods=['POST'])
def perform():
    if "compile" in request.form:
        return redirect(domain + "compile",code = 307)
    elif "save" in request.form:
        return redirect(domain + "savefile",code = 307)



@app.route('/<username>/files', defaults={'filetype':'None'})
@app.route('/<username>/files/<filetype>')
def filemanager(username,filetype):
    rows = []
    if filetype=="None":
        rows = retriveFolders()
        return render_template('FileManager.html',folder = "None",domain = domain,username = session['username'], links = rows)
    else:
        filetype_decoded = base64.b64decode(filetype)
        lang = getLanguageFromFileType(filetype_decoded)
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            #totalfiles = totalfile(filetype)
            #totalpages = int(totalfile / 10)
            cursor.execute("SELECT filename, TO_BASE64(filename), fileType, '" + session['username'] + "' , 'Size' , date(timeCreated),icon,pcid, id FROM repository INNER JOIN languages ON languages.extension = repository.fileType WHERE username = %s AND filetype = %s ORDER BY repository.id DESC", (session['username'],filetype_decoded,))
            rows = cursor.fetchall()
            rows = [list(i) for i in rows]
            return render_template('FileManager.html',folder = lang,domain = domain,username = session['username'], links = rows)

@app.route('/login', methods = ['GET','POST'])
def login():
    msg = []
    if request.method == 'GET':
        if 'username' in session:
            return redirect(domain + session['username'] + '/codeeditor', code=302)
        return render_template('Login.html',errors = msg)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        errors = validateLogin(email,password)
        if len(errors) == 0:
            username = getUsernameFromEmail(email)

            m = hashlib.md5()
            num = str(random.randint(1,10000))
            string = str(datetime.datetime.now()) + username + num
            #d = bytes(str(datetime.datetime.now()),'utf-8')
            d = bytes(string)
            m.update(d)
            key = m.hexdigest()

            session['username'] = username
            session['id'] = str(key)
            insertInLoginlog(session['username'])
            return redirect(domain + session['username']+ '/codeeditor', code=302)
        else:
            return render_template('Login.html',errors = errors)

@app.route('/<username>/codeeditor',methods = ['GET','POST'])
def logged_in(username):
    if request.method == 'GET':
        filename = request.args.get('file')
        filetype = request.args.get('type')
        # request.environ['REMOTE_ADDR']
        if filename is None or filetype is None:
            msg = "Page not found.!"
            if 'username' in session:
                if session['username'] != username:
                    return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)
                elif session['username'] == username:
                    languages = retriveLanguages()
                    return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages,language = filetype, filetype = "None")
            else:
                return redirect(domain, code=302)
        else:
            filename = base64.b64decode(filename)
            code = readfile(filetype,session['username'],filename)
            languages = retriveLanguages()
            file_type = getLanguageFromType(filetype)
            return render_template('_CodeEditor.html',domain = domain,code = code,username = session['username'],languages = languages,language = file_type, fname = filename, filetype = filetype)
    elif request.method == 'POST':
        _code = request.form['code']
        _language = request.form['language']
        _input = request.form['input']
        _username = 'guest'
        print request.environ['REMOTE_ADDR']
        if "compile" in request.form:
            if 'username' in session:
                _username = session['username']
            response, languages, _cStatus, _rStatus, _execution = compile(_code, _language, _username, _input)
            _language = getLanguageFromFileType(_language)
            insertInActivityLog("-",_language,_cStatus,_rStatus,_execution,"10 KB",session['username'],session['id'])
            return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages, output = response, code = _code, input = _input, language = _language, executionTime = _execution, memUsage = "10 KB", filetype = "None")
        else:
            _filename = request.form['filename']
            _username = session['username']
            output, languages = savefile(_code, _language, _input, _filename, _username)
            _language = getLanguageFromFileType(_language)
            # insertInActivityLog(_filename,_language,"-","-","-","-",session['username'],session['id'])
            return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages, output = output, code = _code, input = _input, language = _language, filetype = "None")

@app.route('/<username>/dashboard',methods = ['GET'])
def dashboard(username):
    msg = "Page not found.!"
    if 'username' in session:
        if session['username'] != username:
            return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)
        elif session['username'] == username:
            fileno = getTotalFileNo()
            return render_template('Dashboard.html',domain = domain,username = session['username'], filecount = fileno)
    else:
        return redirect(domain, code=302)

@app.errorhandler(404)
def page_not_found(e):
    msg = "Page not Found.!"
    return render_template('404.html',domain = domain,error = "Sorry", h1tag_msg = msg), 404

@app.errorhandler(500)
def server_not_found(e):
    msg = "Page not Found.!"
    return render_template('404.html',domain = domain,error = "Sorry", h1tag_msg = msg), 500

@app.route('/<username>/logout',methods = ['GET'])
def logout(username):
    msg = "Page not found.!"
    if session['username'] == username:
        session.pop('username',None)
        return redirect(domain, code=302)
    elif session['username'] != username:
        return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(domain + session['username'], code=302)
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
                     + domain + "activate" + "?email=" + email + "&id=" + key
            subject = "Activate Your Account"
            mail(email,body,subject)    
            if isSuccess:
                return redirect(domain + "congratulation?success=register", code=302)
            else:
                return "Error"
        else:
            return render_template('SignUp.html',errors = errors)

@app.route('/congratulation',methods = ['GET'])
def success():
    if 'username' in session:
        return redirect(domain + session['username'], code=302)
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
            return render_template('404.html',domain = domain, error="404", h1tag_msg = msg)

@app.route('/forgotpassword',methods = ['GET','POST'])
def forgot_password():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(domain + session['username'], code=302)
        else:
            return render_template('ForgotPassword.html',domain = domain)
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
                     + domain + "ChangePassword" + "?email=" + email + "&id=" + key + "&pass=forgot"
            subject = "Change Password Request"
            mail(email,body,subject)
            return redirect(domain + "congratulation?success=mailsent", code=302)
        else:
            return render_template('ForgotPassword.html',domain = domain, errors = errors) 
    else:
        msg = "Sorry, bad request."
        return render_template('404.html',domain = domain,error = "404", h1tag_msg = msg)

@app.route('/activate',methods = ['GET'])
def activate():
    if 'username' in session:
        return redirect(domain + session['username'], code=302)
    else:
        email = request.args.get('email')
    
        id = request.args.get('id')
        key = getActivationKey(email)
    
        if key == id:
            activateEmail(email)
            return redirect(domain + "congratulation?success=accountactivated", code=302)
        else:
            msg = "Somthing thing went wrong. Plase copy link correctly."
            return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)

@app.route('/changepassword',methods = ['GET','POST'])
def change_password():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(domain + session['username'], code=302)
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
                    return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)
    elif request.method == 'POST':
        email = request.args.get('email')
        key = request.args.get('id')
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if password == confirmPassword:
            changePassword(email, password, key)
            return redirect(domain + "congratulation?success=changepassword", code=302)
        else:
            msg = "Somthing thing went wrong. Please try again."
            return render_template('404.html',domain = domain, error = "Sorry", h1tag_msg = msg)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080)