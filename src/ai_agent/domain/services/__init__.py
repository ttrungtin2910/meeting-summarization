"""
Domain Services Module

This folder contains Domain Service classes responsible for coordinating complex
business logic that cannot naturally fit within a single Entity or Value Object.

A Domain Service:
- Operates across multiple Entities or Value Objects.
- Encapsulates domain-specific operations or validation rules.
- Does not maintain its own state (stateless behavior preferred).

Example services include DocumentValidator, DocumentSplitter.

Domain Services should only depend on Entities and Value Objects and should not
know about infrastructure or application layers.
"""
