from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId

class ProductSchema(Schema):
    # name = fields.String(required=True, validate=validate.Length(min=2))
    # image = fields.String(required=True)
    # price = fields.Number(required= True)
    # desc = fields.String(required=False, validate=validate.Length(min=5))
    name = fields.String(required=True, validate=validate.Length(min=2))
    image = fields.String(required=True)
    price = fields.Float(required=True)
    desc = fields.String(required=True)

    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
