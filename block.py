#!/usr/bin/python2

print "content-type:text/html \n"
#print ""
 
import cgi,commands,cgitb,os

cgitb.enable()


data=cgi.FormContent()
user=data['user'][0]
size=data['size'][0]
passwd=data['passwd'][0]


print user
print size
print passwd

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


m=commands.getstatusoutput("sudo touch /media/{}.py".format(user))
print m
g=commands.getstatusoutput("sudo chmod 777 /media/{}.py".format(user))
print g
fobj=open('/media/{}.py'.format(user), 'a')
fobj.write("#!/usr/bin/python2\n")
fobj.write("print 'content-type:text/html'\n")
fobj.write("print\n")
fobj.write("import cgi,commands\n")
fobj.write("commands.getstatusoutput('iscsiadm --mode discoverydb --type sendtargets --portal 192.168.56.101 --discover')\n")
fobj.write("commands.getstatusoutput('iscsiadm --mode node --targetname {} --portal 192.168.56.101:3260 --login')\n ".format(user))
fobj.close()
print "yes"
k=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}.tar /media/{}.py".format(user,user))
print k
print "End"
print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.56.101/{}.tar\">\n".format(user)



