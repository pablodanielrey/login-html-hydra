

"""
    https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    https://google-auth.readthedocs.io/en/latest/user-guide.html
    https://developers.google.com/identity/protocols/oauth2/scopes
"""

import httplib2
from google.auth import load_credentials_from_file
from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
from googleapiclient.discovery import build

def get_credentials(file, impersonate, scopes=[], lifetime=500):
    credentials = load_credentials_from_file(file)
    target_credentials = ImpersonatedCredentials(
        source_credentials=credentials,
        target_principal=impersonate,
        target_scopes=scopes,
        lifetime=lifetime) 
    return target_credentials   

def get_api(api, version, credentials):
    http = credentials.authorize(httplib2.Http())
    service = build(api, version, http=http)
    return service


