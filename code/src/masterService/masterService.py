import requests
from flask import Flask, render_template, json, request

app = Flask(__name__)

compiler_url = 'http://localhost:5004'

@app.route('/master', methods=["POST","GET"])
def master():
    jsonRes = request.get_json()
    code = jsonRes['code']
    language = jsonRes['language']
    inp = jsonRes['input']

    userID = '123'
    filename = 'example'
    language = str(language.decode('utf-8'))
    code = str(code.decode('utf-8'))
    inp = str(inp.decode('utf-8'))

    r = requests.post(compiler_url+'/compile', data=json.dumps({'getCode':code, 'type':language, 'input':inp, 'userid':userID,'filename':filename}), \
    											headers={'Content-Type' : 'application/json'})
    print str(r.text)

    return str(r.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
