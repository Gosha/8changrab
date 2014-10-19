#8chan Grabber

###Dependencies:

* Python2.7
* BeautifulSoup4
* blessings
* docopt

In order to be able to run 8chan Grabber, you'll need to have
BeautifulSoup4 and a few other dependencies installed.  This is easily
done with pip or easy_install:

######For Pip:

`pip install -r requirements.txt`

#####For Easy_install:

`easy_install $(cat requirements.txt)`

###Usage:

```
dl.py [-s SUBJECT] [options] THREAD

-d --directory SAVEPATH  Save images to a directory in SAVEPATH
-s --subject SUBJECT     If set, don't ask for folder name, but directly save
                         in SUBJECT. If not set 8changrab tries the subject
                         of the thread, and asks otherwise.
--workers=<num>          # of processes to spawn [default: 10]

-h --help     Show this
-v --version  Show version
```

`python dl.py [thread url]` should work on most platforms.
