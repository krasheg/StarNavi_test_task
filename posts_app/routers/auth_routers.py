import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from ninja import Router
from datetime import datetime, timedelta

auth_router = Router()


@auth_router.post("/token")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if user is not None:
        payload = {
            'id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(minutes=60),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return {"access_token": token}
    return {"error": "Invalid credentials"}, 401
