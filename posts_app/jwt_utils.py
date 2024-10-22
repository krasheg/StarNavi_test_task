import datetime

from ninja.security import HttpBearer
import jwt
from django.conf import settings
from jwt.exceptions import InvalidTokenError


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            _, token = token.split(' ')
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if datetime.datetime.fromtimestamp(decoded['exp']) < datetime.datetime.utcnow():
                raise InvalidTokenError
            return decoded
        except InvalidTokenError:
            return None
