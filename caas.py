#!/usr/bin/python2

print "content-type:text/html"
print ""
 
import cgi,commands,cgitb,os,time

cgitb.enable()


data=cgi.FormContent()
user=data['user'][0]
passwd=data['passwd'][0]

no=data['no'][0]
print user

print passwd
print no
commands.getstatusoutput("sudo touch /caas/{}.sh".format(user))
commands.getstatusoutput("sudo chmod 777 /caas/{}.sh".format(user))
f=open("/caas/{}.sh".format(user),"w")
f.write("#!/bin/bash\nuseradd {0}\necho  {0} | passwd {1} --stdin\n".format(passwd,user))
f.close()
print "yes"
port=5290
i=1

while i<=int(no) :
	p=commands.getstatusoutput("sudo docker run -itd -p {}:4200 --privileged -v /caas:/media/caas rahul1 /bin/bash".format(port))
	print p
	commands.getstatusoutput("sudo docker exec {} /media/caas/{}.sh".format(p[1],user))
	
	v=commands.getstatusoutput("sudo docker exec {} hostname -i".format(p[1]))
	print v
	commands.getstatusoutput("sudo docker exec {} sed -Ei 's/172.17.0.2/{}/g' /etc/sysconfig/shellinaboxd".format(p[1],v[1]))
	time.sleep(5)	

	k=commands.getstatusoutput("sudo docker exec -t {} service sshd restart".format(p[1]))	
	print k
	
	c=commands.getstatusoutput("sudo docker exec -t {} service shellinaboxd restart".format(p[1]))
	print c
	commands.getstatusoutput("sudo docker exec -t {} service shellinaboxd restart".format(p[1]))
	commands.getstatusoutput("sudo touch /var/www/html/{}.html".format(user))
	commands.getstatusoutput("sudo chmod 777 /var/www/html/{}.html".format(user))	
	f1=open('/var/www/html/{}.html'.format(user),"a")
	f1.write("<a href='http://192.168.56.101:{}' target='_blank'>docker</a>\n".format(port))
	f1.close()
	print "end"
	port=port+1
	i=i+1
	
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.html\">\n".format(user)
