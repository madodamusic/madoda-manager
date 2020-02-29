from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Auth:
    def __init__(self, SCOPES, credentials):
        self.SCOPES = SCOPES
        self.credentials = credentials


    def auth(self):
        self.cards = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.cards = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.cards or not self.cards.valid:
            if self.cards and self.cards.expired and self.cards.refresh_token:
                self.cards.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                self.cards = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.cards, token)
            
        return self.cards

