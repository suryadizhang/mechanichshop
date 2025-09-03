# 🔧 Mechanic Shop API

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![Tests](https://img.shields.io/badge/tests-76%20passing-brightgreen.svg)](tests/)
[![API Documentation](https://img.shields.io/badge/API-Swagger%20UI-orange.svg)](http://127.0.0.1:5000/api/docs)

A comprehensive REST API for managing a mechanic shop's operations, built with Flask and following professional development practices including complete API documentation, extensive testing, and robust authentication.

## 📋 Table of Contents

- [🔧 Mechanic Shop API](#-mechanic-shop-api)
  - [📋 Table of Contents](#-table-of-contents)
  - [🚀 Project Overview](#-project-overview)
    - [Key Features](#key-features)
    - [Technology Stack](#technology-stack)
    - [API Statistics](#api-statistics)
  - [🏗️ Architecture \& Design](#️-architecture--design)
    - [Project Structure](#project-structure)
    - [Database Schema](#database-schema)
    - [API Design Patterns](#api-design-patterns)
  - [⚡ Quick Start](#-quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
  - [🛠️ Detailed Setup Instructions](#️-detailed-setup-instructions)
    - [1. Environment Setup](#1-environment-setup)
    - [2. Dependency Installation](#2-dependency-installation)
    - [3. Database Configuration](#3-database-configuration)
    - [4. Environment Variables](#4-environment-variables)
    - [5. Application Startup](#5-application-startup)
  - [📖 API Documentation](#-api-documentation)
    - [Swagger UI](#swagger-ui)
    - [Authentication](#authentication)
    - [Available Endpoints](#available-endpoints)
  - [🧪 Testing](#-testing)
    - [Running Tests](#running-tests)
    - [Test Coverage](#test-coverage)
    - [Test Structure](#test-structure)
  - [🔒 Security Features](#-security-features)
  - [🚀 Advanced Features](#-advanced-features)
  - [🐛 Troubleshooting](#-troubleshooting)
  - [📚 API Usage Examples](#-api-usage-examples)
    - [Customer Registration \& Authentication](#customer-registration--authentication)
    - [Creating a Service Ticket](#creating-a-service-ticket)
    - [Managing Inventory](#managing-inventory)
  - [🤝 Contributing](#-contributing)
  - [📝 License](#-license)
  - [👨‍💻 Author](#-author)

## 🚀 Project Overview

The Mechanic Shop API is a production-ready REST API designed to manage all aspects of an automotive repair shop's operations. This system handles customer management, mechanic scheduling, service ticket tracking, and inventory management with a focus on security, scalability, and maintainability.

### Key Features

- **👥 Customer Management**: Registration, authentication, and profile management
- **🔧 Mechanic Administration**: Staff management with role-based access control
- **🎫 Service Tickets**: Complete workflow from creation to completion
- **📦 Inventory Management**: Parts tracking with quantity management
- **🔐 JWT Authentication**: Secure token-based authentication system
- **📚 Interactive Documentation**: Complete Swagger/OpenAPI documentation
- **🧪 Comprehensive Testing**: 76 tests with 100% pass rate
- **⚡ Performance Features**: Rate limiting, caching, and optimization
- **🛡️ Security**: Input validation, CORS protection, and secure headers

### Technology Stack

- **Backend Framework**: Flask 2.3.3
- **Database ORM**: SQLAlchemy with SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Flask-Swagger with OpenAPI 2.0
- **Validation**: Marshmallow schemas
- **Testing**: Python unittest framework
- **Security**: Flask-CORS, rate limiting, input sanitization

### API Statistics

- **25+ Endpoints** across 5 functional areas
- **4 Database Models** with complex relationships
- **76 Comprehensive Tests** (100% pass rate)
- **5 Blueprint Modules** for organized code structure
- **2 Authentication Roles** (Customer & Mechanic)

## 🏗️ Architecture & Design

### Project Structure

```
mechanic-shop-api/
│
├── app.py                     # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
│
├── app/                       # Main application package
│   ├── __init__.py
│   ├── models.py             # Database models
│   ├── auth.py               # Authentication utilities
│   ├── extention.py          # Flask extensions
│   ├── swagger_config.py     # Swagger configuration
│   │
│   ├── blueprints/           # API route blueprints
│   │   ├── customer/         # Customer management
│   │   ├── mechanic/         # Mechanic management
│   │   ├── service_ticket/   # Service ticket operations
│   │   └── inventory/        # Inventory management
│   │
│   └── static/
│       └── swagger.yaml      # OpenAPI specification
│
└── tests/                    # Comprehensive test suite
    ├── base_test.py          # Test base class
    ├── test_api_general.py   # General API tests
    ├── test_customers.py     # Customer endpoint tests
    ├── test_mechanics.py     # Mechanic endpoint tests
    ├── test_service_tickets.py # Service ticket tests
    └── test_inventory.py     # Inventory tests
```

### Database Schema

The API uses four interconnected models:

- **Customer**: User accounts for shop clients
- **Mechanic**: Staff accounts with administrative privileges
- **ServiceTicket**: Work orders with customer and mechanic relationships
- **Inventory**: Parts and materials with quantity tracking

### API Design Patterns

- **RESTful Design**: Standard HTTP methods and status codes
- **Blueprint Architecture**: Modular route organization
- **Schema Validation**: Marshmallow for request/response validation
- **Error Handling**: Consistent error responses with proper HTTP codes
- **Authentication**: JWT-based with role separation

## ⚡ Quick Start

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** package manager
- **Git** for cloning the repository

### Installation

```bash
# Clone the repository
git clone https://github.com/suryadizhang/mechanichshop.git
cd mechanichshop

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Running the Application

Once started, the API will be available at:

- **API Base URL**: http://127.0.0.1:5000
- **Swagger Documentation**: http://127.0.0.1:5000/api/docs
- **Health Check**: http://127.0.0.1:5000/health

## 🛠️ Detailed Setup Instructions

### 1. Environment Setup

**Step 1: Install Python**
- Download Python 3.8+ from [python.org](https://python.org)
- Verify installation: `python --version`

**Step 2: Clone Repository**
```bash
git clone https://github.com/suryadizhang/mechanichshop.git
cd mechanichshop
```

### 2. Dependency Installation

**Step 1: Create Virtual Environment**
```bash
# Create isolated Python environment
python -m venv venv

# Activate environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows Command Prompt:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate
```

**Step 2: Install Requirements**
```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 3. Database Configuration

The application uses SQLite and automatically creates the database:

```bash
# Database will be created automatically on first run
# Location: SQLite file in project directory
# Tables: customers, mechanics, service_tickets, inventory
```

### 4. Environment Variables

Create a `.env` file (optional) for custom configuration:

```bash
# .env file (optional)
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///mechanic_shop.db
JWT_SECRET_KEY=your-jwt-secret
```

### 5. Application Startup

```bash
# Start the Flask application
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

**Verification Steps:**
1. Open browser to http://127.0.0.1:5000/health
2. Should see: `{"status": "healthy", "timestamp": "..."}`
3. Visit http://127.0.0.1:5000/api/docs for Swagger UI
4. API is ready for use!

## 📖 API Documentation

### Swagger UI

The API includes comprehensive interactive documentation accessible at:
**http://127.0.0.1:5000/api/docs**

Features:
- **Interactive Testing**: Try endpoints directly from the browser
- **Request/Response Examples**: See expected data formats
- **Authentication Integration**: Test protected routes with JWT tokens
- **Parameter Documentation**: Detailed parameter descriptions
- **Schema Definitions**: Complete data model documentation

### Authentication

The API uses JWT (JSON Web Token) authentication with two user types:

**Customer Authentication:**
```bash
POST /customer/login
{
  "email": "customer@example.com",
  "password": "password123"
}
```

**Mechanic Authentication:**
```bash
POST /mechanic/login
{
  "email": "mechanic@example.com",
  "password": "password123"
}
```

**Using Tokens:**
Include the JWT token in the Authorization header:
```bash
Authorization: Bearer <your-jwt-token>
```

### Available Endpoints

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Customer** | 6 endpoints | Registration, login, profile management |
| **Mechanic** | 7 endpoints | Staff management, authentication, queries |
| **Service Tickets** | 8 endpoints | Create, assign, manage work orders |
| **Inventory** | 5 endpoints | Parts management, stock control |
| **General** | 2 endpoints | Health check, API information |

## 🧪 Testing

### Running Tests

**Run All Tests:**
```bash
# Comprehensive test suite
python -m unittest discover tests -v

# Quick test run (summary only)
python -m unittest discover tests --buffer
```

**Run Specific Test Categories:**
```bash
# Customer tests only
python -m unittest tests.test_customers -v

# Mechanic tests only  
python -m unittest tests.test_mechanics -v

# Service ticket tests only
python -m unittest tests.test_service_tickets -v

# Inventory tests only
python -m unittest tests.test_inventory -v

# General API tests only
python -m unittest tests.test_api_general -v
```

**Run Individual Tests:**
```bash
# Specific test method
python -m unittest tests.test_customers.TestCustomerRoutes.test_create_customer_success -v
```

### Test Coverage

- **76 Total Tests** with 100% pass rate
- **17 Customer Tests**: Registration, authentication, CRUD operations
- **15 Mechanic Tests**: Management, authentication, advanced queries  
- **17 Service Ticket Tests**: Creation, assignment, parts management
- **13 Inventory Tests**: CRUD with role-based access control
- **14 General Tests**: Security, CORS, rate limiting, error handling

### Test Structure

```python
# Example test structure
class TestCustomerRoutes(BaseTest):
    def test_create_customer_success(self):
        """Test successful customer creation"""
        # Positive test case

    def test_create_customer_invalid_email(self):
        """Test customer creation with invalid email"""
        # Negative test case

    def test_create_customer_missing_fields(self):
        """Test customer creation with missing required fields"""
        # Edge case testing
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Input Validation**: Marshmallow schemas prevent injection attacks
- **CORS Protection**: Configured cross-origin resource sharing
- **Rate Limiting**: Prevents API abuse and DoS attacks
- **Secure Headers**: Security-focused HTTP headers
- **Role-Based Access**: Separate permissions for customers and mechanics
- **Token Expiration**: Configurable JWT token lifetimes

## 🚀 Advanced Features

- **Blueprint Architecture**: Modular, scalable code organization
- **Automatic Documentation**: Self-updating Swagger/OpenAPI specs
- **Database Relationships**: Complex many-to-many relationships
- **Error Handling**: Comprehensive error responses with proper HTTP codes
- **Logging**: Detailed application logging for debugging
- **Configuration Management**: Environment-based configuration
- **Performance Optimization**: Caching and query optimization
- **Testing Infrastructure**: Comprehensive test base classes

## 🐛 Troubleshooting

**Common Issues and Solutions:**

**Issue: Port 5000 already in use**
```bash
# Solution 1: Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process-id> /F

# Solution 2: Use different port
# Edit app.py: app.run(port=5001)
```

**Issue: Virtual environment not activating**
```bash
# Windows PowerShell execution policy issue
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\Activate.ps1
```

**Issue: Module not found errors**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Database errors**
```bash
# Delete existing database and restart
del mechanic_shop.db  # Windows
rm mechanic_shop.db   # macOS/Linux
python app.py
```

**Issue: Tests failing**
```bash
# Run individual test to isolate issue
python -m unittest tests.test_customers.TestCustomerRoutes.test_create_customer_success -v

# Check test database isolation
# Tests use separate test database automatically
```

## 📚 API Usage Examples

### Customer Registration & Authentication

**1. Register a New Customer:**
```bash
curl -X POST http://127.0.0.1:5000/customer \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "password": "securepassword123"
  }'
```

**2. Customer Login:**
```bash
curl -X POST http://127.0.0.1:5000/customer/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

**3. Access Protected Route:**
```bash
curl -X GET http://127.0.0.1:5000/customer/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

### Creating a Service Ticket

**1. Create Service Ticket:**
```bash
curl -X POST http://127.0.0.1:5000/service_ticket \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <customer-jwt-token>" \
  -d '{
    "customer_id": 1,
    "description": "Oil change and tire rotation",
    "status": "pending"
  }'
```

**2. Assign Mechanic (Mechanic Role Required):**
```bash
curl -X PUT http://127.0.0.1:5000/service_ticket/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <mechanic-jwt-token>" \
  -d '{
    "mechanic_id": 1,
    "status": "in_progress"
  }'
```

### Managing Inventory

**1. Add Inventory Item (Mechanic Role Required):**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <mechanic-jwt-token>" \
  -d '{
    "name": "Motor Oil 5W-30",
    "description": "High-quality synthetic motor oil",
    "price": 29.99,
    "quantity": 50
  }'
```

**2. Update Inventory Quantity:**
```bash
curl -X PUT http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <mechanic-jwt-token>" \
  -d '{
    "quantity": 45
  }'
```

## 🤝 Contributing

We welcome contributions to improve the Mechanic Shop API! Here's how to get started:

**1. Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/mechanichshop.git
```

**2. Set Up Development Environment**
```bash
cd mechanichshop
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**3. Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

**4. Make Changes and Test**
```bash
# Make your changes
# Run tests to ensure nothing breaks
python -m unittest discover tests -v
```

**5. Submit Pull Request**
- Push your changes to your fork
- Create a pull request with detailed description
- Ensure all tests pass

**Development Guidelines:**
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use descriptive commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Surya Zhang**
- GitHub: [@suryadizhang](https://github.com/suryadizhang)
- Project: [Mechanic Shop API](https://github.com/suryadizhang/mechanichshop)

---

**🚀 Ready to start developing? Follow the [Quick Start](#-quick-start) guide and you'll be up and running in minutes!**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/suryadizhang/mechanichshop).
