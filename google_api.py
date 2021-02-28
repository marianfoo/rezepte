import requests
import json
import os
from apiclient import discovery
from google.oauth2 import service_account
import glob
import httplib2
import sys
class GoogleAPI:
    def __init__(self):
        with open('secrets.json') as json_file:
            json_file_secrets = json.load(json_file)
            self.spreadsheet_id = json_file_secrets["spreadsheet_id"]
            self.spreadsheet_id_recipe = json_file_secrets["spreadsheet_id_recipes"]
    def get_google_sheets_data(self):
        try:
            scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
            secret_file = os.path.join(os.getcwd(), 'client_secret.json')
            credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
            service = discovery.build('sheets', 'v4', credentials=credentials)

            request  = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range='A1:G300')
            response = request.execute()

            metadata = []
            length = len(response["values"])
            values = response["values"]
            for data in range(1, length):
                tupel = {}
                for value in range(len(values[data])):
                    tupel[response["values"][0][value]] = values[data][value]
                metadata.append(tupel)
            print("Metadata from Google Sheets loaded")
            return metadata
        except OSError as e:
            print (e)
    def get_recipes(self):
        try:
            scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
            secret_file = os.path.join(os.getcwd(), 'client_secret.json')
            credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
            service = discovery.build('sheets', 'v4', credentials=credentials)

            request  = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id_recipe, range='A1:F300')
            response = request.execute()

            metadata = []
            length = len(response["values"])
            values = response["values"]
            for data in range(1, length):
                tupel = {}
                for value in range(len(values[data])):
                    tupel[response["values"][0][value]] = values[data][value]
                metadata.append(tupel)
            print("Metadata from Google Sheets loaded")
            return metadata
        except OSError as e:
            print (e)
