from __future__ import unicode_literals
import youtube_dl
import os
from download_manager.download_URL_txt import ManagerURL

manager_url = ManagerURL()
# music_dir = os.path.abspath("../musics")
def mp3(links):
    for link in links:
        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'musics/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        

