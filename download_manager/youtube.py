from __future__ import unicode_literals
import youtube_dl
import os
import json
from download_URL_txt import ManagerURL

class YtDownload:
    def __init__(self):        
        self.manager_url = ManagerURL()
        self.all_wp_ids = {}
 


    def set_WP_ID(self, url, yt_title):
        if(self.manager_url.getWP_ID(url) != -1):
            wp_id = self.manager_url.getWP_ID(url)
            self.all_wp_ids.setdefault(yt_title+".mp3", wp_id)
            return wp_id
        else:
            return "no wp_id"



    def create_WP_ID_log_file(self):
        wp_id_log = open("wp_id_log.json", "w")
        wp_id_log.write(json.dumps(self.all_wp_ids))
        wp_id_log.close()

    
    
    def mp3(self):
        links = self.manager_url.getYoutubeUrls()
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
            with youtube_dl.YoutubeDL() as ydl:
                meta = ydl.extract_info(link, download=False)
                self.set_WP_ID(link, meta['title'])
            self.create_WP_ID_log_file()

if __name__ == "__main__":
    # print("kkk")
    ytd = YtDownload()
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=BTgCJ-m4u3o", "musica1")
    # print(wp_id)
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=dDwWE1hp8rY", "musica2")
    # print(wp_id)
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=kP2lkoqLx8A", "musica2")
    # print(wp_id)
    # ytd.create_WP_ID_log_file()
    ytd.mp3()
    