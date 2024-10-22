from ninja import Schema


class PostSchema(Schema):
    title: str
    content: str
