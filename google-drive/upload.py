from __future__ import print_function
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

import auth

class Upload:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials = os.path.join(os.getcwd(), "google-drive/credentials.json")
        # self.credentials = "credentials.json"
        self.auth = auth.Auth(self.SCOPES, self.credentials)
        self.creds = self.auth.getCreds()
        
        self.service = build('drive', 'v3', credentials=self.creds)

    def musicFolader(self):
        music_path = os.path.join(os.getcwd(), "musics")
        files = os.listdir(music_path)
        
        for file in files:
            upload_file = os.path.join(music_path, file)
            file_metadata = {'name': file}
            
            media = MediaFileUpload(upload_file, mimetype='audio/mpeg')
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            print("File ID: {}".format(file.get('id')))

        
        
if __name__ == "__main__":
    upload = Upload()
    upload.musicFolader()
