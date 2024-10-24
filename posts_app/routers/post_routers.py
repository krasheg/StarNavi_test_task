from typing import List

from ninja import Router

from posts_app.ai_utils import ai_check_for_rude_words
from posts_app.jwt_utils import JWTAuth
from posts_app.models import Post
from posts_app.schemas import PostSchema, PostSchemaOutput
from django.contrib.auth import get_user_model

post_router = Router()


@post_router.post("/create", auth=JWTAuth())
def create_post(request, payload: PostSchema):
    user_model = get_user_model()
    user_data = request.auth
    user = user_model.objects.get(pk=user_data['id'])
    blocked = ai_check_for_rude_words(payload.content)
    post = Post.objects.create(
        author=user,
        title=payload.title,
        content=payload.content,
        blocked=blocked
    )
    return {"id": post.id, "title": post.title, 'blocked': post.blocked}


@post_router.get("/all_posts", response=List[PostSchemaOutput])
def get_posts(request):
    posts = Post.objects.all()
    return posts
