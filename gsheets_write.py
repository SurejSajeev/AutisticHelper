from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = r'C:\Users\surej\Downloads\renamedrivefiles-de0b98892de2.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and build the service
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = '1cQt9f5gbCgGAaPRfobbnoJRcVHxY9wZdFKUrP2MiLIU'

# Data to append
data = [
    ["Name", "Age", "City"],
    ["Alice", "30", "New York"],
    ["Bob", "25", "San Francisco"]
]

range_name = 'Sheet1!E1'
body = {
    'values': data
}

# Write data
result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range=range_name,
    valueInputOption='RAW',  # or 'USER_ENTERED'
    body=body
).execute()

print(f"{result.get('updatedCells')} cells updated.")
