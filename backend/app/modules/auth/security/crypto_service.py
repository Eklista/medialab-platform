# backend/app/modules/auth/security/crypto_service.py
"""
Crypto Service - Encriptación segura de datos de sesión
"""
import json
import base64
import os
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.core.config import get_settings
from ..exceptions.security_exceptions import EncryptionError, DecryptionError


class CryptoService:
    """Servicio de encriptación para datos sensibles de autenticación"""
    
    def __init__(self):
        self.settings = get_settings()
        self._session_fernet = self._create_session_fernet()
        self._token_fernet = self._create_token_fernet()
    
    def _create_session_fernet(self) -> Fernet:
        """Crea instancia Fernet para encriptación de sesiones"""
        master_key = self.settings.SESSION_MASTER_KEY
        if not master_key:
            raise EncryptionError("SESSION_MASTER_KEY not configured")
        
        salt = self.settings.SESSION_ENCRYPTION_SALT.encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)
    
    def _create_token_fernet(self) -> Fernet:
        """Crea instancia Fernet para encriptación de tokens"""
        master_key = self.settings.TOKEN_MASTER_KEY
        if not master_key:
            raise EncryptionError("TOKEN_MASTER_KEY not configured")
        
        salt = self.settings.TOKEN_ENCRYPTION_SALT.encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=150000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)
    
    def encrypt_session_data(self, data: Dict[str, Any]) -> str:
        """
        Encripta datos de sesión para almacenamiento en Redis
        
        Args:
            data: Diccionario con datos de sesión
            
        Returns:
            String encriptado en base64
            
        Raises:
            EncryptionError: Error en proceso de encriptación
        """
        try:
            # Serializar a JSON
            json_data = json.dumps(data, default=str).encode('utf-8')
            
            # Encriptar
            encrypted_data = self._session_fernet.encrypt(json_data)
            
            # Codificar en base64 para almacenamiento
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            raise EncryptionError(f"Failed to encrypt session data: {str(e)}")
    
    def decrypt_session_data(self, encrypted_data: str) -> Optional[Dict[str, Any]]:
        """
        Desencripta datos de sesión desde Redis
        
        Args:
            encrypted_data: String encriptado en base64
            
        Returns:
            Diccionario con datos de sesión o None si falla
        """
        try:
            # Decodificar de base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            # Desencriptar
            decrypted_data = self._session_fernet.decrypt(encrypted_bytes)
            
            # Deserializar JSON
            return json.loads(decrypted_data.decode('utf-8'))
            
        except Exception as e:
            raise DecryptionError(f"Failed to decrypt session data: {str(e)}")
    
    def encrypt_sensitive_field(self, value: str) -> str:
        """
        Encripta campo sensible individual (IP, device info, etc.)
        
        Args:
            value: Valor a encriptar
            
        Returns:
            Valor encriptado en base64
        """
        try:
            encrypted_data = self._session_fernet.encrypt(value.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Failed to encrypt sensitive field: {str(e)}")
    
    def decrypt_sensitive_field(self, encrypted_value: str) -> Optional[str]:
        """
        Desencripta campo sensible individual
        
        Args:
            encrypted_value: Valor encriptado en base64
            
        Returns:
            Valor desencriptado o None si falla
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode('utf-8'))
            decrypted_data = self._session_fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode('utf-8')
        except Exception:
            return None
    
    def encrypt_token_payload(self, payload: Dict[str, Any]) -> str:
        """
        Encripta payload para tokens JWE
        
        Args:
            payload: Diccionario con datos del token
            
        Returns:
            Payload encriptado
        """
        try:
            json_data = json.dumps(payload, default=str).encode('utf-8')
            encrypted_data = self._token_fernet.encrypt(json_data)
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Failed to encrypt token payload: {str(e)}")
    
    def decrypt_token_payload(self, encrypted_payload: str) -> Optional[Dict[str, Any]]:
        """
        Desencripta payload de tokens JWE
        
        Args:
            encrypted_payload: Payload encriptado
            
        Returns:
            Diccionario con datos del token o None si falla
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_payload.encode('utf-8'))
            decrypted_data = self._token_fernet.decrypt(encrypted_bytes)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception:
            return None
    
    def mask_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enmascara datos sensibles para logging
        
        Args:
            data: Diccionario con datos que pueden ser sensibles
            
        Returns:
            Diccionario con datos enmascarados
        """
        masked_data = data.copy()
        
        # Campos que deben ser enmascarados
        sensitive_fields = {
            'ip_address': self._mask_ip,
            'user_agent': self._mask_user_agent,
            'device_fingerprint': self._mask_hash,
            'session_id': self._mask_hash,
            'refresh_token_id': self._mask_hash,
            'email': self._mask_email,
            'phone': self._mask_phone
        }
        
        for field, mask_func in sensitive_fields.items():
            if field in masked_data and masked_data[field]:
                masked_data[field] = mask_func(masked_data[field])
        
        return masked_data
    
    def _mask_ip(self, ip: str) -> str:
        """Enmascara dirección IP"""
        if '.' in ip:  # IPv4
            parts = ip.split('.')
            return f"{parts[0]}.{parts[1]}.xxx.xxx"
        elif ':' in ip:  # IPv6
            parts = ip.split(':')
            return f"{':'.join(parts[:2])}:xxxx:xxxx:xxxx:xxxx"
        return "xxx.xxx.xxx.xxx"
    
    def _mask_user_agent(self, user_agent: str) -> str:
        """Enmascara user agent manteniendo info básica"""
        if len(user_agent) > 50:
            return f"{user_agent[:30]}...{user_agent[-10:]}"
        return user_agent
    
    def _mask_hash(self, value: str) -> str:
        """Enmascara hash/ID manteniendo primeros y últimos caracteres"""
        if len(value) > 8:
            return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"
        return '*' * len(value)
    
    def _mask_email(self, email: str) -> str:
        """Enmascara email"""
        if '@' in email:
            local, domain = email.split('@', 1)
            masked_local = f"{local[0]}{'*' * (len(local) - 2)}{local[-1]}" if len(local) > 2 else '***'
            return f"{masked_local}@{domain}"
        return '***@***.***'
    
    def _mask_phone(self, phone: str) -> str:
        """Enmascara número telefónico"""
        if len(phone) > 4:
            return f"***-***-{phone[-4:]}"
        return '***-***-****'
    
    def rotate_keys(self) -> bool:
        """
        Rota claves de encriptación (para implementación futura)
        
        Returns:
            True si la rotación fue exitosa
        """
        # TODO: Implementar rotación de claves
        # 1. Generar nuevas claves
        # 2. Re-encriptar datos existentes
        # 3. Actualizar configuración
        return False
    
    def verify_encryption_health(self) -> Dict[str, Any]:
        """
        Verifica estado de salud del sistema de encriptación
        
        Returns:
            Diccionario con estado de salud
        """
        health_status = {
            'encryption_available': True,
            'session_encryption': True,
            'token_encryption': True,
            'last_key_rotation': None,
            'errors': []
        }
        
        try:
            # Test de encriptación/desencriptación
            test_data = {'test': 'encryption_health_check'}
            encrypted = self.encrypt_session_data(test_data)
            decrypted = self.decrypt_session_data(encrypted)
            
            if decrypted != test_data:
                health_status['session_encryption'] = False
                health_status['errors'].append('Session encryption test failed')
        
        except Exception as e:
            health_status['encryption_available'] = False
            health_status['errors'].append(f'Encryption health check failed: {str(e)}')
        
        return health_status


# Instancia singleton
crypto_service = CryptoService()