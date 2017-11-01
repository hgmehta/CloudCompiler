import requests
from flask import Flask, render_template, json, request
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

compiler_url = 'http://10.20.24.42:5004'
savefile_url = 'http://10.20.24.42:5005'

@app.route('/master', methods=["POST","GET"])
def master():
    jsonRes = request.get_json()
    _type = jsonRes['type']
    code = jsonRes['code']
    language = jsonRes['language']
    inp = jsonRes['input']
    username = jsonRes['username']

    if _type=="compile":
        print 'into compilation'
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
        print str(r.text)
        return str(r.text)
    else:
        print 'savefile'
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
