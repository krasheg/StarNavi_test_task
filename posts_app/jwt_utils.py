import datetime

from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
import jwt
from django.conf import settings
from jwt.exceptions import InvalidTokenError


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            _, token = token.split(' ')
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_model = get_user_model()
            user = user_model.objects.get(pk=decoded['id'])
            if user.password != decoded['password']:  # If user changed it`s password while jwt exists,
                raise InvalidTokenError               # hash will be different
            if datetime.datetime.fromtimestamp(decoded['exp']) < datetime.datetime.utcnow():
                raise InvalidTokenError
            return decoded
        except InvalidTokenError:
            return None
