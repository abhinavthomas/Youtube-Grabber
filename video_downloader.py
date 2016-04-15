#!/usr/bin/env/python
"""
	Script to download from youtube playlist.
	Author : Abhinav Thomas
	
"""
import pickle
import logging
import time

def urlfetch():
	try:
		fp= open('config.txt','r')
		logging.info("config file opened")
		url=fp.read()
		fp.close()
		logging.info("url read. returning url...")
		return url
	except IOError:
		logging.info("config file not found")
		fp = open('config.txt','w')
		logging.info("config created")
		url = raw_input("Enter the url : ")
		fp.write(url)
		logging.info("config file opened and new url is inputed")
		fp.close()
		return url
		
def download_stack_reader():
	try:
		fp=open("downloaded_files.pkl","rb")
	except IOError:
		fp=open("downloaded_files.pkl","wb")
		fp.close()
		fp=open("downloaded_files.pkl","rb")		
		
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

def download_stack_updater(downloaded):
	fp=open("downloaded_files.pkl","ab")
	pickle.dump(downloaded,fp)
	fp.close()
	
def display(v): 
	print "Title	: ",v.title
	print "Duration : ",v.duration
	print "Rating	: ",v.rating
	print "Author	: ",v.author
	print "Views	: ",v.viewcount
	for s in v.videostreams:
	    print(s.mediatype, s.extension, s.quality)
	print "=========Downloading best quality video==========="
	logging.info("=========Downloading best quality video===========")

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

	to_download=0 
	downloaded = download_stack_reader()
	url = urlfetch()
	playlist = pafy.get_playlist(url)
	logging.info("playlist created")
    
	while(True):
		try:
			video = playlist['items'][to_download]['pafy']
			logging.info(playlist['items'][to_download]['pafy'])
			if video.videoid not in downloaded :
				display(video)
				download_url = video.getbest()
				logging.info("Video found")
				filename = download_url.download()
				logging.info("Downloading...")
				download_stack_updater(video.videoid)
			else:
				print "Video already downloaded"
			logging.info("stack updated with new value")
			to_download+=1

		except IndexError:
			print "Downloading finished"
			logging.info("download finished")
			break

if __name__=='__main__':
	logging.basicConfig(filename="downloader_log.log", level=logging.DEBUG)
	print "GPL... (c) Abhinav Thomas .."
	print "All rights reserved.."
	while True:
	        downloader()
        	time.sleep(3600) # 3600 seconds = 1 hour
