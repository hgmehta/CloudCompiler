import requests
from flask import Flask, render_template, json, request

app = Flask(__name__)

compiler_url = 'http://10.20.24.42:5004'

@app.route('/master', methods=["POST","GET"])
def master():
    jsonRes = request.get_json()
    _type = jsonRes['type']

    if _type=="compile":
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
        print str(r.text)
    else:
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
        print str(r.text)

    return str(r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
