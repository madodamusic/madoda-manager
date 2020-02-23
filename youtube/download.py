from __future__ import unicode_literals
import youtube_dl
import os

music_dir = os.path.abspath("../musics")
def mp3(link):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '{}%(title)s.%(ext)s'.format(music_dir),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link)
