"""
Database models for the Mechanic Shop API
"""
from app.extention import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables for many-to-many relationships

# Links mechanics to service tickets (one mechanic can work on many tickets)
mechanic_service_ticket = db.Table('mechanic_service_ticket',
    db.Column('mechanic_id', db.Integer,
              db.ForeignKey('mechanics.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer,
              db.ForeignKey('service_tickets.id'), primary_key=True)
)

# Links inventory items to service tickets (tickets can need multiple parts)
inventory_service_ticket = db.Table('inventory_service_ticket',
    db.Column('inventory_id', db.Integer,
              db.ForeignKey('inventory.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer,
              db.ForeignKey('service_tickets.id'), primary_key=True)
)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relationships
    service_tickets = db.relationship('ServiceTicket', backref='customer',
                                      lazy=True,
                                      cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.name}>'


class Mechanic(db.Model):
    __tablename__ = 'mechanics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialty = db.Column(db.String(100))
    hourly_rate = db.Column(db.Numeric(10, 2))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relationships - Many-to-many with service tickets
    service_tickets = db.relationship('ServiceTicket',
                                      secondary=mechanic_service_ticket,
                                      back_populates='mechanics')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Mechanic {self.name}>'


class ServiceTicket(db.Model):
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            nullable=False)
    vehicle_info = db.Column(db.Text)
    estimated_cost = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50), default='Open')
    priority = db.Column(db.String(20), default='Medium')
    completion_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relationships
    # Many-to-many with mechanics
    mechanics = db.relationship('Mechanic',
                                secondary=mechanic_service_ticket,
                                back_populates='service_tickets')

    # Many-to-many with inventory items
    inventory_items = db.relationship('Inventory',
                                      secondary=inventory_service_ticket,
                                      back_populates='service_tickets')

    def calculate_total_cost(self):
        """Calculate total cost including labor and parts"""
        total_cost = float(self.estimated_cost or 0)

        # Add labor costs from assigned mechanics
        if self.mechanics:
            avg_rate = (sum(mechanic.hourly_rate for mechanic in
                           self.mechanics) / len(self.mechanics))
            # Assuming 2 hours of work - this could be made configurable
            total_cost += float(avg_rate) * 2

        # Add parts costs
        for item in self.inventory_items:
            total_cost += float(item.price)

        return round(total_cost, 2)

    def __repr__(self):
        return f'<ServiceTicket {self.title}>'


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(100))
    supplier = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Relationships
    service_tickets = db.relationship('ServiceTicket',
                                      secondary=inventory_service_ticket,
                                      back_populates='inventory_items')

    def __repr__(self):
        return f'<Inventory {self.name}>'
