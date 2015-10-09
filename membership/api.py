#!/usr/bin/env python3

import logging
import os

import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

APPLICATION_NAME = 'Hack@UCF Membership Updater v1'
FILE_ID = '1Cj8HQ8fKarE_6L2dDmG6ilva5ziyF_rSx8YBqm8BKUI'
CLIENT_SECRET = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
]

def _get_credentials(flags, client_secret):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir, 'drive-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to', credential_path)
    return credentials


def download_membership_file(flags, filename='membership.csv'):
    service = build_service(flags)

    file = service.files().get(fileId=FILE_ID).execute()
    url = file['exportLinks']['text/csv']
    logging.info('URL: {}'.format(url))
    resp, content = service._http.request(url)
    open(filename, 'wb').write(content)
    return content


def build_service(flags):
    _credentials = _get_credentials(flags, CLIENT_SECRET)
    _http = _credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=_http)
    return service
