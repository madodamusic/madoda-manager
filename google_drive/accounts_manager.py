import os
from pathlib import Path
from googleapiclient.discovery import build

from .auth import Auth
class AccountsManager:
    def __init__(self):
        self.main_path = Path(__file__).parent.parent.absolute()
    
    def getFullAccount(self):
            full_accounts_path = Path(os.path.join(str(self.main_path), "google_drive/logs/full_accounts.txt"))
            full_accounts = full_accounts_path.read_text().split("\n")
            return full_accounts
        

    def setFullAccount(self, account):
        full_accounts_path = Path(os.path.join(str(self.main_path), "google_drive/logs/full_accounts.txt"))
        full_accounts_path.write_text(str(account)+"\n")

    
    def __get_folder_size(self,folder):
        music_path = Path(folder)
        size = 0
        for music in music_path.iterdir():
            if str(music).endswith(".mp3"):
                size += int(os.path.getsize(str(music)))
        
        return size
    
    def __get_gdrive_free_size(self, account):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        auth = Auth(SCOPES, account)
        creds = auth.getCreds()

        service = build('drive', 'v3', credentials=creds)
        res = service.about().get(fields = "user, storageQuota").execute()
        free_space = int(res["storageQuota"]["limit"]) - int(res["storageQuota"]["usage"])

        return free_space


    def getCred(self, music_folder):
        accounts_path = Path(os.path.join(str(self.main_path), "google_drive/accounts"))
        full_accounts = self.getFullAccount()
        for ac in accounts_path.iterdir():
            if str(ac) not in full_accounts and str(ac.suffix) == ".json":
                print(self.__get_folder_size(music_folder))
                print(self.__get_folder_size(music_folder) * 6)
                if ( self.__get_folder_size(music_folder) * 6) < self.__get_gdrive_free_size(ac):
                    return str(ac.absolute())
                else:
                    print("less space in: "+str(ac))
            else:
                print(str(ac)+" [is full]")

    # def get_gdrive_id(name, parent_id):
    # def _upload_file(self, file, parent_id, mimetype= "text/plain"):
    #     file_metadata = {
    #         'name': os.path.basename(file), 
    #         "parents": [parent_id]
    #     }
    #     media = MediaFileUpload(file, mimetype=mimetype)
    #     Dfile = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    #     return Dfile.get('id')
    
    def update_account(self, account):
        if self.__get_gdrive_free_size(account) < 100000000:
            self.setFullAccount(account)

if __name__ == "__main__":
    am = AccountsManager()
    am.update_account(am.getCred("/mnt/x/workspace/madoda-manager/musics/"))