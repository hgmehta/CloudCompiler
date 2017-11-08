import sqlite3
import datetime
from flask import Flask, render_template, request, redirect, session, json

# connection string for sqlite3
def connectTolog():
    return sqlite3.connect('./../../rec/Database/Logs/log.db')

# Insert user acitivities into activity log
def insertInActivityLog(filename, language, cStatus, rStatus, duration, memUsage, username, sessionId):
    conn = connectTolog()
    time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    conn.execute("INSERT INTO activityLog \
                (username, sessionid, filename, \
                language, time, compilationStatus, runtimeStatus, \
                duration, memUsage) \
                VALUES ('"+ username +"', '"+sessionId+"', '"+filename+"', '"+language+"', '"+time+"', '" + cStatus + "', '" + rStatus + "', '" + duration + "', '" + memUsage + "')")
    conn.commit()
    conn.close()

# Retrieves log activity for user from activity log given sessionID
def getFromActivityLog(sessionId):
    conn = connectTolog()
    cursor = conn.execute("SELECT filename, language, time, \
                        compilationStatus, runtimeStatus, duration, \
                        memUsage from activityLog WHERE sessionid = '" + sessionId +"' ORDER BY id DESC")
    return cursor

# Insert Login actitivity of user into loginLog
def insertInLoginlog(username):

    platform = request.user_agent.platform
    browser = request.user_agent.browser
    ip = request.environ['REMOTE_ADDR']
    time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    conn = connectTolog()
    conn.execute("INSERT INTO loginLog (username, ip, time, browser, Platform, sessionId) \
                VALUES ('" + username + "', '" + ip +  "', '" + time + "' , '" + browser + "', '" + platform +"', '" + session['id'] + "' )")
    conn.commit()
    conn.close()

# Retrieves log actitvity of user
def getFromLoginlog(username):
    conn = connectTolog()
    cursor = conn.execute("SELECT id, username, ip, time, \
                        browser, Platform,sessionid from loginLog WHERE username = '" + username + "' ORDER BY id DESC")
    return cursor