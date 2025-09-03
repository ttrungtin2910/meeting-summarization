"""
Domain Exceptions Module

This folder contains Exception classes representing domain-specific business errors.

A Domain Exception:
- Represents a violation of business rules or domain logic.
- Is distinct from infrastructure-related errors (e.g., database errors, network errors).
- Should be caught and mapped to application-level or interface-level error handling.

Example domain exceptions include InvalidDocumentTypeError, FileTooLargeError.

Domain Exceptions must be pure Python classes derived from Python's built-in Exception class.
"""
