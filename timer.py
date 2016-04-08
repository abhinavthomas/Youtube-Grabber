import time

def doit():
	from os import system
	system("python video_downloader.py")
	
if __name__ == "__main__":
    while True:
        doit()
        time.sleep(60) # 60 seconds = 1 minutes
