from flask import Flask, request, abort, jsonify
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from cryptography.fernet import Fernet
import hashlib

app = Flask(__name__)


plaintext = b"somerandomtext"
plaintext_str = 'somerandomtext'


def get_settings():
    path = 'C:\\Projects\\credentials\\udacity_api_settings.json'
    f = open(path)
    auth0_settings = json.load(f)

    return auth0_settings


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token, auth0_settings):
    AUTH0_DOMAIN = auth0_settings["AUTH0_DOMAIN"]
    ALGORITHMS = auth0_settings["ALGORITHMS"]
    API_AUDIENCE = auth0_settings["API_AUDIENCE"]

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def generate_key():
    # Generate a key
    key = Fernet.generate_key()

    # Instantiate a Fernet instance
    f = Fernet(key)

    return key


def encrypt(message, key):
    f = Fernet(key)
    ciphertext = f.encrypt(message)

    return ciphertext


def decrypt(message, key):
    f = Fernet(key)
    decryptedtext = f.decrypt(message)

    return decryptedtext


def hash(message):
    hashedtext = hashlib.md5(message.encode()).hexdigest()

    return hashedtext


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(403)
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth0_settings = get_settings()
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token, auth0_settings)
            except:
                abort(401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

# @app.route('/')
# def encrypt_decrypt_msg():
#     key = generate_key()
#
#     encrypted_msg = encrypt(plaintext, key)
#
#     decrypted_msg = decrypt(encrypted_msg, key)
#
#     hashed_msg = hash(plaintext_str)
#
#     return jsonify(
#         {
#             "key": str(key),
#             "plaint text": str(plaintext),
#             "encrypted text": str(encrypted_msg),
#             "decrypted text": str(decrypted_msg),
#             "md5 hashed text": str(hashed_msg)
#         }, 200
#     )


# @app.route('/headers')
# @requires_auth
# def headers(payload):
#     return 'Access Granted'


@app.route('/image')
@requires_auth('get:images')
def images(payload):
    return 'Access Granted'

#
# if __name__ == '__main__':
#     app.run()
