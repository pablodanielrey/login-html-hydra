

"""
    https://github.com/googleapis/google-api-python-client/blob/master/docs/dyn/index.md
    https://google-auth.readthedocs.io/en/latest/user-guide.html
    https://developers.google.com/identity/protocols/oauth2/scopes
"""

from oauth2client.service_account import ServiceAccountCredentials
from google.auth import impersonated_credentials
from googleapiclient.discovery import build

def _get_credentials(file, impersonate, scopes=[], lifetime=500):    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(file, scopes)
    ''' uso una cuenta de admin del dominio para acceder a todas las apis '''
    admin_credentials = credentials.create_delegated(impersonate)
    
    return admin_credentials
        
    #source_credentials = (service_account.Credentials.from_service_account_file(file,scopes=scopes))   
    #target_credentials = impersonated_credentials.Credentials(
    #            source_credentials=source_credentials,
    #            target_principal=impersonate,
    #            target_scopes = scopes,
    #            lifetime=lifetime)
    #return target_credentials

def get_credentials(file, impersonate, scopes=[], lifetime=500):
    """
        https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md
    """
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file(file, scopes=scopes, subject=impersonate)
    return credentials    


def get_api(api, version, credentials):
    service = build(api, version, credentials=credentials)
    return service
