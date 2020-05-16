import eyed3 
import os
from pathlib import Path
from .tags_manager import TagsManager
import json
class Edit:
    def __init__(self, musics_folder="none", urls_file="none", wp_ids_file="none"):
        self.main_path = Path(__file__).parent.parent.absolute()
        self.urls_file = urls_file
        self.wp_ids = json.loads(str(Path(str(wp_ids_file)).read_text()))
        if musics_folder == "none":
            self.musics_folder = os.path.join(str(self.main_path), "musics")
        else:
            self.musics_folder = musics_folder
        
        imagepath = Path(str(self.main_path)) / "tags/image.jpg"
        print(imagepath)
        self.main_image = imagepath.read_bytes()
    
    
    def edit_tags_by_tag_data(self,music_path, tag_data):
        try:
            audiofile = eyed3.load(music_path)
            audiofile.initTag()            
            if "Image" in tag_data.keys():
                imagedata = Path(str(tag_data["Image"])).read_bytes()
                audiofile.tag.images.set(3,imagedata,"image/jpeg",u"madoda music")
            else:
                audiofile.tag.images.set(3,self.main_image,"image/jpeg",u"madoda music")
                

            print("set image")
            if "Artist" in tag_data.keys():
                audiofile.tag.artist = tag_data["Artist"]
            
            if "Title" in tag_data.keys():
                audiofile.tag.title = tag_data["Title"]
            
            if "Album" in tag_data.keys():
                audiofile.tag.album = tag_data["Album"]
            else:
                audiofile.tag.album = u"madoda music"
            
            audiofile.tag.version = (2, 3, 0)
            audiofile.tag.save()
        except:
            print("error editing tags")
        

    def tags_by_file_name(self, music="none"):
        files = os.listdir(self.musics_folder)
        if music == "none":
            for file in files:
                if(file.endswith(".mp3")):
                    try:
                        audiofile = eyed3.load(os.path.abspath(os.path.join(self.musics_folder, file)))
                        audiofile.initTag()
                        audiofile.tag.images.set(3,self.main_image,"image/jpeg",u"madoda music")
                        audiofile.tag.title = file.replace(".mp3","")
                        audiofile.tag.album = u"madoda music"
                        audiofile.tag.version = (2, 3, 0)
                        audiofile.tag.save()
                    except:
                        print("error editing tags")
        else:
            print(music)
            try:
                audiofile = eyed3.load(music)
                audiofile.initTag()
                audiofile.tag.images.set(3,self.main_image,"image/jpeg",u"madoda music")
                audiofile.tag.title = str(Path(str(music)).stem)
                audiofile.tag.album = u"madoda music"
                audiofile.tag.version = (2, 3, 0)
                audiofile.tag.save()
            except:
                print("error editing tags")


    def edit(self):
        if self.urls_file != "none" and self.wp_ids != "none":
            tm = TagsManager(self.urls_file)
            musics = Path(str(self.musics_folder))
            for music in musics.iterdir():
                if music.suffix == ".mp3":
                    for wp_id_key in self.wp_ids.keys():
                        if music.name == wp_id_key:
                            print(tm.getTagsByWP_ID(self.wp_ids[wp_id_key]))
                            if tm.getTagsByWP_ID(self.wp_ids[wp_id_key]) != -1:
                                tag_data = tm.getTagsByWP_ID(self.wp_ids[wp_id_key])
                                self.edit_tags_by_tag_data(str(music.absolute()), tag_data)
                            else:
                                print("edit tag by faile name")
                                self.tags_by_file_name(str(music))   
                    print(music.name)
        else:
            self.tags_by_file_name()            

