# backend/app/modules/auth/utils/__init__.py
"""
Auth utils module - Utilidades para autenticación
"""

from .device_detector import device_detector, DeviceDetector

__all__ = [
    # Services (instances)
    "device_detector",
    
    # Classes
    "DeviceDetector"
]