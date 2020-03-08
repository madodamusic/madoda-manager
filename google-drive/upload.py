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
        self.credentials = os.path.join(os.getcwd(), "google-drive/service.json")
        self.auth = auth.Auth(self.SCOPES, self.credentials)
        self.creds = self.auth.getCreds()
        
        self.service = build('drive', 'v3', credentials=self.creds)

    def musicFolader(self):
        results = self.service.files().list(
        pageSize=2, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)            


        
        
if __name__ == "__main__":
    upload = Upload()
    upload.musicFolader()
