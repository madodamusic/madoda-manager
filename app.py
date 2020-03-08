#from youtube import download
#from tags import edit
import json

cred = json.load(open("./google-drive/service.json", "r"))

print(cred["type"])