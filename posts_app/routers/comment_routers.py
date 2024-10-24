from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from ninja import Router

from posts_app.ai_utils import ai_check_for_rude_words
from posts_app.jwt_utils import JWTAuth
from posts_app.models import Comment, Post
from posts_app.schemas import CommentSchema, CommentAnalyticsSchema
from django.shortcuts import get_object_or_404

from posts_app.utils import build_comment_tree
from posts_app.tasks import ai_answer_with_delay

comment_router = Router()


@comment_router.post("/create", auth=JWTAuth())
def create_comment(request, payload: CommentSchema):
    user_model = get_user_model()
    user_data = request.auth
    user = user_model.objects.get(pk=user_data['id'])
    blocked = ai_check_for_rude_words(payload.content)
    parent = None
    if payload.parent_id:
        parent = get_object_or_404(Comment, pk=payload.parent_id)
    comment = Comment.objects.create(
        author=user,
        post_id=payload.post_id,
        content=payload.content,
        blocked=blocked,
        parent=parent

    )
    # Get post author for checking if he had autoreply on his posts
    post = get_object_or_404(Post, pk=payload.post_id)
    post_author = post.author
    if post_author.autoreply and not blocked:
        ai_answer_with_delay.delay(post_author.id, post.id, comment.id)
    response = {"id": comment.id, "content": comment.content, 'blocked': blocked}
    if parent:
        response.update({"parent": parent.id})
    return response


@comment_router.get("/by_post_id/{post_id}")
def get_comments_by_post_id(request, post_id: int):
    comments = Comment.objects.filter(blocked=False, post__id=post_id).select_related('author')
    comment_tree = build_comment_tree(comments)
    return comment_tree


@comment_router.get("/comments-daily-breakdown", response=List[CommentAnalyticsSchema])
def comments_daily_breakdown(request, date_from: str, date_to: str):
    start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
    end_date = datetime.strptime(date_to, "%Y-%m-%d").date()

    analytics = (
        Comment.objects
        .filter(date_posted__date__range=(start_date, end_date))
        .annotate(date=TruncDate('date_posted'))
        .values('date')
        .annotate(
            total_comments=Count('id'),
            blocked_comments=Count('id', filter=Q(blocked=True))
        )
        .order_by('date')
    )

    return analytics
