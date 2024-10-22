from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from posts_app.routers import user_router, post_router, comment_router, auth_router


api = NinjaAPI()

# Add routers
api.add_router("/users/", user_router)
api.add_router("/posts/", post_router)
api.add_router("/comments/", comment_router)
api.add_router('/auth/', auth_router)
