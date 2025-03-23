from marshmallow import fields
from marshmallow import Schema


class WordSchema(Schema):
    writing = fields.Str()
    reading = fields.Str()
    definition = fields.Str()