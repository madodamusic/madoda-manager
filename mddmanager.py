import sys
import os
import sys
from tags import edit
from youtube import download as yt_download
from google_drive.upload import Upload
from download_manager.download_URL_txt import ManagerURL
 
upload = Upload()
manager_url = ManagerURL()

if(os.path.getsize("download_URL.txt") > 0):
    print("download youtube video and convert to mp3")
    urls = manager_url.getAllUrls()
    yt_download.mp3(urls)
    print("editing tags...")
    edit.tags_by_file_name()
    print("upload musics....")
    upload.mp3()
    print("done")
elif (os.listdir( os.path.join(os.getcwd(), "musics")  )):
    print("NO URL found in download_URL.txt\nstart uploading mp3 files in musics directory\n\n")
    print("editing tags...")
    edit.tags_by_file_name()
    print("upload musics....")
    upload.mp3()
    print("done")
else:
    print("no musics and links")