from database import *
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
        print("Sorry, we are Unable to get your files..!")

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

def getTotalFileNo(username):
    fileno = []
    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT DISTINCT _language, COUNT(fileType), icon,TO_BASE64(fileType) FROM repository INNER JOIN languages ON repository.fileType = languages.extension WHERE username = '" + username + "' GROUP BY fileType")
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
        conn = createConnection()
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
        conn = createConnection()
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

def pagination(_id, limit, filetype):
    query = "SELECT filename, TO_BASE64(filename), fileType, '" + session['username'] + "' , 'Size' , date(timeCreated),icon,pcid FROM repository INNER JOIN languages ON languages.extension = repository.fileType WHERE username = %s AND filetype = %s AND id < %s ORDER BY repository.id DESC LIMIT %s"
    values = (session['username'], filetype, _id, limit)
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

    return cursor

def totalfile(filetype):
    count = 0
    query = "SELECT COUNT(*) FROM repository WHERE filetype = %s AND username = %s"
    values = (filetype, session['username'])

    try:
        conn = createConnection()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, values)
            rows = cursor.fetchone()
            for row in rows:
                count = int(row)
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

    return count

def retrievefiles(username, filetype):
    conn = createConnection()
    try:
        if conn.is_connected():
            cursor = conn.cursor();
            cursor.execute("SELECT filename, TO_BASE64(filename), fileType, '" + username + "' , 'Size' , \
                            date(timeCreated),icon,pcid, id \
                            FROM repository INNER JOIN languages \
                            ON languages.extension = repository.fileType \
                            WHERE username = %s AND filetype = %s \
                            ORDER BY repository.id DESC",(username, filetype,))
            rows = cursor.fetchall()
            rows = [list(i) for i in rows]
            return  rows
            return render_template('FileManager.html', folder=lang, domain=domain, username=session['username'],
                                   links=rows)
    except Error as e:
        print("Sorry, we are unable to retrive your files..!")