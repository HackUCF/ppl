#!/usr/bin/env python3
from datetime import datetime, timedelta
import logging
import os

from django.conf import settings
from django.core.cache import cache
import googleapiclient.errors
import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.client import OAuth2Credentials
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI
from social.apps.django_app.default.models import UserSocialAuth

APPLICATION_NAME = 'Hack@UCF Membership Updater v1'
FILE_ID = '1Cj8HQ8fKarE_6L2dDmG6ilva5ziyF_rSx8YBqm8BKUI'
CLIENT_SECRET = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
]

DOWNLOADABLE_CACHE_KEY = 'can_download_{}'.format(FILE_ID)


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


def build_service_from_credentials(credentials):
    http = credentials.authorize(httplib2.Http())
    return discovery.build('drive', 'v2', http=http)


def user_can_download_sheet(user):
    cache_key = '{}_{}'.format(user.email, DOWNLOADABLE_CACHE_KEY)
    if cache.get(cache_key, False):
        return True

    if download_sheet_with_user(user):
        cache.set(cache_key, True, 300)
        return True

    return False


def download_sheet_with_user(user, filename='membership.csv'):
    """
    Download the membership with a user's credentials

    :type user: users.models.User
    :param user:
    :return: boolean of successful download
    """
    try:
        social = UserSocialAuth.get_social_auth_for_user(user).get()
    except UserSocialAuth.DoesNotExist:
        return False

    extra = social.extra_data
    expiry = datetime.utcnow() + timedelta(seconds=int(extra['expires']))
    credentials = OAuth2Credentials(
        extra['access_token'],
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        extra['refresh_token'],
        expiry,
        GOOGLE_TOKEN_URI,
        None,
        revoke_uri=GOOGLE_REVOKE_URI
    )
    service = build_service_from_credentials(credentials)
    try:
        file = service.files().get(fileId=FILE_ID).execute()
    except googleapiclient.errors.HttpError:
        return False

    url = file['exportLinks']['text/csv']
    resp, content = service._http.request(url)
    open(filename, 'wb').write(content)
    return True
