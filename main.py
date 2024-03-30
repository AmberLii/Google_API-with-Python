##
import os
from Google import Create_Service
import pandas as pd

CLIENT_SECRET_FILE = 'your json file name'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# https://docs.google.com/spreadsheets/d/XXXX/edit#gid=0
spreadsheet_id = 'XXXX'

# get
response = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    majorDimension='ROWS',
    range='hum1'
).execute()

columns = response['values'][0]
data = response['values'][1:]
df = pd.DataFrame(data, columns=columns)
print(df)


# batchGet
valueRanges_body = [
    'hum1!A1:E1000',
    'lig1!A1:E1000',
    'motion1!A1:E1000',
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
