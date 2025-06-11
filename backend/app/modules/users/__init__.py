"""
Users Module - Universidad Galileo MediaLab Platform

This module manages all user types and their relationships within the MediaLab ecosystem.
It handles both internal staff and external institutional users with proper role
and organizational assignments.

RESPONSIBILITIES:
- User account management and authentication data
- Internal vs Institutional user differentiation
- Role-based access assignments
- Organizational structure assignments (areas for internal, academic units for institutional)
- User profile and contact information management
- Account status and security features

CORE COMPONENTS:
- models/: Database models for users and their relationships
- schemas/: Pydantic models for API validation
- services/: Business logic for user operations
- repositories/: Data access layer for user data
- router.py: API endpoints for user management

USER TYPES:
- InternalUser: MediaLab staff with area assignments and dashboard access
- InstitutionalUser: University faculty, students, and external clients

RELATIONSHIP MODELS:
- UserRole: Many-to-many between users and security roles
- UserArea: Many-to-many between internal users and MediaLab areas
- UserAcademicUnit: Many-to-many between institutional users and academic units

This module uses a hybrid ID strategy (internal ID + public UUID) to balance
performance for internal operations with security for public APIs.
"""