from __future__ import unicode_literals
import youtube_dl
from pathlib import Path

class YoutubeDownload:
    def __init__(self):
       self.save_folder = Path(__file__).absolute().parent.parent / Path("musics")

   
   
    def mp3(self, yt_url, outpname= None):
        if outpname:
            save_folder = Path(str(outpname)).parent
            if save_folder.exists():
                self.save_folder = save_folder
            title = Path(str(outpname)).name
        else:
            title = '%(title)s'
  
        for num in range(0, 5):
            try:
                ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.save_folder)+'/'+title+'.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                }
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    meta = ydl.extract_info(yt_url, download=True)
                    if title == "%(title)s":
                        return Path(self.save_folder) / Path(meta['title'])
                    else:
                        return Path( str(outpname) ).with_suffix(".mp3")
                            
                break
            except youtube_dl.utils.DownloadError:
                pass

if __name__ == "__main__":
    yt = YoutubeDownload()
    links = ["https://www.youtube.com/watch?v=m0mC3dcAOFU"]
    for lin in links:
        print(yt.mp3(lin))
