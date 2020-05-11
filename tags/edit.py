import eyed3 
import os
import pathlib
from tags.tags_manager import TagsManager

class Edit:
    def __init__(self, musics_folder="none"):
        self.main_path = Path(__file__).parent.parent.absolute()

        if musics_folder == "none":
            self.musics_folder = os.path.join(str(self.main_path), "musics")
        else:
            self.musics_folder = musics_folder
    
    
    def tags_by_tags_file(tags_file, wp_ids):
        for wp_id in wp_ids.keys():
            pass

    
    def tags_by_file_name(self):
        imagedata = open(str(self.main_path)+"/tags/image.jpg","rb").read()
        files = os.listdir(self.musics_folder)
        for file in files:
            if(file.endswith(".mp3")):
                try:
                    audiofile = eyed3.load(os.path.abspath(os.path.join(self.musics_folder, file)))
                    audiofile.initTag()
                    audiofile.tag.images.set(3,imagedata,"image/jpeg",u"madoda music")
                    audiofile.tag.title = file.replace(".mp3","")
                    audiofile.tag.album = u"madoda music"
                    audiofile.tag.version = (2, 3, 0)
                    audiofile.tag.save()
                except:
                    print("error editing tags")


