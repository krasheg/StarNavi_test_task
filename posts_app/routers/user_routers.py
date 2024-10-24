from ninja import Router

from posts_app.jwt_utils import JWTAuth
from posts_app.schemas import RegisterUserSchema, LoginUserSchema, AutoReplySchema
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model
from posts_app.models import CustomUser
import jwt
from django.conf import settings
from ninja import Router
from datetime import datetime, timedelta

user_router = Router()


@user_router.post("/register")
def register_user(request, payload: RegisterUserSchema):
    user = CustomUser.objects.create(
        username=payload.username,
        password=make_password(payload.password)
    )
    return {"id": user.id, "username": user.username}


@user_router.post("/login")
def login_user(request, payload: LoginUserSchema):
    username = payload.username
    password = payload.password
    user = authenticate(username=username, password=password)
    if user is not None:
        payload = {
            'id': user.id,
            'username': user.username,
            'password': user.password,  # We use hash for check if password wasn't changed
            'exp': datetime.utcnow() + timedelta(minutes=60),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return {'success': True, "access_token": token}
    return {"error": "Invalid credentials"}, 401


@user_router.post("/set_autoreply", auth=JWTAuth())
def set_autoreply(request, payload: AutoReplySchema):
    user_model = get_user_model()
    user_data = request.auth
    user = user_model.objects.get(pk=user_data['id'])
    if not user:
        return {"error": "Invalid credentials"}
    if payload.autoreply:
        user.autoreply = payload.autoreply
    if payload.autoreply_delay:
        user.autoreply_delay = payload.autoreply_delay
    user.save()
    return {"message": f"{user.username} autoreply was switched to {user.autoreply},"
                       f"autoreply delay: {payload.autoreply_delay} sec."}
