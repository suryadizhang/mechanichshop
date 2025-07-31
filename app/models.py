from app.extention import db  
from datetime import datetime

# Association table for many-to-many relationship between mechanics and service tickets
mechanic_service_ticket = db.Table('mechanic_service_ticket',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_tickets.id'), primary_key=True)
)

class Customer(db.Model):
    """Customer model representing shop customers"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service_tickets = db.relationship('ServiceTicket', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Mechanic(db.Model):
    """Mechanic model representing shop mechanics"""
    __tablename__ = 'mechanics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    years_experience = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with ServiceTicket
    service_tickets = db.relationship('ServiceTicket', secondary=mechanic_service_ticket, back_populates='mechanics')
    
    def __repr__(self):
        return f'<Mechanic {self.name}>'

class ServiceTicket(db.Model):
    """Service ticket model representing work orders"""
    __tablename__ = 'service_tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vehicle_info = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Open')  # Open, In Progress, Completed, Cancelled
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High, Urgent
    estimated_hours = db.Column(db.Float, default=0.0)
    actual_hours = db.Column(db.Float, default=0.0)
    parts_cost = db.Column(db.Float, default=0.0)
    labor_cost = db.Column(db.Float, default=0.0)
    total_cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    
    # Many-to-many relationship with Mechanic
    mechanics = db.relationship('Mechanic', secondary=mechanic_service_ticket, back_populates='service_tickets')
    
    def calculate_total_cost(self):
        """Calculate total cost based on labor and parts"""
        total_labor_cost = 0
        if self.mechanics and self.actual_hours:
            # Calculate average hourly rate if multiple mechanics
            avg_rate = sum(mechanic.hourly_rate for mechanic in self.mechanics) / len(self.mechanics)
            total_labor_cost = self.actual_hours * avg_rate
        self.labor_cost = total_labor_cost
        self.total_cost = self.labor_cost + self.parts_cost
        return self.total_cost
    
    def __repr__(self):
        return f'<ServiceTicket {self.id} - {self.status}>'