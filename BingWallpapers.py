#!/usr/bin/python

import feedparser
import urllib
import os
import sys

ROOT_FOLDER= "Wallpapers/" #folder to store the downloaded wallpapers
TOKEN="RSSFeed=" #key used to find the feed in the bing theme

def main(file):
    downloadUrl = _extractRss(file)
    downloadq=[]
    feed = feedparser.parse(downloadUrl)
    for article in feed['entries']:
        for link in article.links:
            if 'ref' in link:
                downloadq.append(link['ref'])
    print "Downloading: ",len(downloadq)
    for imageUrl in downloadq:
        imgData = urllib.urlopen(imageUrl).read()
        imfile = imageUrl.split('/')[-1]
        filename = ROOT_FOLDER+imfile
        dfile = open(filename,'wb')
        dfile.write(imgData)
        dfile.close()

def _extractRss(themeFile):
    extractedUrl=""
    f = open(themeFile)
    for line in f:
        if TOKEN in line:
            extractedUrl = line
            break;
    return extractedUrl.split(TOKEN)[1]
        
if __name__=="__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print
        print "usage:python ",sys.argv[0]," .theme_filename"
        print
        exit(-1)
    main(filename)
