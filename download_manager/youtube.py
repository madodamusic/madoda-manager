from __future__ import unicode_literals
import youtube_dl
import os
import json
import datetime
from pathlib import Path

from download_manager.download_URL_txt import ManagerURL
class YtDownload:
    def __init__(self, url_file="none"):
        self.main_path = Path(__file__).parent.parent.absolute()
        self.all_wp_ids = {}
        self.all_music_path = []
        
        if url_file == "none":
            self.save_folder = os.path.join(str(self.main_path) ,"musics")
            self.manager_url = ManagerURL()
            self.wp_id_log = os.path.join(str(self.main_path) ,"assets/wp_id_logs/main_log.json")
        else:
            self.manager_url = ManagerURL(url_file)
            folder_name = os.path.basename(url_file).replace(".txt", "")
            self.wp_id_log = os.path.join(str(self.main_path) ,"assets/wp_id_logs/"+folder_name+".json")

            self.save_folder = Path(str(self.main_path)+"/musics/"+folder_name)
            if not self.save_folder.exists():
                self.save_folder.mkdir()

    def set_WP_ID(self, url, yt_title):
        if(self.manager_url.getWP_ID(url) != -1):
            wp_id = self.manager_url.getWP_ID(url)
            self.all_wp_ids.setdefault(yt_title+".mp3", wp_id)
            return wp_id
        else:
            return "no wp_id"



    def create_WP_ID_log_file(self):
        wp_id_log = open(self.wp_id_log, "w")
        wp_id_log.write(json.dumps(self.all_wp_ids))
        wp_id_log.close()

    
    
    def mp3(self):
        for num in range(0, 10):
            try:
                links = self.manager_url.getYoutubeUrls()
                print(links)
                for link in links:
                    if self.manager_url.getNameByTags(link) != -1:
                        title = self.manager_url.getNameByTags(link)
                    else:
                        title = '%(title)s'

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
                        meta = ydl.extract_info(link, download=True)
                        self.set_WP_ID(link, meta['title'])
                    self.create_WP_ID_log_file()
                return {"save_folder":str(self.save_folder), "wp_id_log":self.wp_id_log}
                break;
            except youtube_dl.utils.DownloadError:
                pass
        

if __name__ == "__main__":
    # print("kkk")
    ytd = YtDownload("/mnt/x/workspace/madoda-manager/assets/wp_download_links/2020_21_06.txt").mp3()
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=BTgCJ-m4u3o", "musica1")
    # print(ytd.save_folder)
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=dDwWE1hp8rY", "musica2")
    # print(wp_id)
    # wp_id = ytd.set_WP_ID("https://www.youtube.com/watch?v=kP2lkoqLx8A", "musica2")
    # print(wp_id)
    # ytd.create_WP_ID_log_file()
    # print(ytd.mp3())

    # pa = Path(__file__)
    # print(os.path.basename(pa).replace(".py", ""))

    