from __future__ import print_function
import pickle
import os.path
import os
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import auth

class Upload:
    def __init__(self, main_drive_folder_id):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials = os.path.join(os.getcwd(), "google-drive/service.json")
        self.auth = auth.Auth(self.SCOPES, self.credentials)
        self.creds = self.auth.getCreds()

        self.service = build('drive', 'v3', credentials=self.creds)

        self.main_drive_folder_id = main_drive_folder_id
        self.copy_folders_ids = []

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
                    if file.get('parents')[0] == parent_folder_id:
                        return file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return False


    def musicFolader(self):
        main_folder_name = str(datetime.datetime.today().year)
        main_folder_id = self._ceackFolder(main_folder_name, self.main_drive_folder_id)
        if(main_folder_id):
            sub_folder_name = str(datetime.datetime.today().day)+"/"+str(datetime.datetime.today().month)
            sub_folder_id = self._ceackFolder(sub_folder_name, main_folder_id)
            if(sub_folder_id):
                #create copy folders
                pass
            else:
                file_metadata = {
                    'name': 'Drive api',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                file = self.service.files().create(body=file_metadata,
                                                    fields='id').execute()
                print('Folder ID: {}'.format(file.get('id')))
                
            
        else:
            print("no such folder")
        # file_metadata = {
        #     'name': 'Drive api',
        #     'mimeType': 'application/vnd.google-apps.folder'
        # }
        # file = self.service.files().create(body=file_metadata,
        #                                     fields='id').execute()
        # print('Folder ID: {}'.format(file.get('id')))
        
        
if __name__ == "__main__":
    upload = Upload("1k3kHkKOgFQCcKXkBJeJsFGMj4GVPJAS9")
    upload.musicFolader()
