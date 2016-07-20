#!/usr/bin/env/python
"""
    Script to download from youtube playlist.
    Author : Abhinav Thomas
    
"""
import pickle
import logging
import time
import os

def urlfetch():
    try:
        fp= open('config.txt','r')
        logging.info("config file opened")
        url=fp.read().splitlines()
        fp.close()
        logging.info("url read. returning url...")
        return url
    except IOError:
        logging.info("config file not found")
        fp = open('config.txt','w')
        logging.info("config created")
        vurl = raw_input("Enter the video url : ")
        fp.write(vurl)
        fp.write('\n')
        aurl = raw_input("Enter the audio url : ")
        fp.write(aurl)
        logging.info("config file opened and new url is inputed")
        fp.close()
        return [vurl,aurl]
        
def v_download_stack_reader():
    try:
        fp=open("v_downloaded_files.pkl","rb")
    except IOError:
        fp=open("v_downloaded_files.pkl","wb")
        fp.close()
        fp=open("v_downloaded_files.pkl","rb")        
        
    logging.info("downloaded_files opened .... ")
    l=[]
    while(True):
        try:
            l.append(pickle.load(fp))
            logging.info("loaded stack of downloaded files..")
        except EOFError:
            break
    fp.close()      
    return l

def a_download_stack_reader():
    try:
        fp=open("a_downloaded_files.pkl","rb")
    except IOError:
        fp=open("a_downloaded_files.pkl","wb")
        fp.close()
        fp=open("a_downloaded_files.pkl","rb")        
        
    logging.info("downloaded_files opened .... ")
    l=[]

    while(True):
        try:
            l.append(pickle.load(fp))
            logging.info("loaded stack of downloaded files..")
        except EOFError:
            break
    fp.close()      
    return l

def v_download_stack_updater(downloaded):
    fp=open("v_downloaded_files.pkl","ab")
    pickle.dump(downloaded,fp)
    fp.close()
    
def a_download_stack_updater(downloaded):
    fp=open("a_downloaded_files.pkl","ab")
    pickle.dump(downloaded,fp)
    fp.close()
    
def display(v,a): 
    print "Title    : ",v.title
    print "Duration : ",v.duration
    print "Rating   : ",v.rating
    print "Author   : ",v.author
    print "Views    : ",v.viewcount
    
    if a=='v':
        for s in v.videostreams:
            print(s.mediatype, s.extension, s.quality)
        print "=========Downloading best quality video==========="
        logging.info("=========Downloading best quality video===========")
    else:

        for a in v.audiostreams:
            print(a.bitrate, a.extension, a.get_filesize())
        print "=========Downloading best quality audio==========="
        logging.info("=========Downloading best quality audio===========")


def downloader():
    while(True):

        try:
            import pafy
            break

        except ImportError:
            print "Inside exception ImportError"
            from os import system

            try:
                print "trying pafy installation"
                system("sudo pip install pafy")
                logging.info("pafy has installed...")
                print "pip installation finished"
            except:
                print "Couldn't install pip. Inside pip exception"
                logging.error("couldn't install pafy")
                system("wget https://bootstrap.pypa.io/get-pip.py")
                logging.info("trying to install pip..")
                system("sudo python get-pip.py")
                logging.info("Successfully installed pip...")
                print "pip already install"

    v_to_download=0 
    a_to_download=0 
    vdownloaded = v_download_stack_reader()
    adownloaded = a_download_stack_reader()
    url = urlfetch()
    vplaylist = pafy.get_playlist(url[0])
    aplaylist = pafy.get_playlist(url[1])
    logging.info("playlist created")
    a,v=0,0
    while(True):
        a,v=0,0    
        try:
            video = vplaylist['items'][v_to_download]['pafy']
            logging.info(vplaylist['items'][v_to_download]['pafy'])
            if video.videoid not in vdownloaded :
                display(video,'v')
                download_url = video.getbest()
                logging.info("Video found")
                filename = download_url.download()
                logging.info("Downloading...")
                v_download_stack_updater(video.videoid)
            else:
                print "Video already downloaded"
            logging.info("stack updated with new value")
            
            v_to_download+=1

        except IndexError:

            print "Video Downloading finished"
            v=1
            logging.info("download finished")

        try:
            video = aplaylist['items'][a_to_download]['pafy']
            logging.info(aplaylist['items'][a_to_download]['pafy'])
            if video.videoid not in adownloaded :
                display(video,'a')
                download_url = video.getbestaudio()
                logging.info("Audio found")
                filename = download_url.download()
                logging.info("Downloading...")
                a_download_stack_updater(video.videoid)
            else:
                print "Audio already downloaded"
            print("outside audio else")
            logging.info("stack updated with new value")
            
            a_to_download+=1

        except IndexError:

            print "Audio Downloading finished"
            a=1
            logging.info("download finished")

        if(a==1 and v==1):
            break

if __name__=='__main__':
    logging.basicConfig(filename="downloader_log.log", level=logging.DEBUG)
    print "GPL .v2... (c) Abhinav Thomas .."
    print "All rights reserved.."
    while True:
            downloader()
            time.sleep(20) # 60 seconds = 1 minute
