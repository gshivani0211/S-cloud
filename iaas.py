#!/usr/bin/python2

print "content-type:text/html"
print ""
 
import cgi,commands,cgitb,os,random

cgitb.enable()


data=cgi.FormContent()
user=data['user'][0]

cpu=data['cpu'][0]
memory=data['memory'][0]
harddisk=data['harddisk'][0]
vnc=data['vnc'][0]

df=random.randint(5910,5940)
dg=random.randint(6000,7000)
a=commands.getstatusoutput("sudo qemu-img create -f qcow2 /iaas/{0}.qcow2 {1}G".format(user,harddisk))
print a
b=commands.getstatusoutput("sudo virt-install --hvm --name {0} --memory {1} --disk /iaas/{0}.qcow2 --vcpu {2} --cdrom /media/rhel-server-7.2-x86_64-dvd.iso --graphics vnc,listen=0.0.0.0,port={3} --noautoconsole".format(user,memory,cpu,df))
print b


if vnc=="vncviewer":

	print "hello"
	c=commands.getstatusoutput("sudo netstat -tnlp | grep {}".format(df))
	print c
	if c[0] == 0:
		commands.getstatusoutput("sudo touch /media/{}.py".format(user))
		g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
		print g
		fobj=open('/media/{}.py'.format(user), 'a')
		fobj.write("#!/usr/bin/python2\n")
		fobj.write("print 'content-type:text/html'\n")
		fobj.write("print\n")
		fobj.write("import cgi,commands\n")
		fobj.write("commands.getstatusoutput('sudo virt-viewer 192.168.56.101:{}')\n".format(df))
		fobj.write("raw_input() \n")
		fobj.close()
		print g
		commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
		print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/"+user+".tar\">\n"
	else:
		exit
elif vnc=="novnc":
	e=commands.getstatusoutput("sudo  /var/www/cgi-bin/websockify-master/websockify.py -D 192.168.56.101:{0} 192.168.56.101:{1}".format(dg,df))
	print e
	print"<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101:80/vnc/index.html?host=192.168.56.101&port={}\">\n".format(dg)



