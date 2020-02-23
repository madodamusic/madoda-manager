from __future__ import unicode_literals
import youtube_dl
import os

# music_dir = os.path.abspath("../musics")
def mp3(link):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'files/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)
