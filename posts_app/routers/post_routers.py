from ninja import Router

from posts_app.jwt_utils import JWTAuth
from posts_app.models import Post
from posts_app.schemas import PostSchema
from django.contrib.auth import get_user_model

post_router = Router()


@post_router.post("/create", auth=JWTAuth())
def create_post(request, payload: PostSchema):
    user_model = get_user_model()
    user_data = request.auth
    user = user_model.objects.get(pk=user_data['id'])
    post = Post.objects.create(
        author=user,
        title=payload.title,
        content=payload.content
    )
    return {"id": post.id, "title": post.title}


@post_router.get("/posts")
def get_posts(request):
    posts = Post.objects.filter(blocked=False)
    return [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
