#!/usr/bin/python2
print "content-type:text/html\n"
print ""
import cgi,commands
data=cgi.FormContent()
user=data['uname'][0]
size=data['size'][0]
passwd=data['passwd'][0]
print user,size,passwd
commands.getstatusoutput("sudo lvextend --size +{} /dev/myvg/{}".format(size,user))
commands.getstatusoutput("sudo resize2fs /dev/myvg/{}".format(user))

