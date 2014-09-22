#!/usr/bin/python

import sys, os, urllib2, string, shutil
from bs4 import BeautifulSoup
from os.path import expanduser

url = sys.argv[1]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       }
home = expanduser("~")

if not os.path.exists('%s/8chan' % home):
   os.makedirs('%s/8chan' % home)
       
if not "8chan.co" in url:
   print "Not an 8chan URL"
   sys.exit()

req = urllib2.Request(url, headers=hdr)
page = urllib2.urlopen(req).read()
soup = BeautifulSoup(page)

try:
   sub = soup.find_all(attrs={"class": "subject"})
   sub = str(sub)
   sub = BeautifulSoup(sub)
   topic = sub.span.string
except:
   topic = raw_input('Please specify folder name: ')
	
if not os.path.exists('%s/8chan/%s' %(home, topic)):
   os.makedirs('%s/8chan/%s' %(home, topic))
else:
   shutil.rmtree('%s/8chan/%s' %(home, topic))
   os.makedirs('%s/8chan/%s' %(home, topic))

img = soup.find_all(attrs={"class": "fileinfo"})
img = str(img)

soup = BeautifulSoup(img)
img = soup.find_all('a')

progress = ""
for link in soup.find_all('a'):
   fileinfo = link.get('href')
   dl = 'https://8chan.co%s' % fileinfo
   name = link.string
   req = urllib2.Request(dl, headers=hdr)
   response = urllib2.urlopen(req)
   fh = open('%s/8chan/%s/%s' %(home, topic, name), "wb")
   fh.write(response.read())
   fh.close()
   progress += "|"
   print progress
