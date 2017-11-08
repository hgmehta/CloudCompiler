import requests
from flask import Flask, render_template, json, request
import sys
import ast

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

compiler_url = 'http://10.20.24.42:5004'
savefile_url = 'http://10.20.24.42:5005'
readfile_url = 'http://10.20.24.42:5006'

def getMonitorStatus(monitorIP):
    monitorfile_url = 'http://' + str(monitorIP)+":5007"
    r = requests.post(monitorfile_url+'/monitor')
    result = ast.literal_eval(str(r.text))
    return result

@app.route('/master', methods=["POST","GET"])
def master():
    jsonRes = request.get_json()
    print request.remote_addr
    _action = jsonRes['action']

    if _action=="compile":
        code = jsonRes['code']
        language = jsonRes['language']
        inp = jsonRes['input']
        username = jsonRes['username']
        filename = 'example'
        language = str(language.decode('utf-8'))
        code = str(code.decode('utf-8'))
        inp = str(inp.decode('utf-8'))

        r = requests.post(compiler_url+'/compile', data=json.dumps({'getCode':code, \
                                                                    'type':language, \
                                                                    'input':inp, \
                                                                    'userid':username, \
                                                                    'filename':filename}), \
                                                                    headers={'Content-Type' : 'application/json'})
        return r.text

    elif _action=="savefile":
        code = jsonRes['code']
        language = jsonRes['language']
        inp = jsonRes['input']
        username = jsonRes['username']
        filename = jsonRes['filename']
        language = str(language.decode('utf-8'))
        code = str(code.decode('utf-8'))
        inp = str(inp.decode('utf-8'))

        r = requests.post(savefile_url+'/savefile', data=json.dumps({'getCode':code, \
                                                                    'type':language, \
                                                                    'input':inp, \
                                                                    'userid':username, \
                                                                    'filename':filename}), \
                                                                    headers={'Content-Type' : 'application/json'})
        return '{0}&{1}'.format(str(r.text), '10.20.24.42')
    elif _action=="read":
        language = jsonRes['language']
        username = jsonRes['username']
        filename = jsonRes['filename']
        r = requests.post(readfile_url+'/readfile', data=json.dumps({'type':language, \
                                                                    'userid':username, \
                                                                    'filename':filename}), \
                                                                    headers={'Content-Type' : 'application/json'})
        print str(r.text)
        return str(r.text)
    else:
        return "Sorry, wrong request"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
