from celery import shared_task
from posts_app.ai_utils import ai_response_to_comment
from posts_app.models import CustomUser, Comment, Post
import time


@shared_task
def ai_answer_with_delay(post_author_id: int, post_id: int, comment_id: int):
    post_author = CustomUser.objects.get(id=post_author_id)
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    delay = post_author.autoreply_delay
    time.sleep(delay)
    post_text = post.content
    comment_text = comment.content
    ai_response = ai_response_to_comment(post_text, comment_text)
    Comment.objects.create(author=post_author,
                           content=ai_response,
                           post=post,
                           parent=comment
                           )