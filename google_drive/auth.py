from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import json

class Auth:
    def __init__(self, SCOPES, credentials="none"):
        self.SCOPES = SCOPES
        self.credentials = credentials
        self.creds = None
        self.is_service_account = False
        
        if self.credentials != "none":
            try:
                credfile = json.load(open(self.credentials, "r"))  
                if credfile["type"] == "service_account":
                    self.is_service_account = True    
            except:
                pass
        else:
            
            try:
                cread_dir = os.listdir("google_drive/accounts")
                full_accounts = open("google_drive/logs/full_accounts.txt", "r").read().split("\n")
                print(full_accounts)
                for cread in cread_dir:
                    print(cread)
                    if cread not in full_accounts and cread.endswith(".json"):
                        print("acount not full")
                        self.credentials = cread
                        print(self.credentials)
                        print(json.load(open("./credentials.json", "r")) )
                        print("hiiiii")
                        print(credfile) 
                        # if credfile["type"] == "service_account":
                        #     self.is_service_account = True
                        #     print("ceck type")
                        
                        # break  
                    else:
                        print("account full")          
            except:
                print("error on find credential")
        
                    

    def __auth(self):
        
        if self.is_service_account: 
            self.creds = service_account.Credentials.from_service_account_file(self.credentials, scopes=self.SCOPES)
        else:
            # The file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials, self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

    def getCreds(self):
        self.__auth()
        return self.creds


if __name__ == "__main__":
    SCOPES = ['https://www.googleapis.com/auth/drive']
    auth = Auth(SCOPES)
    # auth = Auth(SCOPES, "google_drive/service.json")
    creds = auth.getCreds()    
    service = build('drive', 'v3', credentials=creds)
    # res = service.about().get().execute()
    res = service.about().get(fields = "user, storageQuota").execute()
    # print(res["storageQuota"]["usage"])
    # print(res["storageQuota"]["limit"])
    print(res["user"]["emailAddress"])
