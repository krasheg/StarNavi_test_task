import datetime
from typing import Optional, List

from ninja import Schema


class CommentSchema(Schema):
    post_id: int
    content: str
    parent_id: int | None = None


class CommentAnalyticsSchema(Schema):
    date: datetime.datetime
    total_comments: int
    blocked_comments: int
