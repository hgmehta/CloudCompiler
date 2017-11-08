# def temp():
#     platform = request.user_agent.platform
#     browser = request.user_agent.browser
#     ip = request.environ['REMOTE_ADDR']
#     conn = sqlite3.connect('log.db')
#     time = str()
#     # conn.execute('''CREATE TABLE loginLog
#     #      (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     #      username VARCHAR(15)    NOT NULL,
#     #      ip VARCHAR(20) NOT NULL,
#     #      time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#     #      browser VARCHAR(15) NOT NULL,
#     #      Platform VARCHAR(15) NOT NULL);''')
#     # conn.execute("INSERT INTO loginLog (username,ip,browser,Platform) \
#     #   VALUES ('" + session['username'] + "', '" + ip +  "', '" + browser + "', '" + platform +"' )")
#     cursor = conn.execute("SELECT id, username, ip, time,browser,Platform from loginlog")
#     for row in cursor:
#         print "ID = ", row[0]
#         print "User name = ", row[1]
#         print "Ip = ", row[2]
#         print "Time = ", row[3]
#         print "Browser = ", row[4]
#         print "Platform = ", row[5], "\n"

#     # cursor = conn.execute("SELECT id, username, ip, time,browser,Platform from loginlog")
#     # for row in cursor:
#     #     print "ID = ", row[0]
#     #     print "User name = ", row[1]
#     #     print "Ip = ", row[2]
#     #     print "Time = ", row[3]
#     #     print "Browser = ", row[4]
#     #     print "Platform = ", row[5], "\n"
#     # conn.execute("DELETE from loginlog where ID = 1;")
#     # conn.commit()
#     print "Operation done successfully"
#     conn.close()


#     {% for row in activities %}
#                         <tr>
#                             <td>{{row[0]}}</td>
#                             <td>{{row[2]}}</td>
#                             <td>{{row[5]}}</td>
#                             <td>{{row[4]}}</td>
#                             <td>{{row[3]}}</td>
#                             <td>
#                                 <button type="button" class="btn btn-icon" aria-label="Product details">
#                                     <i class="icon icon-dots-horizontal s-4"></i>
#                                 </button>
#                             </td>
#                         </tr>
#                     {% endfor %}
# import hashlib
# import datetime
# import random

# m = hashlib.md5()
# num = str(random.randint(1,10000))
# string = str(datetime.datetime.now()) + num
# #d = bytes(str(datetime.datetime.now()),'utf-8')
# d = bytes(string)
# m.update(d)
# key = m.hexdigest()
# print key

# conn.execute("ALTER TABLE loginlog ADD COLUMN sessionID VARCHAR(35);")
#     conn.commit()
#     print "Operation done successfully"

# Allactivities = [list(i) for i in Allactivities]
# for row in Allactivities:
#     row[0] = count
#     count = count + 1

# conn.execute('''CREATE TABLE activityLog
#                     (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     username VARCHAR(15) NOT NULL,
#                     sessionid VARCHAR(35) NOT NULL,
#                     filename VARCHAR(25),
#                     language VARCHAR(10),
#                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
#                     compilationStatus VARCHAR(1),
#                     runtimeStatus VARCHAR(1),
#                     duration VARCHAR(15),
#                     memUsage VARCHAR(15) NOT NULL);''')