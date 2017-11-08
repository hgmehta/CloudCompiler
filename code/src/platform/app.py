import requests
import sys, parse
import hashlib
import datetime
import base64
import random
import socket, ast
from uuid import getnode

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./models')

from flask import Flask, render_template, request, redirect, session, json
from authenticateModel import *
from werkzeug import generate_password_hash, check_password_hash
from email_pyfile import *
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc'

hostname = socket.gethostname()
AppAddress = socket.gethostbyname(hostname)
port = 8080
domain = "http://" + AppAddress + ":" + str(port) + "/"

master_url = 'http://localhost:5003'

def connectTolog():
    return sqlite3.connect('./../../rec/Database/Logs/log.db')

@app.route('/temp')
def temp():
    conn = connectTolog()
    conn.execute("DELETE from loginlog where ID = 6;")
    conn.commit()
    conn.close()
    return "Connected Database"

def insertInLoginlog(username):

    platform = request.user_agent.platform
    browser = request.user_agent.browser
    ip = request.environ['REMOTE_ADDR']
    time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    conn = connectTolog()
    conn.execute("INSERT INTO loginLog (username,ip,time,browser,Platform,sessionId) \
                    VALUES ('" + username + "', '" + ip +  "', '" + time + "' , '" + browser + "', '" + platform +"', '" + session['id'] + "' )")
    conn.commit()
    conn.close()

def getFromLoginlog(username):
    conn = connectTolog()
    cursor = conn.execute("SELECT id, username, ip, time, browser, Platform,sessionid from loginLog WHERE username = '" + username + "'")
    return cursor

@app.route('/<username>/activity', methods = ['GET'])
def loginActivity(username):
    if 'username' in session:
        if session['username'] == username:
            if 'id' in request.args:
                if len(request.args.get('id')) != 32:
                    return "Sorry"
                else:
                    return request.args.get('id')
            else:
                Allactivities = list(getFromLoginlog(session['username']))
                return render_template('LoginActivity.html', domain = domain, username = session['username'], activities = Allactivities)
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
        responce, languages = compile(_code, _language, _username, _input)
        return render_template('_CodeEditor.html',domain = domain,username = 'guest',languages = languages, output = responce, code = _code, input = _input, language = _language)
    else:
        languages = retriveLanguages()
        return render_template('_CodeEditor.html',domain = domain, languages = languages)

def createHTMLString(string):
    string = string.replace("\r\n", "<br />")
    return string.replace("\n", "<br />")

@app.route('/perform',methods=['POST'])
def perform():
    if "compile" in request.form:
        return redirect(domain + "compile",code = 307)
    elif "save" in request.form:
        return redirect(domain + "savefile",code = 307)

def retriveFolders():
    rows = []
    conn = createConnection()
    try:
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT DISTINCT _language,TO_BASE64(fileType) FROM repository INNER JOIN languages ON languages.extension = repository.fileType WHERE username = %s", (session['username'],))
            rows = cursor.fetchall()
            rows = [list(i) for i in rows]
        for row in rows:
            row.append('Folder')
            row.append(session['username'])
            row.append('Size')
            row.append('time')
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return rows

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
            cursor.execute("SELECT filename, TO_BASE64(filename), fileType, '" + session['username'] + "' , 'Size' , date(timeCreated),icon FROM repository INNER JOIN languages ON languages.extension = repository.fileType WHERE username = %s AND filetype = %s", (session['username'],filetype_decoded,))
            rows = cursor.fetchall()
            rows = [list(i) for i in rows]
            return render_template('FileManager.html',folder = lang,domain = domain,username = session['username'], links = rows)

def getLanguageFromFileType(filetype):
    language = ""
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT DISTINCT _language FROM languages WHERE extension = %s",(filetype,))
            l = cursor.fetchone()
            for lang in l:
                language = str(lang)

    except Error as e:
        print(e)

    finally:
        conn.close()

    return language

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
                    return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages)
            else:
                return redirect(domain, code=302)
        else:
            code = readfile(filetype,session['username'],base64.b64decode(filename))
            languages = retriveLanguages()
            return render_template('_CodeEditor.html',domain = domain,language = filetype,code = code,username = session['username'],languages = languages)
    elif request.method == 'POST':
        _code = request.form['code']
        _language = request.form['language']
        _input = request.form['input']
        _username = 'guest'
        print request.environ['REMOTE_ADDR']
        if "compile" in request.form:
            if 'username' in session:
                _username = session['username']
            responce, languages = compile(_code, _language, _username, _input)
            return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages, output = responce, code = _code, input = _input, language = _language)
        else:
            _filename = request.form['filename']
            _username = session['username']
            output, languages = savefile(_code, _language, _input, _filename, _username)
            return render_template('_CodeEditor.html',domain = domain,username = session['username'],languages = languages, output = output, code = _code, input = _input, language = _language)

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

def getTotalFileNo():
    fileno = []
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT DISTINCT _language, COUNT(fileType), icon,TO_BASE64(fileType) FROM repository INNER JOIN languages ON repository.fileType = languages.extension GROUP BY fileType")
            fileno = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        conn.close()

    return fileno

def compile(_code, _language, _username, _input):
    r = requests.post(master_url+'/master', data=json.dumps({'action':'compile', \
                                                            'code':_code, \
                                                            'language':_language, \
                                                            'username': _username, \
                                                            'input':_input}), headers={'Content-Type' : 'application/json'})

    languages = retriveLanguages()
    result = ast.literal_eval(str(r.text))
    responce = ""
    if result['valid_selection']=="False":
        responce = "Please select the language from mentioned ones only"
    else:
        if result['compilation_status']=="False":
            responce = result['compilation_error']
        else:
            if result['execution_status']=="False":
                responce = result['execution_error']
            else:
                exe_time = result['execution_time']
                responce = result['execution_output']

    return responce, languages

def readfile(_language, _username, _filename):
    r = requests.post(master_url+'/master', data=json.dumps({'action':'read', \
                                                            'language':_language, \
                                                            'username': _username, \
                                                            'filename':_filename}), headers={'Content-Type' : 'application/json'})
    return str(r.text)

def savefile(_code,_language,_input,_filename,_username):
    r = requests.post(master_url+'/master', data=json.dumps({'action': 'savefile', \
                                                            'code': _code,\
                                                            'language': _language, \
                                                            'input': _input, \
                                                            'filename': _filename, \
                                                            'username': _username}), \
                                                            headers={'Content-Type' : 'application/json'})
    responce = str(r.text)
    result = parse.parse('{0}&{1}', responce)

    _timestamp = result[0]
    _pcip = result[1]
    _pcid = getPcidFromIP(_pcip)

    query = "INSERT INTO repository (filename,username,fileType, timeCreated, pcid)" \
            " VALUES(%s,%s,%s,%s,%s)"
    values = (_filename,_username,_language,_timestamp, _pcid)
    isSuccess = True
    try:
        conn =createConnection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
        else:
            isSuccess = False
    except Error as error:
        isSuccess = False
        print(error)

    finally:
        cursor.close()
        conn.close()

    languages = retriveLanguages()
    if isSuccess:
        output = 'Your code is saved successfully.'
    else:
        output = 'Please try again.'

    return output, languages


def getPcidFromIP(ip):
    pcid = 1
    query = "SELECT pcid FROM pcip WHERE ip = %s"
    values = (ip)
    try:
        conn = mysql.connector.connect(host='localhost',
                                        port='3306',
                                        database='cloudcompiler',
                                        user='root',
                                        password='lab@cc2')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchone()
            for row in rows:
                pcid = int(row)
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    return pcid

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

def retriveLanguages():
    languages = []
    try:
        conn = mysql.connector.connect(host='localhost',
                                       port='3306',
                                       database='cloudcompiler',
                                       user='root',
                                       password='lab@cc2')
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT * FROM languages")
            languages = cursor.fetchall()

    except Error as e:
        print(e)

    finally:
        conn.close()

    return languages

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080)
