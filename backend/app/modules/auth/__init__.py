# backend/app/modules/auth/__init__.py
"""
Auth Module - Universidad Galileo MediaLab Platform

This module handles comprehensive authentication and session management for the platform.
It provides secure login/logout, 2FA, OAuth integration, and advanced security monitoring
using a hybrid architecture (MySQL + Redis) for optimal performance and auditability.

RESPONSIBILITIES:
- User authentication and session management
- Two-factor authentication (TOTP)
- OAuth/SSO integration (Google, Microsoft)
- Security monitoring and threat detection
- Rate limiting and brute force protection
- Device trust management
- User invitation system

CORE COMPONENTS:
- models/: Database models for auth entities (sessions, devices, attempts)
- schemas/: Pydantic models for API validation
- services/: Business logic for auth operations (hybrid MySQL+Redis)
- controllers/: Request handling and business logic coordination
- repositories/: Data access layer for auth data
- router.py: API endpoints for authentication

SECURITY FEATURES:
- Hybrid storage (Redis for speed, MySQL for audit)
- Advanced threat detection and risk analysis
- Automatic rate limiting with escalating blocks
- Location and device change detection
- Session management across multiple devices
- Comprehensive audit logging

AUTHENTICATION FLOW:
1. User submits credentials
2. Rate limiting check (Redis)
3. Credential validation
4. Risk analysis (location, device, behavior)
5. 2FA requirement evaluation
6. Session creation (Redis + MySQL)
7. Security event logging

This module ensures platform security while maintaining excellent user experience
through intelligent risk assessment and seamless authentication flows.
"""

# Import principales para facilitar uso externo
from .controllers import auth_controller
from .services import auth_service, redis_auth_service

__all__ = [
    "auth_controller",
    "auth_service", 
    "redis_auth_service"
]