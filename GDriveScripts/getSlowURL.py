import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os


def getLinks():
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    drive_service = build('drive', 'v3', credentials=creds)

    with open('keys.txt') as file:
        data = file.readlines()

    relation = []
    for i in range(len(data)):
        print(data[i])
        row = json.loads(data[i])
        fileID = row['id']
        fileName = row['name']
        fileURL = drive_service.files().get(fileId=fileID, fields='webViewLink').execute()
        shareable_link = fileURL['webViewLink']  # remove dictionary formatting
        relation.append([fileName, shareable_link])
    return relation


arr = getLinks()
print(arr[0])
f = open('relation.txt', 'w')
for i in range(len(arr)):
    print(arr[i])
    f.write('{titleID}, {url}'.format(titleID=arr[i][0], url=arr[i][1]))
    f.write('\n')
