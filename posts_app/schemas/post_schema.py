from datetime import datetime

from ninja import Schema


class PostSchema(Schema):
    title: str
    content: str


class AuthorSchema(Schema):
    id: int
    username: str


class PostSchemaOutput(Schema):
    id: int
    title: str
    content: str
    author: AuthorSchema
    date_posted: datetime
    blocked: bool
