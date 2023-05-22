from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from google.oauth2.credentials import Credentials
import json

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def search_file():
    """
    Search file in drive location
    :return:
    """
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            response = service.files().list(q='mimeType="image/png"',
                                            spaces='drive',
                                            fields='nextPageToken, '
                                            'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
    print(len(files))
    return files

if __name__ == '__main__':
    arr = search_file()

    #f = open('keys.txt', 'w')
    # for i in range(len(arr)):
        # f.write(json.dumps(arr[i]))
        # f.write('\n')
