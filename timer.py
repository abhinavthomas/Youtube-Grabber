#! /usr/bin/env/python
import time

def doit():
	from os import system
	system("python video_downloader.py")
	
if __name__ == "__main__":
    while True:
        doit()
        time.sleep(3600) # 3600 seconds = 1 hour
