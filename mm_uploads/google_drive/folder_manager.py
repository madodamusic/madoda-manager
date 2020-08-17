from __future__ import print_function
import datetime
# from googleapiclient.discovery import build
import os
from gdrive import Gdive
from google_drive.gdrive import Gdive
# from .auth import Auth

class FolderManager(Gdive):
    def __init__(self, gdrive_service):
        self.service = gdrive_service
        self.main_drive_folder_id = main_drive_folder_id
        self.__content_folder_id = ""
        self.copy_folders_ids = []
        self.log_folder_id = ""
        super().__init__()

    
    def __init_conf(self):
        self.__conf_file = Path("")
    
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


    
    def _get_base_folder_id(self):
        main_folder_name = str(datetime.datetime.today().year)
        sub_folder_name = str(datetime.datetime.today().month)

        main_folder_id = self._ceackFolder(main_folder_name, self.main_drive_folder_id)
        if main_folder_id:
            sub_folder_id = self._ceackFolder(sub_folder_name, main_folder_id)
            if not sub_folder_id:
                sub_folder_id = self.createNewFolder(sub_folder_name, main_folder_id)        
        else:
            main_folder_id = self.createNewFolder(main_folder_name, self.main_drive_folder_id)
            sub_folder_id = self.createNewFolder(sub_folder_name, main_folder_id)
        
        return sub_folder_id

    
    
    def create(self, folders):
        base_folder_id = self._get_base_folder_id()
        for index, folder in enumerate(folders):
            parent_id = folders[index -1]
            
            if index == 0:parent_id =  base_folder_id
               
            content_folder_id = self._ceackFolder(folder, parent_id)
            if not content_folder_id:
                content_folder_id = self.createNewFolder(folder, parent_id)
        
        return content_folder_id
                
    
    # def getLogFolderID(self):
        


fm = FolderManager("service")

print(fm.conf["main_folder_id"])
