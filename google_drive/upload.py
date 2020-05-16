from __future__ import print_function
import pickle
import os.path
from pathlib import Path
import os
import datetime
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload

from .auth import Auth
from .folder_manager import FolderManager
from .accounts_manager import AccountsManager
class Upload:
    def __init__(self, main_drive_folder_id="12NYDA17jfMGgHJazCIrWwfiZpe1o9w9S", musics_folder_path="main"):
        self.main_path = Path(__file__).parent.parent.absolute()
        
        if musics_folder_path == "main":
            self.musics_folder_path = os.path.join(str(self.main_path), "musics")
        else:
            self.musics_folder_path = musics_folder_path
            self.gdrive_folder_base_name = Path(str(self.musics_folder_path)).name
        
        self.accounts_manager = AccountsManager()
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        try:
            self.credentials = self.accounts_manager.getCred(self.musics_folder_path)
        except:
            self.credentials = False
            print("credentials not found")
            
        self.auth = Auth(self.SCOPES, self.credentials)
        self.creds = self.auth.getCreds()

        self.service = build('drive', 'v3', credentials=self.creds)

        self.main_drive_folder_id = main_drive_folder_id
        self.gdrive_folder_base_name = ""
       

        
        self.folder_manager = FolderManager(self.main_drive_folder_id, self.credentials)
        self.copy_folders_ids = []
        self.new_files_id = {}


    def _upload_multi_mp3(self, file_name, parent_ids):
        new_file_id = []
        if file_name.endswith(".mp3"):
            for parent_id in parent_ids:
                upload_file = os.path.join(self.musics_folder_path, file_name)
                file_metadata = {
                    'name': file_name, 
                    "parents": [parent_id]
                }
                media = MediaFileUpload(upload_file, mimetype='audio/mp3')
                Dfile = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                new_file_id.append(Dfile.get('id'))

            self.new_files_id.setdefault(file_name, new_file_id)

            return self.new_files_id
        else:
            return "error: not a mp3 file"

    
    def _upload_file(self, file, parent_id, mimetype= "text/plain"):
        file_metadata = {
            'name': os.path.basename(file), 
            "parents": [parent_id]
        }
        media = MediaFileUpload(file, mimetype=mimetype)
        Dfile = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return Dfile.get('id')


    def _create_file_with_all_ids(self, new_files_id):
        log_folder_path = os.path.join(str(self.main_path), "assets/gdrive_log")
        if self.gdrive_folder_base_name:
            log_name = str(self.gdrive_folder_base_name)
        else:
            log_name = str(datetime.datetime.today())
        
        log_file_text = os.path.join(log_folder_path, log_name+".txt")
        log_file_json = os.path.join(log_folder_path, log_name+".json")
        
        #create file with all drive urls to use with madoda_getway
        drive_urls = open("drive_urls.json", "w")
        drive_urls.write(json.dumps(new_files_id))
        drive_urls.close()
        
        #make file that is suported by madoda-music theme
        mdd_new_file_ids = str(new_files_id).replace("',", "&&\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("'", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace(":", ":\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("],", "\n\n\n")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("{", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("[", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("]", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace("}", "")
        mdd_new_file_ids = str(mdd_new_file_ids).replace(" ", "")
        
        if os.path.exists(log_folder_path):
            log_txt = open(log_file_text, "w")
            log_json = open(log_file_json, "w")
            
            log_txt.write(str(mdd_new_file_ids))
            log_json.write(json.dumps(new_files_id))
        else:
            os.makedirs(log_folder_path)
            log_txt = open(log_file_text, "w")
            log_json = open(log_file_json, "w")
            
            log_txt.write(str(mdd_new_file_ids))
            log_json.write(json.dumps(new_files_id))
        
        log_txt.close()
        log_json.close()
        return [log_file_text, log_file_json]
    
    def mp3(self):
        self.new_files_id = {}
        self.folder_manager.create()
        copy_folders_ids = self.folder_manager.getCopyFolderIds()
        files = os.listdir(self.musics_folder_path)
        for file in files:
            self._upload_multi_mp3(file, copy_folders_ids)
        
        log_files = self._create_file_with_all_ids(self.new_files_id)
        for log_file in log_files:
            self._upload_file(log_file, self.folder_manager.getLogFolderID())
        
        self.accounts_manager.update_account(self.credentials)
        return log_files[1]
        
