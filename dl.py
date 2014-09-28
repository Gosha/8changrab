#!/usr/bin/env python

from __future__ import print_function
import sys, os, urllib2, shutil
from bs4 import BeautifulSoup
from os.path import expanduser

try:
    from blessings import Terminal
    def update_progress(current, total):
        """Create a pretty progress bar by constantly updating one line"""
        progress_bar_length = 40

        percent_finished = current/float(total) # 0 -> 1

        fillers = int(percent_finished * progress_bar_length)
        empty_fillers = progress_bar_length - fillers

        progress_bar = "["
        progress_bar += fillers*"="
        progress_bar += ">"
        progress_bar += empty_fillers*" "
        progress_bar += "]"

        term = Terminal()
        with term.location(x=0):
            print("{} {}/{}".format(progress_bar, current, total), end="")
        sys.stdout.flush()
except ImportError:
    def update_progress(current, total):
        """Simple update progress"""
        sys.stdout.write("|")
        sys.stdout.flush()

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

def download_image(link, filename):
    """Download LINK to FILENAME"""
    req = urllib2.Request(link, headers=HDR)
    response = urllib2.urlopen(req)
    with open(filename, "wb") as _file:
        _file.write(response.read())
        _file.close()

def main(argv):
    """Usage: dl.py THREAD"""
    try:
        url = argv[1]
    except:
        print ("No URL supplied")
        print ("Usage: %s [Thread URL]" % argv[0])
        return 1

    home = expanduser("~")

    if not os.path.exists('%s/8chan' % home):
        os.makedirs('%s/8chan' % home)

    if not "8chan.co" in url:
        print("Not an 8chan URL")
        return 1

    req = urllib2.Request(url, headers=HDR)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)

    subject = soup.find(attrs={"class": "subject"})
    if subject:
        topic = subject.string
    else:
        topic = raw_input('Please specify folder name: ')

    download_path = '%s/8chan/%s' % (home, topic)

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    else:
        shutil.rmtree(download_path)
        os.makedirs(download_path)

    fileinfos = soup.find_all(attrs={"class": "fileinfo"})
    fileinfos_count = len(fileinfos)
    current_fileinfo = 1
    for fileinfo in fileinfos:
        for link in fileinfo.find_all('a'):
            fileinfo = link.get('href')
            download_link = 'https://8chan.co%s' % fileinfo
            download_image(download_link, '%s/%s'
                           %(download_path, link.string))
            update_progress(current_fileinfo, fileinfos_count)
        current_fileinfo += 1
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
