from __future__ import print_function
from google.oauth2 import service_account
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Auth:
    def __init__(self, SCOPES, credentials):
        self.SCOPES = SCOPES
        self.credentials = credentials
        self.creds = None
        self.is_service_account = False

        credfile = json.load(open(self.credentials, "r"))
        if credfile["type"] == "service_account":
            self.is_service_account = True        

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

