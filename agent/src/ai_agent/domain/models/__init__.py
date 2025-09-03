"""
Models Module (Entities)

This folder contains Entity classes that represent the core business objects
within the system.

An Entity:
- Has a unique identity (e.g., ID).
- Possesses a lifecycle (creation, modification, deletion).
- Contains business rules and logic related to its state.
- Is independent from infrastructure concerns (no database or API dependencies).

Example entities include Document, DocumentChunk, User.

Entities must be pure Python classes and must not inherit from ORM frameworks
such as SQLAlchemy's Base or FastAPI's BaseModel.
"""
