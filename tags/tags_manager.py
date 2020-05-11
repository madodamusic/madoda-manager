import os
from pathlib import Path
import json

class TagsManager:
    def __init__(self, tag_file="none"):
        self.main_path = Path(__file__).parent.parent.absolute()
        if tag_file == "none":
            self.tag_file = str(self.main_path)+"/download_URL.txt"
        else:
            self.tag_file = tag_file
        
    def _getTextOnFile(self):
        file = open(self.tag_file, "r")
        all_text = str(file.read()).split("\n")
        file.close()
        return all_text
    

    def getTagsByWP_ID(self, id):
        all_text = self._getTextOnFile()
        tags = -1
        for text in all_text:
            text = text.replace("'", "\"")
            text_a = text.split(" ")
            if(text.find("wp_id="+str(id)) != -1):
                if(text.find("-t") != -1):
                    tag_index = text_a.index("-t")+1
                    if tag_index < len(text_a):
                        tags = text_a[tag_index]
                    else:
                        return -1
                
        return json.loads(tags)

if __name__ == "__main__":
    tm = TagsManager()
    print(tm.getTagsByWP_ID(676)["title"])
    print(tm.getTagsByWP_ID(777))

