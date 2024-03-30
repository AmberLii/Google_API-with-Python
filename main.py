##
import os
from Google import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = 'your json file name'
API_NAME = 'sheets'
API_VERSION = 'v4'
# you can find SCOPES that API supported at: https://developers.google.com/sheets/api/scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# https://docs.google.com/spreadsheets/d/XXXX/edit#gid=0
spreadsheet_id = 'XXXX'

# get method
response = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    majorDimension='ROWS',
    # if range has only sheet_name, then it will read all cells that are not None
    range='sheet_name'
    # range='sheet name!A1:B5'
).execute()

# read the first row as columns
columns = response['values'][0]
# read the rest rows as data
data = response['values'][1:]
df = pd.DataFrame(data, columns=columns)
print(df)


# batchGet Method(read multiple tables at one time)
valueRanges_body = [
    'sheet_name1!A1:E1000',
    'sheet_name2!A1:E1000',
    'sheet_name3!A1:E1000',
]
response = service.spreadsheets().values().batchGet(
    spreadsheetId=spreadsheet_id,
    majorDimension='ROWS',
    ranges=valueRanges_body
).execute()

print(response['valueRanges'])

dataset = {}
for item in response['valueRanges']:
    dataset[item['range']] = item['values']

df = {}
for indx, k in enumerate(dataset):
    columns = dataset[k][0]
    data = dataset[k][1:]
    df[indx] = pd.DataFrame(data, columns=columns)
