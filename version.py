# -*- coding: utf-8 -*-
# RSScrawler
# Projekt von https://github.com/rix1337

import re
import urllib2


def getVersion():
    return "v.2.9.6"

def updateCheck():
    localversion = getVersion()
    try:
        onlineversion = re.search('return "(v\.\d{1,2}\.\d{1,2}\.\d{1,2})"', urllib2.urlopen('https://raw.githubusercontent.com/rix1337/RSScrawler/master/version.py').read()).group(1)
        if localversion == onlineversion:
            return (False, localversion)
        else:
            return (True, onlineversion)
    except:
        return (False, "Error")