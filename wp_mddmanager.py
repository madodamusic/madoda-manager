import sys
import datetime
import random
import os
import array
from pathlib import Path
from download_manager.youtube import YtDownload
from tags.edit import Edit as Tag_edit
from google_drive.upload import Upload as gdUpload
from madoda_theme_getway.update_post import UpdatePost as gwUpdatePost
# from download_manager.download_URL_txt import ManagerURL

class WpMManager:
    def __init__(self):
        self.args = sys.argv
        self.main_path =  os.path.dirname(Path(__file__).absolute())
        self.wp_link_file = ""
        self.main()
                        
                
    def createLinkFile(self, links):
        dif_name = ""
        
        for num in range(0, 7):
            dif_name = str(random.randrange(0, 9)) + str(dif_name)
        
        file_name = str(datetime.datetime.today()).replace(" ", "").replace(":","_").replace("-","_").replace(".","_") + dif_name+".txt"
        
        wp_links_path = os.path.join(self.main_path, "assets/wp_download_links") 
        self.wp_link_file = os.path.join(wp_links_path, file_name)
        
        file = open(self.wp_link_file, "w")
        for link in links:
            if link == links[-1]:
                file.write(link)
            else:
                file.write(link+"\n")

        file.close()        
        return self.wp_link_file
    
  

    def get_links_file(self):
        if("-l" in self.args):
            link_indx = self.args.index("-l") + 1
            links = self.args[link_indx].split(",")
            return self.createLinkFile(links)
        elif("-f" in self.args) :
            wp_link_file_idx = self.args.index("-f") + 1
            self.wp_link_file = self.args[wp_link_file_idx]
            return self.wp_link_file
    
    
    def main(self):
        urls_file = self.get_links_file()
        yt_download = YtDownload(urls_file)
        yt_data = yt_download.mp3()
        Tag_edit(yt_data["save_folder"], urls_file, yt_data["wp_id_log"]).edit()
        gdrive_log = gdUpload(musics_folder_path=yt_data["save_folder"]).mp3()
        gwUpdatePost(gdrive_log, yt_data["wp_id_log"]).update()
        # path = Path(urls_file)
        # print(os.path.basename(path).replace(".txt", ""))
        
        

WpMManager()

# if __name__ == "__main__":
#     print(sys.argv)