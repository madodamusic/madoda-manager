from __future__ import print_function
from google.oauth2 import service_account
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient import errors

SCOPES = ['https://www.googleapis.com/drive/v3/about']
SERVICE_ACCOUNT_FILE = './google_drive/service.json'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# ...


about = service.about().get().execute()
print(about)
# print( "Current user name: {}".format(about['name']) )
# print( "Root folder ID: {}".format( about['rootFolderId']) )
# print( "Total quota (bytes): {}".format(about['quotaBytesTotal']) )
# print( "Used quota (bytes): {}".format(about['quotaBytesUsed']) )


# music_path = os.path.join(os.getcwd(), "musics")
# files = os.listdir(music_path)
# # uplog = open("uploadLog.txt", "a")
# # print("start upload files")
# # for file in files:
# #     upload_file = os.path.join(music_path, file)
# #     file_metadata = {
# #         'name': file, 
# #         "parents": ['1HCQz3IoxGi2bEV0JGceLtQm-Z6nqXExh']
# #     }
# #     media = MediaFileUpload(upload_file, mimetype='audio/mp3')
# #     Dfile = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# #     uplog.write("'File Name:{}|| ID:{}|||',".format(file, Dfile.get('id')))
# #     print("File Name:{}|| ID:{}|||".format(file, Dfile.get('id')))

# def verify_name(file_name, done_files):
#     for done_file in done_files:
#         if done_file == file_name:
#             return False

#     return True


# # uplog.close()
# # print("end upload files")
# # print("")
# # Call the Drive v3 API
# results = service.files().list(
#     pageSize=25, fields="nextPageToken, files(id, name)").execute()
# items = results.get('files', [])
# done_files = []
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         if verify_name(item['name'], done_files):
#             print(item)
#             done_files.append(item['name'])
        

