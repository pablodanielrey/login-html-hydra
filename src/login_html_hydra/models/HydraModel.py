"""
    implementa la api de hydra.
    referencia :
    https://www.ory.sh/docs/api/hydra/?version=latest
    https://www.ory.sh/docs/guides/master/hydra/3-overview/1-oauth2#implementing-a-login--consent-provider
"""
import logging
import requests
import datetime

class HydraModel:

    def __init__(self, hydra_api, verify=False):
        self.verify = verify
        self.hydra_api = hydra_api

    def get_login_challenge(self, challenge:str):
        url = f"{self.hydra_api}/oauth2/auth/requests/login"
        h = {
            'X-Forwarded-Proto':'https',
            'Accept': 'application/json'
        }
        r = requests.get(url, params={'login_challenge': challenge},headers=h, verify=self.verify)
        if r.status_code == 200:
            return (200, r.json())
        return (r.status_code, str(r))

    def accept_login_challenge(self, challenge:str, uid:str, data={}, remember=True):
        url = f"{self.hydra_api}/oauth2/auth/requests/login/accept"
        h = {
            'X-Forwarded-Proto':'https',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'subject': uid,
            'context': data,
            'remember':remember,
            'remember_for': 1 if not remember else 0
        }
        r = requests.put(url, params={'login_challenge': challenge}, headers=h, json=data, verify=self.verify)
        if r.status_code == 200:
            return (200, r.json())
        return (r.status_code, str(r))

    def deny_login_challenge(self, challenge:str, device_id:str, error:str):
        url = f"{self.hydra_api}/oauth2/auth/requests/login/reject"
        h = {
            'X-Forwarded-Proto':'https',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "error": error,
            "error_debug": error,
            "error_description": error,
            "error_hint": error,
            "status_code": 404
        }
        r = requests.put(url, params={'login_challenge': challenge}, headers=h, json=data, verify=self.verify)
        if r.status_code == 200:
            return (200, r.json())
        return (r.status_code, str(r))

    def get_consent_challenge(self, challenge:str):
        url = f"{self.hydra_api}/oauth2/auth/requests/consent"
        h = {
            'X-Forwarded-Proto':'https',
            'Accept': 'application/json'
        }
        r = requests.get(url, params={'consent_challenge': challenge},headers=h, verify=self.verify)
        if r.status_code == 200:
            return (200, r.json())
        return (r.status_code, str(r))

    def accept_consent_challenge(self, challenge:str, scopes=[], context={}, remember=True):
        url = f"{self.hydra_api}/oauth2/auth/requests/consent/accept"
        h = {
            'X-Forwarded-Proto':'https',
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'grant_scope': scopes,
            'remember':remember,
            'remember_for': 1 if not remember else 0,
            'session': {
                'access_token':context,
                'id_token': context
            }
        }
        r = requests.put(url, params={'consent_challenge': challenge}, headers=h, json=data, verify=self.verify)
        if r.status_code == 200:
            return (200, r.json())
        return (r.status_code, str(r))

    def process_user_login(self, session, challenge:str, user_id:str = None):

        if not user_id:
            """
            ''' login erróneo, chequeo la cantidad de intentos fallidos por device '''
            d = self.get_device_logins(session, device_id)
            if d.errors <= 5:
                d.errors = d.errors + 1
                remaining = 5 - d.errors
                return 404, {
                    'remaining': remaining
                }
            else:
                """
            status, data = self.deny_login_challenge(challenge, 'Credenciales incorrectas')
            if status != 200:
                raise Exception(data)

            response = {
                'redirect_to': data['redirect_to']
            }
            return 403, response
        else:
            status, data = self.accept_login_challenge(challenge, user_id, remember=False)
            if status != 200:
                raise Exception(data)

            response = {
                'redirect_to': data['redirect_to']
            }
            return  200, response

