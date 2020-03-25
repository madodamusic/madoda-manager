import os
class ManagerURL:
    def __init__(self, url_file="main"):
        if url_file == "main":
            self.url_file_path = str(os.getcwd())+"/download_URL.txt"
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
        self.all_urls = str(file.read()).split()
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
        
