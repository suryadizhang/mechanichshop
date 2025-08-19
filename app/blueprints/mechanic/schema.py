from app.extention import ma
from app.models import Mechanic
from marshmallow import fields, validate, validates, ValidationError, post_load


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Mechanic model serialization and validation"""
    
    class Meta:
        model = Mechanic
        load_instance = False  # We'll handle instance creation manually
        include_relationships = True
        exclude = ('password_hash',) 
    
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
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, error="Password must be at least 6 characters")
    )
    created_at = fields.DateTime(dump_only=True)
    
    @validates('email')
    def validate_email_unique(self, value):
        """Custom validation to ensure email uniqueness"""
        existing_mechanic = Mechanic.query.filter_by(email=value).first()
        if existing_mechanic and existing_mechanic.id != getattr(self.instance, 'id', None):
            raise ValidationError('Email address already exists')
    
    @post_load
    def make_mechanic(self, data, **kwargs):
        """Create mechanic instance and handle password hashing"""
        # Extract password if present
        password = data.pop('password', None)
        
        # Create or update mechanic instance
        if self.instance:
            # Updating existing mechanic
            for key, value in data.items():
                setattr(self.instance, key, value)
            mechanic = self.instance
        else:
            # Creating new mechanic
            mechanic = Mechanic(**data)
        
        # Set password if provided
        if password:
            mechanic.set_password(password)
        
        return mechanic


class MechanicLoginSchema(ma.Schema):
    """Schema for mechanic login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
mechanic_login_schema = MechanicLoginSchema()