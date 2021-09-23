import csv
import argparse
import yaml
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Manually paste in a personal API key here if you want to test locally
# API_KEY_OVERRIDE = "keeeeeeeyyyyyy"

SAMPLE_SPREADSHEET_ID = '1OX8TsLby-Ddn8WHa7yLKNpEERYN_RlScMrC0sbnT1Zs'
SAMPLE_RANGE_NAME = 'Automotive!A1:E'

if __name__ == '__main__':
    # Parse out arguments
    parser = argparse.ArgumentParser(description='Scrape Google Sheets and output CSV files')
    parser.add_argument('--api-key', help='The Google API key to use in scraping')
    args = parser.parse_args()

    apiKey = API_KEY_OVERRIDE if API_KEY_OVERRIDE else args.api_key

    if apiKey is None:
        raise RuntimeError(f"Missing required arg 'api_key'")

    # Build the Google Sheets API interface
    sheetConfigs = yaml.load(open('config/sheets.yaml', 'r'), Loader=yaml.FullLoader)
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
