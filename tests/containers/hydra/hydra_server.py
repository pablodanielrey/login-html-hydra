

from flask import Flask, jsonify, make_response, request
webapp = Flask(__name__)

@webapp.route('/oauth2/auth/requests/login', methods=['GET'])
def login_request():
    challenge = request.args.get('login_challenge')

    if not challenge:
        generic_error = {
            "debug": "The database adapter was unable to find the element",
            "error": "The requested resource could not be found",
            "error_description": "Object with ID 12345 does not exist",
            "status_code": 404
        }
        return make_response(jsonify(generic_error)), 404

    skip = False
    response_ok = {
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
        "skip": skip
    }
    return make_response(jsonify(response_ok)), 200


if __name__ == '__main__':
    webapp.run('0.0.0.0',4445)