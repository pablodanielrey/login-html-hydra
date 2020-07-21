from flask import Flask, jsonify, make_response, request
webapp = Flask(__name__)

INVALID_CHALLENGE = 'invalidchallenge'
VALID_CHALLENGE = 'validchallenge'

@webapp.route('/oauth2/auth/requests/login/reject', methods=['PUT'])
def reject_login_request():
    """ https://www.ory.sh/hydra/docs/reference/api/#reject-a-login-request """

    generic_error = {
        "debug": "The database adapter was unable to find the element",
        "error": "The requested resource could not be found",
        "error_description": "Object with ID 12345 does not exist",
        "status_code": 404
    }        

    challenge = request.args.get('login_challenge')
    if challenge is None:
        generic_error['status_code'] = 500
        return make_response(jsonify(generic_error)), 500

    if INVALID_CHALLENGE == challenge:
        generic_error['status_code'] = 404
        return make_response(jsonify(generic_error)), 404


    body = request.json
    assert 'error' in body
    assert 'error_description' in body
    assert 'error_hint' in body
    assert 'status_code' in body

    """
        200	OK	completedRequest
        401	Unauthorized
        404	Not Found
        500	Internal Server Error
    """

    completedRequest = {
        'redirect_to': "http://rechazado.com/oauh_callback?error='dsasdadasd'"
    }
    return make_response(jsonify(completedRequest)), 200


@webapp.route('/oauth2/auth/requests/login/accept', methods=['PUT'])
def accept_login_request():
    """ https://www.ory.sh/hydra/docs/reference/api/#accept-a-login-request """

    generic_error = {
        "debug": "The database adapter was unable to find the element",
        "error": "The requested resource could not be found",
        "error_description": "Object with ID 12345 does not exist",
        "status_code": 404
    }        

    challenge = request.args.get('login_challenge')
    if challenge is None:
        generic_error['status_code'] = 500
        return make_response(jsonify(generic_error)), 500

    if INVALID_CHALLENGE == challenge:
        generic_error['status_code'] = 404
        return make_response(jsonify(generic_error)), 404


    body = request.json
    """ https://www.ory.sh/hydra/docs/reference/api/#schemaacceptloginrequest """
    assert 'subject' in body

    """
        200	OK	completedRequest
        401	Unauthorized
        404	Not Found
        500	Internal Server Error
    """

    completedRequest = {
        'redirect_to': "http://todook.cliente.com/oauh_callback?token='dsasdadasd'&blablabla=1"
    }
    return make_response(jsonify(completedRequest)), 200



@webapp.route('/oauth2/auth/requests/login', methods=['GET'])
def login_request():
    """
        https://www.ory.sh/hydra/docs/reference/api/#get-a-login-request 

        200	OK	loginRequest	loginRequest
        400	Bad Request	genericError	genericError
        404	Not Found	genericError	genericError
        409	Conflict	genericError	genericError
        500	Internal Server Error	genericError	genericError    
    """

    generic_error = {
        "debug": "The database adapter was unable to find the element",
        "error": "The requested resource could not be found",
        "error_description": "Object with ID 12345 does not exist",
        "status_code": 404
    }
    challenge = request.args.get('login_challenge')
    if not challenge:
        generic_error['status_code'] = 400
        return make_response(jsonify(generic_error)), 400

    if INVALID_CHALLENGE == challenge:
        generic_error['status_code'] = 404
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