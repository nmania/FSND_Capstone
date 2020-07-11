import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# for auth zero
AUTH0_DOMAIN = 'roofuseat.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:  # authorization not present
        abort(401)
    parts = auth.split()  # Split the string to get the needed parts
    if parts[0].lower() != 'bearer':  # Bearer not present
        abort(401)
    elif len(parts) == 1:  # Not enough parts
        abort(401)
    elif len(parts) > 2:  # Too many parts
        abort(401)
    token = parts[1]  # Get the token and return it
    return token


def check_permissions(permissions, payload):
    if 'permissions' not in payload:  # Check if permissions are present
        abort(401)
    # check if the correct permissions are present
    if permissions not in payload['permissions']:
        abort(401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:  # bad header
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:  # go through the keys and get kid
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:  # continue if rsa key has something there
        try:  # get the payload
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:  # expired
            abort(401)
        except jwt.JWTClaimsError:  # Invalid claim
            abort(401)
        except Exception:  # other exception
            aboort(401)
    # rsa_key was not filled
    abort(401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)  # veryfy the token
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
