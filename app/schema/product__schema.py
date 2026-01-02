from marshmallow import Schema, fields, validate, ValidationError
from bson import ObjectId


class ObjectIdField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("Invalid ObjectId format")

    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)


class ProductSchema(Schema):
    # name = fields.String(required=True, validate=validate.Length(min=2))
    # image = fields.String(required=True)
    # price = fields.Number(required= True)
    # desc = fields.String(required=False, validate=validate.Length(min=5))
    userId = ObjectIdField(required=True) 
    name = fields.String(required=True, validate=validate.Length(min=2))
    image = fields.String(required=True)
    price = fields.Float(required=True)
    desc = fields.String(required=True)

    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
