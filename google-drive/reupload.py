from __future__ import print_function
from google.oauth2 import service_account
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import json
import os

music_path = os.path.join(os.getcwd(), "musics")

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = './google-drive/service.json'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

def download_file(id, file_name):
    file_id = id
    file_name = music_path+"/"+file_name
    # music = open("./musics/go.mp3", "wb")
    request = service.files().get_media(fileId=file_id)
    # fh = io.BytesIO()
    fh = io.FileIO(file_name, 'wb') 
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    down_status = 0
    while done is False:
        status, done = downloader.next_chunk()
        down_status = int(status.progress() * 100)

    return down_status


def upload_file(file_name, parent_ids):
    new_file_id = []
    for parent_id in parent_ids:
        upload_file = os.path.join(music_path, file_name)
        file_metadata = {
            'name': file_name, 
            "parents": [parent_id]
        }
        media = MediaFileUpload(upload_file, mimetype='audio/mp3')
        Dfile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        new_file_id.append(Dfile.get('id'))
        # uplog.write("'File Name:{}|| ID:{}|||',".format(file, Dfile.get('id')))
        # print("File Name:{}|| ID:{}|||".format(file, Dfile.get('id')))
    return new_file_id


def verify_name(file_name, done_files):
    for done_file in done_files:
        if done_file == file_name:
            return False

    return True



def reUploadAll():
    results = service.files().list(
        pageSize=25, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    all_ids = {}
    done_files = []
    if not items:
            print('No files found.')
    else:
        print('Files:')
        for item in items:
            if(item['name'].endswith(".mp3")):
                old_id = item['id']
                file_name = item['name']
                if verify_name(file_name, done_files):
                    if(download_file(old_id, file_name)):
                        new_file_ids = upload_file(file_name, [
                            "18-IMSoFJDoVttO9apnCA_Fm55vtkGJWp",
                            "1EPCuxCSiPgLYfN0lsiMa9lU_HPy0968l",
                            "1Iz0rmS86I6Oj82N4chtLjORKKJ8RfPZZ",
                            "1eAujAfAXX_nxdSTMjS4Q_peigikDUTCn",
                            "1AbVQ5RiSA9PrXx5swlfOYJiVCLGWCR9E",
                            "1-JcQF9LLJ5DCBLJNctphrzOKPiUAvbyq"
                        ])
                        all_ids.setdefault(old_id, new_file_ids)

                    done_files.append(file_name)
    
    
    return all_ids
    

all_ids = reUploadAll()

ids_log = open("driveIdsLog.json", "w")
ids_log.write(json.dumps(all_ids))  
ids_log.close()