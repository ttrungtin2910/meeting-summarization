"""
Data Transfer Objects (DTOs) for Application Layer.

This module contains classes that define the structure of data
transferred between different layers of the system, such as between
API routes and use case services.

DTOs in this package are independent from domain entities and are
tailored for specific use cases, validation rules, or transformations
required by application logic.

They help decouple the domain model from external representation
(e.g., API schemas) and support better separation of concerns.

Example usage:
    - Convert API request models to DTOs for service input
    - Format service output to DTOs before presenting to external layers
"""
