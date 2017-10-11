import requests
from flask import Flask, render_template, json, request
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

master_url = 'http://localhost:5003'

@app.route('/')
def main():
    return render_template('index.html')

def createHTMLString(string):
    string = string.replace("\r\n", "<br />")
    return string.replace("\n", "<br />")

@app.route('/postCode',methods=['POST','GET'])
def signUp():
    _code = request.form['code']
    _language = request.form['language']
    _input = request.form['input']

    # validate the received values
    print _code
    print _language
    print _input

    r = requests.post(master_url+'/master', data=json.dumps({'code':_code, 'language':_language, 'input':_input}), headers={'Content-Type' : 'application/json'})
    responce = str(r.text)

    return json.dumps({'compilation_res':createHTMLString(responce)})

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8080)
