# -*- coding: utf-8 -*-
# RSScrawler
# Projekt von https://github.com/rix1337
# Enthält Code von:
# https://github.com/bharnett/Infringer/blob/master/LinkRetrieve.py

import files
import logging
import os
import re
import socket
import sys
from rssconfig import RssConfig

log_info = logging.info
log_error = logging.error
log_debug = logging.debug
    
def write_crawljob_file(package_name, folder_name, link_text, crawljob_dir, subdir):
    crawljob_file = crawljob_dir + '/%s.crawljob' % unicode(re.sub('[^\w\s\.-]', '', package_name.replace(' ', '')).strip().lower())
    crawljobs = RssConfig('Crawljobs')
    autostart = crawljobs.get("autostart")
    usesubdir = crawljobs.get("subdir")
    if usesubdir == "False":
      subdir = ""
    if autostart == "True":
        autostart = "TRUE"
    else:
        autostart = "FALSE"
    try:
        file = open(crawljob_file, 'w')
        file.write('enabled=TRUE\n')
        file.write('autoStart=' + autostart + '\n')
        file.write('extractPasswords=["' + "bW92aWUtYmxvZy5vcmc=".decode('base64') + '","' + "c2VyaWVuanVua2llcy5vcmc=".decode('base64') + '","' + "aGQtYXJlYS5vcmc=".decode('base64') + '","' + "aGQtd29ybGQub3Jn".decode('base64') + '","' + "d2FyZXotd29ybGQub3Jn".decode('base64') + '"]\n')
        file.write('downloadPassword=' + "c2VyaWVuanVua2llcy5vcmc=".decode('base64') + '\n')
        file.write('extractAfterDownload=TRUE\n')
        file.write('forcedStart=' + autostart + '\n')
        file.write('autoConfirm=' + autostart + '\n')
        if not subdir == "":
            file.write('downloadFolder=' + subdir + "/" + '%s\n' % folder_name)
            if subdir == "RSScrawler/Remux":
                file.write('priority=Lower\n')
        else:
            file.write('downloadFolder=' + '%s\n' % folder_name)
        file.write('packageName=%s\n' % package_name.replace(' ', ''))
        file.write('text=%s\n' % link_text)
        file.close()
        return True
    except UnicodeEncodeError as e:
        file.close()
        log_error("Beim Schreibversuch des Crawljobs: %s FEHLER: %s" %(crawljob_file, e.message))
        if os.path.isfile(crawljob_file):
            log_info("Entferne defekten Crawljob: %s" % crawljob_file)
            os.remove(crawljob_file)
        return False

def checkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def entfernen(retailtitel, identifier):
    def capitalize(line):
        line = line.rstrip()
        return ' '.join(s[0].upper() + s[1:] for s in line.split(' '))
    simplified = retailtitel.replace(".", " ")
    retail = re.sub(r'(|.UNRATED|.Unrated|.Uncut|.UNCUT)(|.Directors.Cut|.DC|.EXTENDED|.Extended|.Theatrical|.THEATRICAL)(|.3D|.3D.HSBS|.3D.HOU|.HSBS|.HOU)(|.)\d{4}(|.)(|.UNRATED|.Unrated|.Uncut|.UNCUT)(|.Directors.Cut|.DC|.EXTENDED|.Extended|.Theatrical|.THEATRICAL)(|.3D|.3D.HSBS|.3D.HOU|.HSBS|.HOU).(German|GERMAN)(|.AC3|.DTS|.DTS-HD)(|.DL)(|.AC3|.DTS).(2160|1080|720)p.(UHD.|Ultra.HD.|)(HDDVD|BluRay)(|.HDR)(|.AVC|.AVC.REMUX|.x264|.x265)(|.REPACK|.RERiP)-.*', "", simplified)
    retailyear = re.sub(r'(|.UNRATED|.Unrated|.Uncut|.UNCUT)(|.Directors.Cut|.DC|.EXTENDED|.Extended|.Theatrical|.THEATRICAL)(|.3D|.3D.HSBS|.3D.HOU|.HSBS|.HOU).(German|GERMAN)(|.AC3|.DTS|.DTS-HD)(|.DL)(|.AC3|.DTS|.DTS-HD).(2160|1080|720)p.(UHD.|Ultra.HD.|)(HDDVD|BluRay)(|.HDR)(|.AVC|.AVC.REMUX|.x264|.x265)(|.REPACK|.RERiP)-.*', "", simplified)
    if identifier == '2':
        liste = "MB_3D"
    else:
        liste = "MB_Filme"
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'Einstellungen/Listen/' + liste + '.txt'), 'r') as l:
        content = l.read()
        l.close()
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'Einstellungen/Listen/' + liste + '.txt'), 'w') as w:
        w.write(content.replace(retailyear, "").replace(retail, "").replace(retailyear.lower(), "").replace(retail.lower(), "").replace(retailyear.upper(), "").replace(retail.upper(), "").replace(capitalize(retailyear), "").replace(capitalize(retail), ""))
    files.check()
    log_debug(retail + " durch Cutoff aus " + liste + " entfernt.")

def cutoff(key, identifier):
    retailfinder = re.search("(|.UNRATED|Uncut|UNCUT)(|.Directors.Cut|.DC|.EXTENDED|.Extended|.Theatrical|.THEATRICAL)(|.3D|.3D.HSBS|.3D.HOU|.HSBS|.HOU).(German|GERMAN)(|.AC3|.DTS|.DTS-HD)(|.DL)(|.AC3|.DTS|.DTS-HD).(2160|1080|720)p.(UHD.|Ultra.HD.|)(HDDVD|BluRay)(|.HDR)(|.AVC|.AVC.REMUX|.x264|.x265)(|.REPACK|.RERiP)-.*",key)
    if retailfinder:
      entfernen(key, identifier)
      return True
    else:
      return False

def load(dockerglobal):
    main = RssConfig('RSScrawler')
    jdownloader = main.get("jdownloader")
    port = main.get("port")
    prefix = main.get("prefix")
    interval = main.get("interval")
    hoster = main.get("hoster")
    mb = RssConfig('MB')
    mbquality = mb.get("quality")
    ignore = mb.get("ignore")
    historical = str(mb.get("historical"))
    mbregex = str(mb.get("regex"))
    cutoff = str(mb.get("cutoff"))
    crawl3d = str(mb.get("crawl3d"))
    enforcedl = str(mb.get("enforcedl"))
    crawlseasons = str(mb.get("crawlseasons"))
    seasonsquality = mb.get("seasonsquality")
    seasonpacks = str(mb.get("seasonpacks"))
    seasonssource = mb.get("seasonssource")
    sj = RssConfig('SJ')
    sjquality = sj.get("quality")
    rejectlist = sj.get("rejectlist")
    sjregex = str(sj.get("regex"))
    yt = RssConfig('YT')
    youtube = str(yt.get("youtube"))
    maxvideos = str(yt.get("maxvideos"))
    ytignore = str(yt.get("ignore"))
    notify = RssConfig('Notifications')
    pushbullet = str(notify.get('pushbullet'))
    pushover = str(notify.get('pushover'))
    jobs = RssConfig('Crawljobs')
    autostart = str(jobs.get('autostart'))
    subdir = str(jobs.get('subdir'))
    if hoster == 'Share-Online':
      hosterso = ' selected'
      hosterul = ''
    else:
      hosterso = ''
      hosterul = ' selected'
    if mbquality == '2160p':
      mbq2160 = ' selected'
      mbq1080 = ''
      mbq720 = ''
      mbq480 = ''
    if mbquality == '1080p':
      mbq2160 = ''
      mbq1080 = ' selected'
      mbq720 = ''
      mbq480 = ''
    if mbquality == '720p':
      mbq2160 = ''
      mbq1080 = ''
      mbq720 = ' selected'
      mbq480 = ''
    if mbquality == '480p':
      mbq2160 = ''
      mbq1080 = ''
      mbq720 = ''
      mbq480 = ' selected'
    if seasonsquality == '2160p':
      msq2160 = ' selected'
      msq1080 = ''
      msq720 = ''
      msq480 = ''
    if seasonsquality == '1080p':
      msq2160 = ''
      msq1080 = ' selected'
      msq720 = ''
      msq480 = ''
    if seasonsquality == '720p':
      msq2160 = ''
      msq1080 = ''
      msq720 = ' selected'
      msq480 = ''
    if seasonsquality == '480p':
      msq2160 = ''
      msq1080 = ''
      msq720 = ''
      msq480 = ' selected'
    if sjquality == '2160p':
      sjq2160 = ' selected'
      sjq1080 = ''
      sjq720 = ''
      sjq480 = ''
    if sjquality == '1080p':
      sjq2160 = ''
      sjq1080 = ' selected'
      sjq720 = ''
      sjq480 = ''
    if sjquality == '720p':
      sjq2160 = ''
      sjq1080 = ''
      sjq720 = ' selected'
      sjq480 = ''
    if sjquality == '480p':
      sjq2160 = ''
      sjq1080 = ''
      sjq720 = ''
      sjq480 = ' selected'
    if historical == 'True':
      historicaltrue = ' selected'
      historicalfalse = ''
    else:
      historicaltrue = ''
      historicalfalse = ' selected'
    if mbregex == 'True':
      mbregextrue = ' selected'
      mbregexfalse = ''
      mrdiv = "block"
    else:
      mbregextrue = ''
      mbregexfalse = ' selected'
      mrdiv = "none"
    if cutoff == 'True':
      cutofftrue = ' selected'
      cutofffalse = ''
    else:
      cutofftrue = ''
      cutofffalse = ' selected'
    if crawl3d == 'True':
      crawl3dtrue = ' selected'
      crawl3dfalse = ''
      tddiv = "block"
    else:
      crawl3dtrue = ''
      crawl3dfalse = ' selected'
      tddiv = "none"
    if enforcedl == 'True':
      enforcedltrue = ' selected'
      enforcedlfalse = ''
    else:
      enforcedltrue = ''
      enforcedlfalse = ' selected'
    if crawlseasons == 'True':
      crawlseasonstrue = ' selected'
      crawlseasonsfalse = ''
      ssdiv = "block"
    else:
      crawlseasonstrue = ''
      crawlseasonsfalse = ' selected'
      ssdiv = "none"
    if seasonpacks == 'True':
      spacktrue = ' selected'
      spackfalse = ''
    else:
      spacktrue = ''
      spackfalse = ' selected'
    if seasonssource == "hdtv|hdtvrip|tvrip":
      shdtv = ' selected'
      shdtvweb = ''
      sweb = ''
      sbluray = ''
      swebbluray = ''
      shdtvwebbluray = ''
      swebretailbluray = ''
    elif seasonssource == "web-dl|webrip|webhd|netflix*|amazon*|itunes*":
      shdtv = ''
      shdtvweb = ''
      sweb = ' selected'
      sbluray = ''
      swebbluray = ''
      shdtvwebbluray = ''
      swebretailbluray = ''
    elif seasonssource == "hdtv|hdtvrip|tvrip|web-dl|webrip|webhd|netflix*|amazon*|itunes*":
      shdtv = ''
      shdtvweb = ' selected'
      sweb = ''
      sbluray = ''
      swebbluray = ''
      shdtvwebbluray = ''
      swebretailbluray = ''
    elif seasonssource == "bluray|bd|bdrip":
      shdtv = ''
      shdtvweb = ''
      sweb = ''
      sbluray = ' selected'
      swebbluray = ''
      shdtvwebbluray = ''
      swebretailbluray = ''
    elif seasonssource == "web-dl|webrip|webhd|netflix*|amazon*|itunes*|bluray|bd|bdrip":
      shdtv = ''
      shdtvweb = ''
      sweb = ''
      sbluray = ''
      swebbluray = ' selected'
      shdtvwebbluray = ''
      swebretailbluray = ''
    elif seasonssource == "hdtv|hdtvrip|tvrip|web-dl|webrip|webhd|netflix*|amazon*|itunes*|bluray|bd|bdrip":
      shdtv = ''
      shdtvweb = ''
      sweb = ''
      sbluray = ''
      swebbluray = ''
      shdtvwebbluray = ' selected'
      swebretailbluray = ''
    else:
      shdtv = ''
      shdtvweb = ''
      sweb = ''
      sbluray = ''
      swebbluray = ''
      shdtvwebbluray = ''
      swebretailbluray = ' selected'
    if sjregex == 'True':
      sjregextrue = ' selected'
      sjregexfalse = ''
      srdiv = "block"
    else:
      sjregextrue = ''
      sjregexfalse = ' selected'
      srdiv = "none"
    if prefix:
      prefix = '/' + prefix
    if dockerglobal == '1':
      dockerblocker = ' readonly="readonly"'
      dockerhint = 'Docker-Modus: Kann nur per Docker-Run angepasst werden! '
    else:
      dockerblocker = ''
      dockerhint = ''
    if youtube == 'True':
      youtubetrue = ' selected'
      youtubefalse = ''
      ytdiv = "block"
    else:
      youtubetrue = ''
      youtubefalse = ' selected'
      ytdiv = "none"
    if autostart == 'True':
      autostarttrue = ' selected'
      autostartfalse = ''
    else:
      autostarttrue = ''
      autostartfalse = ' selected'
    if subdir == 'True':
      subdirtrue = ' selected'
      subdirfalse = ''
    else:
      subdirtrue = ''
      subdirfalse = ' selected'
    return (jdownloader, port, prefix, interval, ignore, rejectlist, hosterso, hosterul, mbq2160, mbq1080, mbq720, mbq480, msq2160, msq1080, msq720, msq480, sjq2160, sjq1080, sjq720, sjq480, historicaltrue, historicalfalse, mbregextrue, mbregexfalse, mrdiv, cutofftrue, cutofffalse, crawl3dtrue, crawl3dfalse, tddiv, enforcedltrue, enforcedlfalse, crawlseasonstrue, crawlseasonsfalse, ssdiv, sjregextrue, sjregexfalse, srdiv, dockerblocker, ytdiv, youtubetrue, youtubefalse, spacktrue, spackfalse, shdtv, shdtvweb, sweb, sbluray, swebbluray, shdtvwebbluray, swebretailbluray, maxvideos, ytignore, pushbullet, pushover, autostarttrue, autostartfalse, subdirtrue, subdirfalse, dockerhint)
