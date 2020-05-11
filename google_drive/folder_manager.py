from __future__ import print_function
import datetime
from googleapiclient.discovery import build
import os
from pathlib import Path


from auth import Auth

class FolderManager:
    def __init__(self, main_drive_folder_id, copy_folders_number = 6):
        self.main_path = Path(__file__).parent.parent.absolute()
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials = os.path.join(os.getcwd(), "google_drive/service.json")
        self.auth = Auth(self.SCOPES)
        self.creds = self.auth.getCreds()

        self.service = build('drive', 'v3', credentials=self.creds)

        self.main_drive_folder_id = main_drive_folder_id
        self.copy_folders_number = copy_folders_number
        self.copy_folders_ids = []
        self.log_folder_id = ""

    
    def _ceackFolder(self, folder_name, parent_folder_id):
        page_token = None
        while True:
            response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name, parents)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                if file.get('name') == folder_name:
                    try:
                       if file.get('parents')[0] == parent_folder_id:
                            return file.get('id')
                    except:
                        pass
                    
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return False

    def createCopyFolders(self, number, parent_id):
        for num in range(1, (number + 1)):
            folder_name = "copy"+str(num)+"  ("+str(datetime.datetime.today().time())+")"
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                "parents": [parent_id]
            }
            file = self.service.files().create(body=file_metadata,
                                                fields='id').execute()
            self.copy_folders_ids.append(file.get('id'))

    def createNewFolder(self, folder_name, parent_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            "parents": [parent_id]
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
    
        return file.get('id')


    def create(self):
        #reset copy_folder_ids
        self.copy_folders_ids = []
        main_folder_name = str(datetime.datetime.today().year)
        sub_folder_name = str(datetime.datetime.today().day)+"/"+str(datetime.datetime.today().month)

        main_folder_id = self._ceackFolder(main_folder_name, self.main_drive_folder_id)
        if(main_folder_id):
            sub_folder_id = self._ceackFolder(sub_folder_name, main_folder_id)
            if(sub_folder_id):
                #create copy folders
                self.createCopyFolders(self.copy_folders_number, sub_folder_id)
                self.log_folder_id = self._ceackFolder("logs", sub_folder_id)
                if not self.log_folder_id:
                    self.log_folder_id =  self.createNewFolder("logs", sub_folder_id)
            else:
                sub_folder_id = self.createNewFolder(sub_folder_name, main_folder_id)
                self.createCopyFolders(self.copy_folders_number, sub_folder_id)
                self.log_folder_id = self._ceackFolder("logs", sub_folder_id)
                if not self.log_folder_id:
                    self.log_folder_id =  self.createNewFolder("logs", sub_folder_id)
        else:
            main_folder_id = self.createNewFolder(main_folder_name, self.main_drive_folder_id)
            sub_folder_id = self.createNewFolder(sub_folder_name, main_folder_id)
            self.createCopyFolders(self.copy_folders_number, sub_folder_id)
            self.log_folder_id = self._ceackFolder("logs", sub_folder_id)
            if not self.log_folder_id:
                self.log_folder_id =  self.createNewFolder("logs", sub_folder_id)
    

    
    def getCopyFolderIds(self):
        return self.copy_folders_ids

    def getLogFolderID(self):
        return self.log_folder_id


if __name__ == "__main__":
    fm = FolderManager("kkjkjk")
    print("auth end")
    fm.fullAccount()