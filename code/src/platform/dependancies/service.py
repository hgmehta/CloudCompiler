import requests
from flask import request, json
import sys, parse
import socket, ast

from filemanager import *

reload(sys)
sys.setdefaultencoding('utf-8')
master_url = 'http://localhost:5003'

def compile(_code, _language, _username, _input):
    r = requests.post(master_url+'/master', data=json.dumps({'action':'compile', \
                                                            'code':_code, \
                                                            'language':_language, \
                                                            'username': _username, \
                                                            'input':_input}), headers={'Content-Type' : 'application/json'})
    languages = retriveLanguages()
    result = ast.literal_eval(str(r.text))
    exe_time = 0.0
    response = ""
    _cStatus = ""
    _rStatus = ""
    if result['valid_selection']=="False":
        response = "Please select the language from mentioned ones only"
    else:
        if result['compilation_status']=="False":
            _cStatus = "0"
            _rStatus = "-"
            response = result['compilation_error']
        else:
            if result['execution_status']=="False":
                _cStatus = "1"
                _rStatus = "0"
                response = result['execution_error']
            else:
                _cStatus = "1"
                _rStatus = "1"
                exe_time = result['execution_time']
                response = result['execution_output']
    exe_time = round(float(exe_time),5)
    return response, languages, _cStatus, _rStatus, str(exe_time)

def readfile(_language, _username, _filename):
    ip_address = get_ip_from_filename(_language, _username, _filename)
    r = requests.post(master_url+'/master', data=json.dumps({'action':'read', \
                                                            'language':_language, \
                                                            'username': _username, \
                                                            'ip': ip_address, \
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
    response = str(r.text)
    result = parse.parse('{0}&{1}', response)

    _timestamp = result[0]
    _pcip = result[1]
    print "In save file" , _pcip
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