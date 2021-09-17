import sys
import urllib.request
import os.path
import yaml
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# import app.citycouncil.scraper
# import app.arguments

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1rumw5gXUbTGLU4fMrftfIYiMrtBeH2FGnXludd6SwZ8'

# Manually paste in a personal API key here if you want to test locally
API_KEY = "keeeeeeeyyyyyy"

SAMPLE_SPREADSHEET_ID = '1OX8TsLby-Ddn8WHa7yLKNpEERYN_RlScMrC0sbnT1Zs'
SAMPLE_RANGE_NAME = 'Automotive!A1:E'

if __name__ == '__main__':
    sheetConfigs = yaml.load(open('config/sheets.yaml', 'r'))
    apiService = build('sheets', 'v4', developerKey=API_KEY)
    sheetInterface = apiService.spreadsheets()

    for sheetConfig in sheetConfigs:
        sheetId = sheetConfig['sheetId']
        if sheetId is None:
            raise RuntimeError(f"Missing sheetId in sheet config")

        outputFilename = sheetConfig['outputFilename']
        if outputFilename is None:
            raise RuntimeError(f"Missing outputFilename for sheet config with sheetId {sheetId}")

        range = sheetConfig['range']
        if range is None:
            raise RuntimeError(f"Missing range for sheet config with sheetId {sheetId}")

        # Call the Sheets API
        result = sheetInterface.values().get(spreadsheetId=sheetId,
                                             range=range).execute()
        values = result.get('values', [])

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s' % (row[0], row[4]))
