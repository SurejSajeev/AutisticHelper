from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = r'C:\Users\surej\Downloads\renamedrivefiles-de0b98892de2.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and build the service
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1cQt9f5gbCgGAaPRfobbnoJRcVHxY9wZdFKUrP2MiLIU'

# Read data
range_name = 'Sheet1!A1:C10'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    for row in values:
        print(row)
