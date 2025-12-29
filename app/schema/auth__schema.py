
from marshmallow import fields



class auth__schema():
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
