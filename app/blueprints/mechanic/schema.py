from app.extention import ma
from app.models import Mechanic
from marshmallow import fields, validate


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Mechanic model serialization and validation"""
    
    class Meta:
        model = Mechanic
        load_instance = True
        include_relationships = True
    
    # Explicitly define fields
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    specialty = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    hourly_rate = fields.Float(required=True, validate=validate.Range(min=0))
    years_experience = fields.Int(validate=validate.Range(min=0))
    is_available = fields.Bool()
    created_at = fields.DateTime(dump_only=True)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)