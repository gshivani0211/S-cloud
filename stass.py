#!/usr/bin/python2

print "content-type:text/html"
print ""
 
import cgi,commands,cgitb,os

cgitb.enable()


data=cgi.FormContent()
user=data['uname'][0]
size=data['size'][0]
passwd=data['passwd'][0]
service=data['service'][0]
protocol=data['protocol'][0]
print service
print protocol





#block storage code

def block():
	c=commands.getstatusoutput("sudo lvcreate --name {} --size {} myvg".format(user,size))
	print c
	d=commands.getstatusoutput("sudo cd /etc/tgt/conf.d/")
	print d
	l=commands.getstatusoutput("sudo touch {}.conf".format(user)) 
	print l
	commands.getstatusoutput("sudo chmod 777 {}.conf".format(user)) 
	fobj=open("{}.conf".format(user), "a")
	fobj.write('<target {}> \n '.format(user))
	fobj.write("backing-store /dev/myvg/{} \n".format(user))
	fobj.write(" </target>")
	fobj.close()
	commands.getstatusoutput("sudo systemctl restart tgtd")
	
	#client code
	m=commands.getstatusoutput("sudo touch /media/{}.py".format(user))
	print m
	g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
	print g
	fobj=open('/media/{}.py'.format(user), 'a')
	fobj.write("#!/usr/bin/python2\n")
	fobj.write("print 'content-type:text/html'\n")
	fobj.write("print\n")
	fobj.write("import cgi,commands\n")
	fobj.write("commands.getstatusoutput('iscsiadm --mode discoverydb --type sendtargets --portal 	192.168.56.101 --discover')\n")
	fobj.write("commands.getstatusoutput('iscsiadm --mode node --targetname {} --portal 192.168.56.101:3260 --login')\n ".format(user))
	fobj.write("commands.getstatusoutput('iscsiadm --mode node --targetname {} --portal 192.168.56.101:3260 --logout')\n ".format(user))
	fobj.close()
	print "yes"
	k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
	print k
	print "End"
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)



#nfs code

def nfsobj():
	c=commands.getstatusoutput("sudo lvcreate --name {} --size {} myvg".format(user,size))
	print c			
	commands.getstatusoutput("sudo mkfs.ext4 /dev/mapper/myvg-{}".format(user))
	commands.getstatusoutput("sudo mkdir /media/{}".format(user))
			
	a=commands.getstatusoutput("sudo mount /dev/mapper/myvg-{} /media/{}".format(user,user))
	print a
	
	x=commands.getstatusoutput("echo \'/media/{}      *(rw,no_root_squash)\' >>/etc/exports".format(user))
	print x
	commands.getstatusoutput("sudo systemctl restart nfs-utils")
	commands.getstatusoutput("sudo exportfs -r")
	print "succesfully created"

	#client code
	m=commands.getstatusoutput("sudo touch /media/{}.py".format(user))
	print m
	g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
	print g
	fobj=open('/media/{}.py'.format(user), 'a')
	fobj.write("#!/usr/bin/python2\n")
	fobj.write("print 'content-type:text/html'\n")
	fobj.write("print\n")
	fobj.write("import cgi,commands\n")
	fobj.write("commands.getstatusoutput('mkdir /media/{}')\n".format(user))
	fobj.write("commands.getstatusoutput('mount 192.168.56.101:/media/{} /media/{}')\n".format(user,user))
	fobj.close()
	print "yes"
	k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
	print k
	print "End"
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)


#sshfs code
def sshfsobj():
	c=commands.getstatusoutput("sudo lvcreate --name {} --size {} myvg".format(user,size))
	print c			
	commands.getstatusoutput("sudo mkfs.ext4 /dev/mapper/myvg-{}".format(user))
	commands.getstatusoutput("sudo mkdir /media/{}".format(user))
			
	a=commands.getstatusoutput("sudo mount /dev/mapper/myvg-{} /media/{}".format(user,user))
	print a
	commands.getstatusoutput("sudo systemctl restart sshd")
	commands.getstatusoutput("sudo useradd {}".format(user))
	commands.getstatusoutput("sudo echo {} | passwd {} --stdin".format(passwd,user))
	commands.getstatusoutput("sudo chown {} /dev/myvg/{}".format(user,user))
	commands.getstatusoutput("sudo 700 /dev/myvg/{}".format(user))

	#client code

	m=commands.getstatusoutput("sudo touch /media/{}.py".format(user))
	print m
	g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
	print g
	fobj=open('/media/{}.py'.format(user), 'a')
	fobj.write("#!/usr/bin/python2\n")
	fobj.write("print 'content-type:text/html'\n")
	fobj.write("print\n")
	fobj.write("import cgi,commands\n")
	fobj.write("commands.getstatusoutput('mkdir /media/{}')\n".format(user))
	fobj.write("commands.getstatusoutput('sshfs {}@192.168.56.101:/dev/myvg{} /media/{}')\n".format(user,user,user))
	fobj.close()
	print "yes"
	k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
	print k
	print "End"
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)

#samba code
def samba():

	c=commands.getstatusoutput("sudo lvcreate --name {} --size {} myvg".format(user,size))
	print c			
	commands.getstatusoutput("sudo mkfs.ext4 /dev/mapper/myvg-{}".format(user))
	commands.getstatusoutput("sudo mkdir /media/{}".format(user))
			
	a=commands.getstatusoutput("sudo mount /dev/mapper/myvg-{} /media/{}".format(user,user))
	print a
	commands.getstatusoutput("sudo yum install samba*")
	commands.getstatusoutput("sudo useradd -s /sbin/nologin {}".format(user))
	commands.getstatusoutput("echo -e '{0}\n{0}' | sudo smbpasswd -a {1}".format(passwd,user))
	commands.getstatusoutput("sudo chmod 777 /etc/samba/smb.conf")

	fh=open("/etc/samba/smb.conf", "a")
	fh.write("[{}] \n".format(user))
	fh.write("path=/dev/myvg/{}\n".format(user))
	fh.write("writable=yes\n")
	fh.write("valid users={}\n".format(user))
	fh.write("hosts allow=ALL\n")
	fh.close()
	commands.getstatusoutput("sudo systemctl restart smb")
	commands.getstatusoutput("sudo systemctl enable smb")

	#client code
	m=commands.getstatusoutput("sudo touch /media/{}.py".format(user))
	print m
	g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
	print g


	fobj=open('/media/{}.py'.format(user), 'a')
	fobj.write("#!/usr/bin/python2\n")
	fobj.write("print 'content-type:text/html'\n")
	fobj.write("print\n")
	fobj.write("import cgi,commands\n")
	fobj.write("commands.getstatusoutput('mkdir /media/{}')\n".format(user))
	fobj.write("commands.getstatusoutput('mount -o username={} //127.0.0.1/{} /media/{}')\n".format(user,user,user))
	fobj.close()
	print "yes"
	k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
	print k
	print "End"
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)








if service=="object":
	if protocol=="nfs":
		nfsobj()
	elif protocol=="sshfs":
		sshfsobj()
	else:
		samba()
else:
	block()





