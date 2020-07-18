import pytest
import requests
from pytest_httpserver import httpserver

def test_login_ok(httpserver):

    challenge = 'algodechallengeopaco'

    httpserver.expect_request('/oauth2/auth/requests/login').respond_with_json({
        "challenge": challenge,
        "client": {
            "allowed_cors_origins": [
                "string"
            ],
            "audience": [
                "string"
            ],
            "backchannel_logout_session_required": True,
            "backchannel_logout_uri": "string",
            "client_id": "string",
            "client_name": "string",
            "client_secret": "string",
            "client_secret_expires_at": 0,
            "client_uri": "string",
            "contacts": [
                "string"
            ],
            "created_at": "2020-06-23T09:16:53Z",
            "frontchannel_logout_session_required": True,
            "frontchannel_logout_uri": "string",
            "grant_types": [
                "string"
            ],
            "jwks": {},
            "jwks_uri": "string",
            "logo_uri": "string",
            "metadata": {},
            "owner": "string",
            "policy_uri": "string",
            "post_logout_redirect_uris": [
                "string"
            ],
            "redirect_uris": [
                "string"
            ],
            "request_object_signing_alg": "string",
            "request_uris": [
                "string"
            ],
            "response_types": [
                "string"
            ],
            "scope": "string",
            "sector_identifier_uri": "string",
            "subject_type": "string",
            "token_endpoint_auth_method": "string",
            "token_endpoint_auth_signing_alg": "string",
            "tos_uri": "string",
            "updated_at": "2020-06-23T09:16:53Z",
            "userinfo_signed_response_alg": "string"
        },
        "oidc_context": {
            "acr_values": [
                "string"
            ],
            "display": "string",
            "id_token_hint_claims": {},
            "login_hint": "string",
            "ui_locales": [
                "string"
            ]
        },
        "request_url": "string",
        "requested_access_token_audience": [
            "string"
        ],
        "requested_scope": [
            "string"
        ],
        "session_id": "string",
        "skip": True,
        "subject": "string"
    })

    params = {
        'username': 'usuario',
        'password': 'clave',
        'challenge': challenge
    }
    r = requests.post(login_url, params, allow_redirects=False)
    assert r.status_code == 200
    assert challenge in r.text
    assert 'Error de usuario' in r.text 

    
