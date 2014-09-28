#!/usr/bin/python

import sys, os, urllib2, shutil
from bs4 import BeautifulSoup
from os.path import expanduser

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }


def main(argv):
    url = argv[1]
    home = expanduser("~")

    if not os.path.exists('%s/8chan' % home):
        os.makedirs('%s/8chan' % home)

    if not "8chan.co" in url:
        print "Not an 8chan URL"
        return 1

    req = urllib2.Request(url, headers=HDR)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)

    subject = soup.find(attrs={"class": "subject"})
    if subject:
        topic = subject.string
    else:
        topic = raw_input('Please specify folder name: ')

    if not os.path.exists('%s/8chan/%s' %(home, topic)):
        os.makedirs('%s/8chan/%s' %(home, topic))
    else:
        shutil.rmtree('%s/8chan/%s' %(home, topic))
        os.makedirs('%s/8chan/%s' %(home, topic))

    fileinfos = soup.find_all(attrs={"class": "fileinfo"})

    progress = ""
    for fileinfo in fileinfos:
        for link in fileinfo.find_all('a'):
            fileinfo = link.get('href')
            dl = 'https://8chan.co%s' % fileinfo
            name = link.string
            req = urllib2.Request(dl, headers=HDR)
            response = urllib2.urlopen(req)
            fh = open('%s/8chan/%s/%s' %(home, topic, name), "wb")
            fh.write(response.read())
            fh.close()
            progress += "|"
            print progress

if __name__ == "__main__":
    sys.exit(main(sys.argv))
