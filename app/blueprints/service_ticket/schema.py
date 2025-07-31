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
    
    
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    vehicle_info = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200)
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )
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
    estimated_hours = fields.Float(allow_none=True)
    actual_hours = fields.Float(allow_none=True)
    parts_cost = fields.Float(allow_none=True)
    labor_cost = fields.Float(dump_only=True)
    total_cost = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)
    notes = fields.Str(allow_none=True)


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)