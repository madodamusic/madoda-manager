import json

class UpdatePost:
    def __init__(self, gdrive_log_file, wp_id_file="main"):
        pass
        
wp_ids = json.load(open("wp_id_log.json", "r"))
# drive_ids = json.load(open("", "r"))
ids = {"1":"car", "2":"jose", "3":"mar"}
print(wp_ids.keys())
