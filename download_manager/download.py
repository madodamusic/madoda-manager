import wget
import os
import re
print('Beginning file download with wget module')

url = 'https://download626.mediafire.com/5fomyrmeywdg/wg1nic8zvh0g2nu/Cleyton+Da+Drena+-+Van+Damme.mp3'
wget.download(url, './musics')
url_base = os.path.basename(url)

def  remove_uncode(text):
    text_r = re.sub('[^A-Za-z0-9]+', ' ', text)
    text_c = text_r.replace(" mp3", ".mp3")
    return text_c

print(remove_uncode(url_base))