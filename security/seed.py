import secrets

#semilla
secret_key = secrets.token_urlsafe(32)

#caracteristicas del token
ACCESS_TOKEN_DURATION = 30
ALGORITHM = 'HS256'