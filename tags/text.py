import eyed3
import os
import pathlib

imagedata = open("./tags/image.jpg","rb").read()
files = os.listdir("./musics/") 
for file in files:
    if(file.endswith(".mp3")):
        audiofile = eyed3.load(os.path.abspath("./musics/{}".format(file)))
        audiofile.initTag()
        audiofile.tag.images.set(3,imagedata,"image/jpeg",u"madoda music")
        # audiofile.tag.title = file.replace(".mp3","")
        # audiofile.tag.album = u"madoda music"
        audiofile.tag.version = (2, 3, 0)
        audiofile.tag.save()