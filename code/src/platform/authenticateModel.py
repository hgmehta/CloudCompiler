import mysql.connector
from mysql.connector import Error
import datetime
from database_dependancies import *

def validateRegistration(email,username,password,confirmpassword):    
    errors = []
    if isRegistered("email", email):
        errors.append("Email Id is already registered")
    if isRegistered("username", username):
        errors.append("Username is already registered")
    return errors

def validateLogin(email,password):
    errors = []
    isMatched = 0
    if isRegistered("email",email) == False:
        errors.append("Email id is not registered");
    elif isAccountVarified(email) == 0:
        errors.append("Before Login Please varify your email account")
    else:
        query = "SELECT COUNT(email) FROM users WHERE email = %s AND password = %s"
        values = (email,password)
        try:
            conn = createConnection()
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(query, values)
                rows = cursor.fetchone()
                for row in rows:
                    isMatched = int(row)
                if isMatched != 1:
                    errors.append("Email id or password is wrong")
        except Error as error:
            isSuccess = False
            print(error)

        finally:
            cursor.close()
            conn.close()
    return errors

def register(email,username,password,key):
    query = "INSERT INTO users (email,username,password,activation_key)" \
            " VALUES(%s,%s,%s,%s)"
    values = (email,username,password,key)
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
    return isSuccess

def isRegistered(dbfield, formcontent):
    registered = False
    noOfUsers = 0
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT COUNT(" + dbfield + ") FROM users WHERE " + dbfield +" = %s", (formcontent,))
            rows = cursor.fetchone()
            for row in rows:
                noOfUsers = int(row)
            if noOfUsers == 0:
                registered = False
            else:
                registered = True

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return registered

def getActivationKey(email):
    key = ""
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT activation_key FROM users WHERE email = %s", (email,))
            rows = cursor.fetchone()
            for row in rows:
                key = str(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return key

def activateEmail(email):
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("UPDATE users SET isEmailVerified = '1' WHERE email = %s", (email,))
            conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def isAccountVarified(email):
    isVarified = 0
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT isEmailVerified FROM users WHERE email = %s", (email,))
            rows = cursor.fetchone()
            for row in rows:
                isVarified = int(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return isVarified


def forgotPasswordDetails(email, key):
    try:
        conn = createConnection()
        query = "INSERT INTO forgotPassword(email,password_key) VALUES(%s,%s)"
        values = (email, key)
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute(query, values)
            conn.commit()
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def getKeyForChangePassword(email):
    key = ""
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT password_key FROM forgotPassword WHERE email = %s", (email,))
            rows = cursor.fetchone()
            for row in rows:
                key = str(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return key

def isKeyExpired(email):
    isKeyExpired = 0;
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT isLinkActive FROM forgotPassword WHERE email = %s", (email,))
            rows = cursor.fetchone()
            for row in rows:
                isKeyExpired = int(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return isKeyExpired

def changePassword(email, password, key):
    time = str(datetime.datetime.now())
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("UPDATE forgotPassword SET isLinkActive = '0', isPasswordChanged = '1',"\
                "timeChanged = %s WHERE email = %s AND password_key = %s", (time,email,key,))
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (password,email,))
            conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def getUsernameFromEmail(email):
    username = ""

    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT username FROM users WHERE email = %s", (email,))
            rows = cursor.fetchone()
            for row in rows:
                username = str(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return username