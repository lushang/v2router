#!/usr/bin/env python  
#coding=utf-8
#  
# Generate a list of dnsmasq rules with ipset for gfwlist
#  
# Copyright (C) 2014 http://www.shuyz.com   
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules    
 
import sys
py_version = sys.version_info[0]

import urllib.request
import re
import os
import datetime
import base64
#import shutil
 
mydnsip = '127.0.0.1'
mydnsport = '7913'

if len(sys.argv) != 2:
    print("fwlist.py outfile.txt")
    sys.exit(-1)

outfile = sys.argv[1]
 
# the url of gfwlist
# baseurl = 'https://raw.githubusercontent.com/Loukky/gfwlist-by-loukky/master/gfwlist.txt'
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# baseurl = 'https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*' 
tmpfile = '/tmp/gfwlisttmp'
# do not write to router internal flash directly
#outfile = '/tmp/gfwlist.conf'
#rulesfile = '/etc/dnsmasq.d/gfwlist.conf'
 
print('fetching list...')
if py_version == 2:
    content = urllib.request.urlopen(baseurl, timeout=15).read().decode('base64')
else:
    content = urllib.request.urlopen(baseurl, timeout=15).read()
# content = urllib2.urlopen(baseurl, timeout=15).read().decode('base64')
 
# write the decoded content to file then read line by line
lines = base64.b64decode(content).decode('utf-8')

print('page content fetched, analysis...')

# remember all blocked domains, in case of duplicate records
domainlist = []

fs = open(outfile, 'w')

for line in lines.split('\n'):
    if re.findall(comment_pattern, line):
        #print 'this is a comment line: ' + line
        #fs.write('#' + line)
        pass
    else:
        domain = re.findall(domain_pattern, line)
        if domain:
            try:
                found = domainlist.index(domain[0])
                #print domain[0] + ' exists.'
            except ValueError:
                #print 'saving ' + domain[0]
                domainlist.append(domain[0])
                fs.write('server=/.%s/%s#%s\n'%(domain[0],mydnsip,mydnsport))
                fs.write('ipset=/.%s/gfwlist\n'%domain[0])
#                 fs.write('%s\n'%domain[0])
        else:
            print('no valid domain in this line: ',line)
                    
fs.close()
 
#print 'moving generated file to dnsmasg directory'
#print outfile
#shutil.move(outfile, rulesfile)
 
#print 'restart dnsmasq...'
#print os.popen('/etc/init.d/dnsmasq restart').read()
 
print('saving to file: ', outfile)
print('done!')
