#!/usr/bin/python2
print "content-type:text/html\n"
print 
import cgi,commands, mysql.connector as db
data=cgi.FormContent()
user=data['user'][0]
passwd=data['passwd'][0]
print user
print passwd

x=db.connect(user="root",database="lw")
y=x.cursor()
y.execute('select USER from SIGNUP;')
for row in y.fetchall():
	
	if user==row[0]:
		y.execute("select PASSWORD from SIGNUP where USER='%s';"%(user))
		for row in y.fetchall():
			if passwd==row[0]:
				print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/main.html\">\n"
			else:
				print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/Login.html\">\n"
	else: 
		print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/Login.html\">\n"


x.close()
