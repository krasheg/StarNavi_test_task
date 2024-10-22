from ninja import Schema


class CommentSchema(Schema):
    post_id: int
    content: str
