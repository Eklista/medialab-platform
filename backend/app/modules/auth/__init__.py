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
- security/: Security services (encryption, tokens, risk analysis)
- utils/: Utilities (device detection, helpers)
- exceptions/: Custom exception handling
- config/: Configuration management
- router.py: API endpoints for authentication

SECURITY FEATURES:
- Hybrid storage (Redis for speed, MySQL for audit)
- Advanced threat detection and risk analysis
- Automatic rate limiting with escalating blocks
- Location and device change detection
- Session management across multiple devices
- Comprehensive audit logging
- Encrypted session data in Redis
- JWE tokens for optimized access control

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

# Core controllers and services
from .controllers import auth_controller
from .services import auth_service, redis_auth_service

# Security services
from .security import crypto_service, token_service, risk_analyzer

# Utilities
from .utils import device_detector

# Configuration
from .config import (
    security_config, auth_config, session_config,
    rate_limit_config, risk_analysis_config, two_factor_config
)

# Router
from .router import router

__all__ = [
    # Core services
    "auth_controller",
    "auth_service", 
    "redis_auth_service",
    
    # Security services
    "crypto_service",
    "token_service",
    "risk_analyzer",
    
    # Utilities
    "device_detector",
    
    # Configuration
    "security_config",
    "auth_config", 
    "session_config",
    "rate_limit_config",
    "risk_analysis_config",
    "two_factor_config",
    
    # Router
    "router"
]