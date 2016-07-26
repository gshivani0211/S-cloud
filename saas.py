#!/usr/bin/python2
print "content-type:text/html\n"
print 

import cgi,commands,cgitb,os
cgitb.enable()

data=cgi.FormContent()
user=data['user'][0]
passwd=data['passwd'][0]
sname=data['Software'][0]

print user,passwd,sname

a=commands.getstatusoutput("sudo yum install openssh-server")
print a
c=commands.getstatusoutput("sudo systemctl restart sshd")
print c
d=commands.getstatusoutput("sudo useradd {}".format(user))
print d
e=commands.getstatusoutput("sudo echo {} | passwd {} --stdin".format(passwd,user))
print e


commands.getstatusoutput("sudo touch /media/{}.py".format(user))
commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
fobj=open('/media/{}.py'.format(user), 'a')
fobj.write("#!/usr/bin/python2\n")
fobj.write("import commands,cgitb,os \n")
fobj.write("commands.getstatusoutput('ssh -X {}@192.168.56.101 {}')\n".format(user,sname))
fobj.close()
k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
print k
print "End"
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)
