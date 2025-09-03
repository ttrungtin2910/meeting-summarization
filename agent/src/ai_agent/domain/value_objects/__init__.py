"""
Value Objects Module

This folder contains Value Object classes representing immutable descriptive
elements within the business domain.

A Value Object:
- Does not have a unique identity.
- Is compared based on its values, not reference.
- Typically represents small pieces of data (e.g., a filename metadata, an email address).
- Is tightly coupled with Entities but does not possess independent lifecycle.

Example value objects include FileMetadata, EmailAddress.

Value Objects must be pure Python classes, free from any external dependencies.
"""
