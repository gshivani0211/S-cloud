#!/usr/bin/python2
print "content-type:text/html\n"
print 
import cgi,commands, mysql.connector as db
data=cgi.FormContent()
user=data['user'][0]
passwd=data['passwd'][0]
email=data['email'][0]
print user
print passwd
print email
x=db.connect(user="root",database="lw")
y=x.cursor()
y.execute("""
	CREATE TABLE IF NOT EXISTS SIGNUP
	(USER char(20) NOT NULL,
	PASSWORD char(20),
	EMAIL char(50),
	 PRIMARY KEY(USER)
	)
""")



y.execute("""
	INSERT INTO SIGNUP (USER,PASSWORD,EMAIL)
	VALUES(%s,%s,%s)
""", (user,passwd,email))

x.commit()
#y.execute('select * from SIGNUP;')
#print y.fetchall()
#x.close()
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/Login.html\">\n"
x.close()

