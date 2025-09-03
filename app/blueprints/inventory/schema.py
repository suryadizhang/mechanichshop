from app.extention import ma
from app.models import Inventory
from marshmallow import fields, validate


class InventorySchema(ma.SQLAlchemyAutoSchema):
    """Schema for Inventory model serialization and validation"""

    class Meta:
        model = Inventory
        load_instance = True
        include_relationships = True

    # Explicitly define fields to match the model
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    description = fields.Str(allow_none=True)
    quantity = fields.Int(validate=validate.Range(min=0))
    category = fields.Str(validate=validate.Length(max=100))
    supplier = fields.Str(validate=validate.Length(max=100))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
