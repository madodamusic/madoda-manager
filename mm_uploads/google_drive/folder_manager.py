from __future__ import print_function
import datetime
import os
from gdrive import Gdive
from pathlib import Path
from auth import Auth
from accounts_manager import AccountsManager

class FolderManager(Gdive):
    def __init__(self, gdrive_service):
        super().__init__()
        self.service = gdrive_service
        if self.conf.get("main_folder_id", 0):
            self.main_drive_folder_id = self.conf["main_folder_id"]
        else:
            self.main_drive_folder_id = "root"
        
        self._content_folder_id = 0
        self._gdrive_path_folders_ids = []
        self.__drive_log_folder_name = "logs"
        self.__log_folder_id = 0
        self.__base_log_folder_id = 0
        

    
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
    
    
    def createNewFolder(self, folder_name, parent_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            "parents": [parent_id]
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()
    
        return file.get('id')


            
    def create(self, folders):
        base_parent_folder_id, base_folder_id = self.create_gdrive_folder_from_date_Y_M(self.main_drive_folder_id)
        for index, folder in enumerate(folders):
            parent_id = folders[index -1]
            
            if index == 0:parent_id =  base_folder_id
               
            content_folder_id = self._ceackFolder(folder, parent_id)
            if not content_folder_id:
                content_folder_id = self.createNewFolder(folder, parent_id)
            
            self._gdrive_path_folders_ids.append(content_folder_id)
            self._content_folder_id = content_folder_id
        
        self._create_gdrive_log_folder_id()
            
        return content_folder_id
    
    
    
    def create_gdrive_folder_from_date_Y_M(self, main_parent_id=None):
        year_folder_name = str(datetime.datetime.today().year)
        month_folder_name = str(datetime.datetime.today().month)
        if not main_parent_id: main_parent_id = self.main_drive_folder_id
        year_folder_id = self._ceackFolder(year_folder_name, main_parent_id)
        if year_folder_id:
            month_folder_id = self._ceackFolder(month_folder_name, year_folder_id)
            if not month_folder_id:
                month_folder_id = self.createNewFolder(month_folder_name, year_folder_id)        
        else:
            year_folder_id = self.createNewFolder(year_folder_name, main_parent_id)
            month_folder_id = self.createNewFolder(month_folder_name, year_folder_id)
        
        return year_folder_id, month_folder_id


    
    def _create_gdrive_log_folder_id(self):
        self.__base_log_folder_id  = self._ceackFolder(self.__drive_log_folder_name, self.main_drive_folder_id)
        if not self.__base_log_folder_id:
            self.__base_log_folder_id = self.createNewFolder(self.__drive_log_folder_name, self.main_drive_folder_id)
        
        parent_folder_id, content_folder_id = self.create_gdrive_folder_from_date_Y_M(self.__base_log_folder_id)
        self.__log_folder_id = content_folder_id
        return content_folder_id
        



                
    @property
    def content_folder_id(self):
        return self._content_folder_id
    
    @property
    def gdrive_path_folders_ids(self):
        return self._gdrive_path_folders_ids
    
    @property
    def log_folder_id(self):
        return self.__log_folder_id
    
    @property
    def base_log_folder_id(self):
        return self.__base_log_folder_id
        

if __name__ == "__main__":
        am = AccountsManager()
        account = am.getCred(__file__)
        SCOPES = ['https://www.googleapis.com/auth/drive']
        auth = Auth(SCOPES, account)
        creds = auth.getCreds()
        service = build('drive', 'v3', credentials=creds)
        fm = FolderManager(service)
        fm.create("madoda", "manager")

        print("base log folder id: ",fm.base_log_folder_id)
        print("log folder id: ",fm.log_folder_id)
        print("content folder id: ",fm.content_folder_id)
