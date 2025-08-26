"""
Swagger API Documentation Configuration
This file defines the OpenAPI/Swagger specifications for the Mechanic Shop API
"""

swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "Mechanic Shop API",
        "description": "A comprehensive Flask API for managing a mechanic shop with customers, mechanics, service tickets, and inventory. Features JWT authentication, rate limiting, caching, and advanced queries.",
        "version": "1.0.0",
        "contact": {
            "name": "Mechanic Shop API Support",
            "email": "support@mechanicshop.com"
        }
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    },
    "definitions": {
        "Customer": {
            "type": "object",
            "required": ["name", "email", "phone", "password"],
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "John Doe"},
                "email": {"type": "string", "example": "john@example.com"},
                "phone": {"type": "string", "example": "555-123-4567"},
                "address": {"type": "string", "example": "123 Main St"},
                "password": {"type": "string", "example": "securepass123"}
            }
        },
        "Mechanic": {
            "type": "object",
            "required": ["name", "email", "phone", "specialty", "hourly_rate", "password"],
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Jane Smith"},
                "email": {"type": "string", "example": "jane@mechanicshop.com"},
                "phone": {"type": "string", "example": "555-123-4567"},
                "specialty": {"type": "string", "example": "Engine Repair"},
                "hourly_rate": {"type": "number", "example": 75.00},
                "password": {"type": "string", "example": "mechanic123"}
            }
        },
        "ServiceTicket": {
            "type": "object",
            "required": ["title", "description", "customer_id", "vehicle_info"],
            "properties": {
                "id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "Engine Repair"},
                "description": {"type": "string", "example": "Replace engine oil and filter"},
                "customer_id": {"type": "integer", "example": 1},
                "vehicle_info": {"type": "string", "example": "2020 Honda Civic"},
                "priority": {"type": "string", "enum": ["Low", "Medium", "High"], "example": "Medium"},
                "status": {"type": "string", "enum": ["Open", "In Progress", "Completed", "Cancelled"], "example": "Open"}
            }
        },
        "Inventory": {
            "type": "object",
            "required": ["name", "price"],
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Engine Oil Filter"},
                "price": {"type": "number", "example": 15.99},
                "quantity": {"type": "integer", "example": 50},
                "category": {"type": "string", "example": "Filters"},
                "supplier": {"type": "string", "example": "AutoParts Inc"}
            }
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {"type": "string", "example": "user@example.com"},
                "password": {"type": "string", "example": "password123"}
            }
        },
        "TokenResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Login successful"},
                "token": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string", "example": "Invalid input data"}
            }
        },
        "CustomerResponse": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "John Doe"},
                "email": {"type": "string", "example": "john@example.com"},
                "phone": {"type": "string", "example": "555-123-4567"},
                "address": {"type": "string", "example": "123 Main St"},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "BulkEditRequest": {
            "type": "object",
            "properties": {
                "add_ids": {
                    "type": "array", 
                    "items": {"type": "integer"}, 
                    "example": [2, 3]
                },
                "remove_ids": {
                    "type": "array", 
                    "items": {"type": "integer"}, 
                    "example": [1]
                }
            }
        },
        "PaginationResponse": {
            "type": "object",
            "properties": {
                "customers": {
                    "type": "array", 
                    "items": {"$ref": "#/definitions/CustomerResponse"}
                },
                "pagination": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pages": {"type": "integer", "example": 5},
                        "per_page": {"type": "integer", "example": 10},
                        "total": {"type": "integer", "example": 50},
                        "has_prev": {"type": "boolean", "example": False},
                        "has_next": {"type": "boolean", "example": True}
                    }
                }
            }
        },
        "Success": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Operation successful"}
            }
        }
    },
    "tags": [
        {"name": "health", "description": "API health check operations"},
        {"name": "customers", "description": "Customer management operations"},
        {"name": "mechanics", "description": "Mechanic management operations"},
        {"name": "service-tickets", "description": "Service ticket operations"},
        {"name": "inventory", "description": "Inventory management operations"}
    ]
}

# Swagger UI configuration
SWAGGER_UI_CONFIG = {
    'app_name': "Mechanic Shop API Documentation",
    'dom_id': '#swagger-ui',
    'url': '/swagger.json',
    'layout': 'StandaloneLayout'
}