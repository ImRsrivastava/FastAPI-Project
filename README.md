# Project Purpose

This project is a modular FastAPI-based backend application built to demonstrate clean API development, routing structure, and request validation using Pydantic models. It serves as a practical template for building scalable backend services in Python.

# The codebase showcases:

1.  Modular Routing Architecture The project separates API endpoints into dedicated route files:
    - authRoutes.py — handles authentication-related endpoints.
    - todoRoutes.py — manages Todo CRUD endpoints This ensures clean separation of features and easy scalability.

2.  Request/Response Validation with Pydantic All incoming API requests are validated using Pydantic models (located in the schemas/folder). This helps maintain data integrity and prevents invalid or malformed requests from reaching your business logic.

3.  Production-Ready FastAPI Application Structure The project follows a clean folder structure: main.py routers/ schemas/ This reflects real-world FastAPI best practices used in professional backend applications.

4.  Simple, Understandable API Design The project includes:
    - Authentication route (placeholder login).
    - Todo route (CRUD endpoints) These serve as foundational building blocks for any backend system such as: 
        • Task management system 
        • Authentication-enabled API 
        • Microservices backend 
        • Any CRUD-driven REST API

5.  Easy to Extend This project is intentionally kept lightweight so developers can easily:
    - Add database support (MySQL/PostgreSQL/SQLite/SQLAlchemy)
    - Add JWT authentication
    - Add service layers
    - Expand into a real production application