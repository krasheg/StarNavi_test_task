from ninja import Router
from posts_app.schemas import RegisterUserSchema, LoginUserSchema
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from posts_app.models import CustomUser

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
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        return {"error": "Invalid credentials"}
    return {"message": f"Welcome {user.username}!"}
