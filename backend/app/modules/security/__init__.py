"""
Security Module - Universidad Galileo MediaLab Platform

This module handles the complete role-based access control (RBAC) system for the platform.
It provides secure authentication, authorization, and permission management for all users
across the MediaLab ecosystem.

RESPONSIBILITIES:
- Role and permission management
- User authorization and access control
- Security policy enforcement
- Audit trail for security-related actions

CORE COMPONENTS:
- models/: Database models for roles, permissions, and relationships
- schemas/: Pydantic models for API validation
- services/: Business logic for security operations
- repositories/: Data access layer for security entities
- router.py: API endpoints for security management

SECURITY FEATURES:
- Granular permission system
- Hierarchical role structure
- Multi-level access control
- Audit logging for all security operations
- Flexible role-permission assignments

This module ensures that only authorized users can access specific features
and maintains the integrity of the platform's security model.
"""