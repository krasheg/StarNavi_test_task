from ninja import Router
from posts_app.models import Comment
from posts_app.schemas import CommentSchema

comment_router = Router()


@comment_router.post("/create")
def create_comment(request, payload: CommentSchema):
    user = request.user
    comment = Comment.objects.create(
        author=user,
        post_id=payload.post_id,
        content=payload.content
    )
    return {"id": comment.id, "content": comment.content}


@comment_router.get("/comments")
def get_comments(request):
    comments = Comment.objects.filter(blocked=False)
    return [{"id": comment.id, "content": comment.content} for comment in comments]
