import os
from pathlib import Path
import json
class ManagerURL:
    def __init__(self, url_file="main"):
        if url_file == "main":
            self.main_path = Path(__file__).parent.parent.absolute()
            self.url_file_path = str(self.main_path)+"/download_URL.txt"
            # self.url_file_path = str(os.path.dirname(absFilePath))+"download_URL.txt"
        else:
            self.url_file_path = url_file

        print(self.url_file_path)
        

    def _openFile(self, to="r"):
        return open(self.url_file_path, to)
    
    
    def _closeFile(self, file):
        file.close()


    def saveUrls(self):
        file = self._openFile("w")
        file.write()
        self._closeFile(file)
        return self.all_urls

    def _generatUrls(self):
        file = self._openFile()
        self.all_urls = str(file.read()).split("\n")
        self._closeFile(file)
        return self.all_urls

    
    def setUrl(self, new_url):
        file = self._openFile("a")
        file.write("\n"+new_url)
        self._closeFile(file)


    def cleanAllUrls(self):
        file = self._openFile("w")
        file.write("")
        file.close()
    
    def getAllUrls(self):
        return self._generatUrls()
        
    def getYoutubeUrls(self):
        allurls = self._generatUrls()
        yurls = []
        for url in allurls:
            if(url.find("https://www.youtube.com/") != -1):
                url_start_index = url.find("https://www.youtube.com/")
                if(url.find(" ", url_start_index) != -1):
                    url_end_index = url.find(" ", url_start_index)
                    yurl = str(url[url_start_index:url_end_index]).replace(" ", "")
                else:
                    yurl = str(url[url_start_index:]).replace(" ", "")
                
                yurls.append(yurl)
        
        return yurls
    
    def getWP_ID(self, _url):
        allurls = self._generatUrls()
        wp_id = -1
        for url in allurls:
            if(url.find(_url) != -1):
                if(url.find("wp_id=") != -1):
                    url_start_index = url.find("wp_id=")+6
                    if(url.find(" ", url_start_index) != -1):
                        url_end_index = url.find(" ", url_start_index)
                        wp_id = str(url[url_start_index:url_end_index]).replace(" ", "")
                    else:
                        wp_id = str(url[url_start_index:]).replace(" ", "")
                
        return wp_id

    def getNameByTags(self, url):
        all_text = self._generatUrls()
        name = -1
        for text in all_text:
            # text = text.replace("'", "\"")
            text_a = text.split(" ")
            if(text.find(str(url)) != -1):
                if(text.find("-t") != -1):
                    tag_index = text_a.index("-t")+1
                    if tag_index < len(text_a):
                        tags = json.loads(text_a[tag_index])
                        
                        if tags["Artist"] and tags["Title"]:
                            return str(tags["Artist"]) +" - " +str(tags["Title"])

                    else:
                        return -1
    
        return name