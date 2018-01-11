#!/usr/bin/env python
# -*- coding: utf-8 -*-
# target router -change details to yours please
from __future__ import unicode_literals
import urllib2
import re
import lxml.html as lh

rooturl="" # add your own admin url of the router 
username = 'admin'
password = 'password'

# create a urllib2 opener for basic authentication
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, rooturl, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

#get self ip
devhandle= urllib2.urlopen(rooturl+'/DEV_device.htm')
devcontent=devhandle.read()
devdoc= lh.document_fromstring(devcontent)
devhandle.close()
devs=[i.text_content() for i in devdoc.xpath("//span")]
devs=zip(*[devs[i::4] for i in xrange(1,4)])
myips=[]
othernames={}
for i in devs[1:]:
    if 'fclef' in i[1].lower(): # fclef is my computer name
        myips.append(i[0])
    else:
        othernames[i[0]]=i[1]

#refresh log, a post method
urllib2.urlopen(rooturl+'/fwLog.cgi','log_detail=&action_Refresh=%CB%A2%D0%C2&email_on=0&log_refresh=1&log_send=0&log_clear=0')

#get log
pagehandle = urllib2.urlopen(rooturl+'/fwLog.cgi')
content=pagehandle.read()
pagehandle.close()
doc=lh.document_fromstring(content)
logs=doc.xpath("//textarea")[0].text_content()
ptn=re.compile('^\[(.+): (.+)\] Source: ([0-9\.]{11,15})')
for i in [i for i in logs.split('\r\n') if i]:
    loginfo=re.search(ptn,i).groups()
    if loginfo[2] not in myips:
        print '{0[2]}({1}) {0[0]} {0[1]}'.format(loginfo,othernames.get(loginfo[2]))

#clear log
urllib2.urlopen(rooturl+'/fwLog.cgi','log_detail=&action_Clear=%C7%E5%BF%D5%C8%D5%D6%BE&email_on=0&log_refresh=0&log_send=0&log_clear=1')
