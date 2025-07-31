from app.extention import ma
from app.models import Customer
from marshmallow import fields, validate, validates, ValidationError

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Customer model serialization and validation"""
    
    class Meta:
        model = Customer
        load_instance = True
    
    # Field validations
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=2, max=100, error="Name must be between 2 and 100 characters")
    )
    email = fields.Email(
        required=True,
        error_messages={'invalid': 'Invalid email address format'}
    )
    phone = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=20, error="Phone number must be between 10 and 20 characters")
    )
    address = fields.Str(
        validate=validate.Length(max=200, error="Address cannot exceed 200 characters")
    )
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Nested relationship (optional, for detailed views)
    service_tickets = fields.Nested('ServiceTicketSchema', many=True, exclude=('customer',), dump_only=True)
    
    @validates('email')
    def validate_email_unique(self, value):
        """Custom validation to ensure email uniqueness"""
        existing_customer = Customer.query.filter_by(email=value).first()
        if existing_customer and existing_customer.id != getattr(self.instance, 'id', None):
            raise ValidationError('Email address already exists')

# Schema instances for different use cases
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True, exclude=('service_tickets',))
customer_detail_schema = CustomerSchema()  