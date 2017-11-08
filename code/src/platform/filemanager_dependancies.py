from database_dependancies import *
from flask import session

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

def getLanguageFromType(fileType):
    language = ""
    query = "SELECT _language FROM languages WHERE extension = '" + str(fileType) + "'"
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            for row in rows:
                language = str(row)
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    return language

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

def getPcidFromIP(ip):
    pcid = 1
    print "IP in gtepcid: ", ip 
    query = "SELECT pcid FROM pcip WHERE ip = '" + str(ip) + "'"
    # values = (str(ip))
    try:
        conn = mysql.connector.connect(host='localhost',
                                        port='3306',
                                        database='cloudcompiler',
                                        user='root',
                                        password='lab@cc2')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            for row in rows:
                pcid = int(row)
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()
    print "check IP:" , pcid
    return pcid

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

def get_ip_from_filename(_language, _username, _filename):
    ip_address = ""
    query = "SELECT ip FROM pcip INNER JOIN repository ON repository.pcid = pcip.pcid WHERE filename = %s and username = %s and fileType = %s"
    values = (_filename,_username,_language )
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchone()
            for row in rows:
                ip_address = str(row)
    except Error as error:
        isSuccess = False
        print(error)

    finally:
        cursor.close()
        conn.close()
    return ip_address