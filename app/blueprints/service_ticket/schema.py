from app.extention import ma
from app.models import ServiceTicket
from marshmallow import fields, validate


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Service Ticket model serialization and validation"""

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_relationships = True
        include_fk = True  # Include foreign keys like customer_id

    # Fields to match the actual model
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    customer_id = fields.Int(required=True)
    vehicle_info = fields.Str(validate=validate.Length(max=200))
    estimated_cost = fields.Float(validate=validate.Range(min=0))
    status = fields.Str(
        validate=validate.OneOf([
            'Open', 'In Progress', 'Completed', 'Cancelled'
        ])
    )
    priority = fields.Str(
        validate=validate.OneOf([
            'Low', 'Medium', 'High', 'Urgent'
        ])
    )
    completion_date = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
