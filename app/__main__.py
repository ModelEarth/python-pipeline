import csv
import os
import yaml
from googleapiclient.discovery import build

# Manually paste in a personal API key here if you want to test locally
API_KEY_OVERRIDE = None

SAMPLE_SPREADSHEET_ID = '1OX8TsLby-Ddn8WHa7yLKNpEERYN_RlScMrC0sbnT1Zs'
SAMPLE_RANGE_NAME = 'Automotive!A1:E'

if __name__ == '__main__':
    apiKey = API_KEY_OVERRIDE if API_KEY_OVERRIDE else os.environ.get('GOOGLE_API_KEY')

    if apiKey is None:
        raise RuntimeError(f"Missing required env var GOOGLE_API_KEY")

    # Build the Google Sheets API interface
    sheetConfigs = yaml.load(open('app/config/sheets.yaml', 'r'), Loader=yaml.FullLoader)
    apiService = build('sheets', 'v4', developerKey=apiKey)
    sheetInterface = apiService.spreadsheets()

    # Iterate over our sheet configurations
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

        # Call the Sheets API to get the actual values
        result = sheetInterface.values().get(spreadsheetId=sheetId,
                                             range=range).execute()
        values = result.get('values', [])

        if not values:
            print(f"No data fetched for sheet {sheetId}")
            continue

        # Open CSV file for writing
        with open(sheetConfig['outputFilename'], 'w', newline='') as csvFile:
            # Using the Unix dialect for now because it seems the most reasonable. Can switch to Excel if it makes
            #   more sense for whomever is using this output.
            writer = csv.writer(csvFile, dialect='unix')
            writer.writerows(values)
    # cleanup
    print(f"Successfully processed {len(sheetConfigs)} sheets")
