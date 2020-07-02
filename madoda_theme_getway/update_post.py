import json
import requests
from pathlib import Path
class UpdatePost:
    def __init__(self, gdrive_log_path="main", wp_id_path="main"):
        self.main_path = Path(__file__).parent.parent.absolute()

        self.gdrive_log_path = gdrive_log_path
        rest_aut_path = Path(self.main_path) / "assets/madoda_getway/rest_auth.json"
        rest_auth = json.loads(str(rest_aut_path.read_text()))
        
        if wp_id_path !="main":
            self.wp_id_path = wp_id_path
        else:
            self.wp_id_path = str(Path(self.main_path) / "assets/wp_id_logs/wp_id_log.json")
        
        if gdrive_log_path !="main":
            self.gdrive_log_path = gdrive_log_path
        else:
            self.gdrive_log_path = str(Path(self.main_path) / "assets/gdrive_log/drive_urls.json")

        self.user = rest_auth["user"]
        self.pswd = rest_auth["pswd"]
        self.aut_url = rest_auth["aut_url"]
        self.up_gdrive_url = rest_auth["update_gdrive_url"]
    

    def generat_data(self, post_data):
        # data = {"settings":{
        #     "user": self.user,
        #     "pswd": self.pswd,
        #     "type": "gdrive"
        # }}
        data = {"token": self.get_token(), "posts":post_data}
        # data.setdefault("posts", post_data)
        return data

    def sendRequest(self, url, data):
        # headers = {'content-type': 'application/json'}
        x = requests.post(url, json = data)
        return x
        

    def get_token(self):
        data = {
            "user": self.user,
            "pass": self.pswd
        }
        return str(self.sendRequest(self.aut_url, data).text.replace("\"", ""))


    def update(self):
        wp_ids = json.load(open(self.wp_id_path, "r"))
        gdrive_log = json.load(open(self.gdrive_log_path, "r"))
        post_data = []
        for wpkey in wp_ids.keys():
            post_data.append(
                {
                    "id": wp_ids[wpkey],
                    "drive_links": gdrive_log[wpkey]
                }
            )
        
        data = self.generat_data(post_data)
        print(self.sendRequest(self.up_gdrive_url, data).content)



if __name__ == "__main__":
    up = UpdatePost("/home/roots/mddr/madoda-manager/assets/gdrive_log/2020_1_06.json", "/home/roots/mddr/madoda-manager/assets/wp_id_logs/2020_1_06.json")
    # print(up.get_token())
    up.update()
