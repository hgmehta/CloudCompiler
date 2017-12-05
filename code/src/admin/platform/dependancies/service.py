import requests
from flask import request, json
import sys, parse
import socket, ast

from filemanager import *

reload(sys)
sys.setdefaultencoding('utf-8')
master_url = 'http://localhost:5003'


def retrieveMonitors():
    languages = []
    try:
        conn = mysql.connector.connect(host='localhost',
                                       port='3306',
                                       database='cloudcompiler',
                                       user='root',
                                       password='lab@cc2')
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT * FROM pcip")
            monitorip = cursor.fetchall()
        # print (monitorip)
    except Error as e:
        print(e)

    finally:
        conn.close()
    return monitorip

def getServerStatisctic():
    pcstrgdetails = []
    pcip = retrieveMonitors()
    for i, ip in enumerate(pcip):
        monitor_details = getMonitorStatus(ip[1])
        ava_storage = int(monitor_details['ava_storage'])
        total_storage = int(monitor_details['total_storage'])
        percent_available = 100 * float((float(ava_storage) / float(total_storage)))
        percent_available = round(percent_available, 2)
        pcstrgdetails.append([ip[1], str(ava_storage), str(percent_available)])
    return pcstrgdetails

def getMonitorStatus(monitorIP): 
    monitorfile_url = 'http://' + str(monitorIP)+":5007"
    r = requests.post(monitorfile_url+'/monitor')
    result = ast.literal_eval(str(r.text))
    return result

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
    suggestion, mem_usage = "", ""
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
                mem_usage = result['memory_usage']
                response = result['execution_output']

        if 'suggestion' in result.keys():
            suggestion = result['suggestion']

        exe_time = round(float(exe_time),5)
    print "Memory Usage :- ", mem_usage
    return response, languages, _cStatus, _rStatus, str(exe_time), str(mem_usage), suggestion

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