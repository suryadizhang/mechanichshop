from app.extention import ma
from app.models import Customer
from marshmallow import fields, validate, validates, ValidationError, post_load


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Customer model - handles validation and JSON conversion"""
    
    class Meta:
        model = Customer
        load_instance = False  
        exclude = ('password_hash',)  # Don't expose password hash in JSON!
    
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
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, error="Password must be at least 6 characters")
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
    
    @post_load
    def make_customer(self, data, **kwargs):
        """Create customer instance and handle password hashing"""
        # Extract password if present
        password = data.pop('password', None)
        
        # Create or update customer instance
        if self.instance:
            # Updating existing customer
            for key, value in data.items():
                setattr(self.instance, key, value)
            customer = self.instance
        else:
            # Creating new customer
            customer = Customer(**data)
        
        # Set password if provided
        if password:
            customer.set_password(password)
        
        return customer


class LoginSchema(ma.Schema):
    """Schema for customer login"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# Schema instances for different use cases
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True, exclude=('service_tickets',))
customer_detail_schema = CustomerSchema()
login_schema = LoginSchema()