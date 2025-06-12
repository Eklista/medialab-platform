# backend/app/modules/auth/security/token_service.py
"""
Token Service - Gestión de tokens JWE para access tokens optimizados
"""
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwe, jwt
from jose.exceptions import JWEError, JWTError

from ..config.security_config import security_config
from ..exceptions.security_exceptions import InvalidTokenError, TokenExpiredError
from .crypto_service import crypto_service


class TokenService:
    """Servicio para gestión de tokens JWE/JWT"""
    
    def __init__(self):
        self.config = security_config
        self.crypto = crypto_service
        
        # Claves para JWE/JWT
        self._access_token_key = self._derive_access_token_key()
        self._refresh_token_key = self._derive_refresh_token_key()
    
    def _derive_access_token_key(self) -> str:
        """Deriva clave para access tokens"""
        # En producción, usar KMS o similar
        return self.config.TOKEN_MASTER_KEY + "_access"
    
    def _derive_refresh_token_key(self) -> str:
        """Deriva clave para refresh tokens si usáramos JWT"""
        return self.config.TOKEN_MASTER_KEY + "_refresh"
    
    # ===================================
    # ACCESS TOKEN MANAGEMENT (JWE)
    # ===================================
    
    def create_access_token(self, session_data: Dict[str, Any]) -> str:
        """
        Crea access token JWE con datos de sesión
        
        Args:
            session_data: Datos de la sesión activa
            
        Returns:
            Token JWE encriptado
            
        Raises:
            InvalidTokenError: Error al crear token
        """
        try:
            now = datetime.utcnow()
            expires_at = now + timedelta(minutes=self.config.ACCESS_TOKEN_DURATION_MINUTES)
            
            # Payload del token
            payload = {
                # Identificación
                "user_id": session_data["user_id"],
                "user_type": session_data["user_type"],
                "session_id": session_data["session_id"],
                
                # Timing estándar JWT
                "iat": int(now.timestamp()),
                "exp": int(expires_at.timestamp()),
                "jti": secrets.token_urlsafe(16),
                
                # Información de contexto
                "ip_address": session_data.get("ip_address"),
                "device_name": session_data.get("device_name"),
                "is_2fa_verified": session_data.get("is_2fa_verified", False),
                
                # Metadatos de seguridad
                "token_type": "access",
                "version": "1.0"
            }
            
            # Encriptar payload sensible
            encrypted_payload = self.crypto.encrypt_token_payload(payload)
            
            # Crear JWE
            jwe_token = jwe.encrypt(
                plaintext=encrypted_payload,
                key=self._access_token_key,
                algorithm=self.config.ACCESS_TOKEN_ALGORITHM,
                encryption=self.config.ACCESS_TOKEN_ENCRYPTION
            )
            
            return jwe_token
            
        except Exception as e:
            raise InvalidTokenError(f"Failed to create access token: {str(e)}", "access")

    async def validate_access_token(
        self, 
        token: str, 
        verify_session: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Valida access token JWE
        
        Args:
            token: Token JWE a validar
            verify_session: Si verificar sesión en Redis/MySQL
            
        Returns:
            Payload del token si es válido, None si inválido
            
        Raises:
            TokenExpiredError: Token expirado
            InvalidTokenError: Token inválido
        """
        try:
            # Desencriptar JWE
            encrypted_payload = jwe.decrypt(token, self._access_token_key)
            
            # Desencriptar payload interno
            payload = self.crypto.decrypt_token_payload(encrypted_payload)
            
            if not payload:
                raise InvalidTokenError("Failed to decrypt token payload", "access")
            
            # Verificar expiración
            now = datetime.utcnow().timestamp()
            if payload.get("exp", 0) < now:
                raise TokenExpiredError(
                    "Access token has expired",
                    "access",
                    datetime.fromtimestamp(payload["exp"]).isoformat()
                )
            
            # Verificar tipo de token
            if payload.get("token_type") != "access":
                raise InvalidTokenError("Invalid token type", "access")
            
            # Verificación adicional de sesión si es requerida
            if verify_session:
                session_valid = await self._verify_session_still_active(
                    payload.get("session_id")
                )
                if not session_valid:
                    raise InvalidTokenError("Session no longer active", "access")
            
            return payload
            
        except TokenExpiredError:
            raise
        except InvalidTokenError:
            raise
        except JWEError as e:
            raise InvalidTokenError(f"JWE validation failed: {str(e)}", "access")
        except Exception as e:
            raise InvalidTokenError(f"Token validation failed: {str(e)}", "access")
    
    async def _verify_session_still_active(self, session_id: Optional[str]) -> bool:
        """Verifica que la sesión siga activa en Redis"""
        if not session_id:
            return False
        
        try:
            from ..services.redis_auth_service import redis_auth_service
            session_data = await redis_auth_service.get_active_session(session_id)
            return session_data is not None
        except Exception:
            return False
    
    def extract_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Extrae información básica del usuario sin validación completa
        Útil para operaciones que no requieren verificación estricta
        
        Args:
            token: Token JWE
            
        Returns:
            Información básica del usuario o None
        """
        try:
            encrypted_payload = jwe.decrypt(token, self._access_token_key)
            payload = self.crypto.decrypt_token_payload(encrypted_payload)
            
            if payload:
                return {
                    "user_id": payload.get("user_id"),
                    "user_type": payload.get("user_type"),
                    "session_id": payload.get("session_id"),
                    "is_2fa_verified": payload.get("is_2fa_verified", False)
                }
        except Exception:
            pass
        
        return None
    
    # ===================================
    # REFRESH TOKEN MANAGEMENT (Opaque)
    # ===================================
    
    def create_refresh_token(self) -> str:
        """
        Crea refresh token opaco (no JWE para mayor control)
        
        Returns:
            Token opaco criptográficamente seguro
        """
        return secrets.token_urlsafe(32)
    
    def should_rotate_refresh_token(self, token_age_days: int) -> bool:
        """
        Determina si se debe rotar el refresh token
        
        Args:
            token_age_days: Edad del token en días
            
        Returns:
            True si se debe rotar
        """
        if not self.config.REFRESH_TOKEN_ROTATION:
            return False
        
        return token_age_days >= self.config.REFRESH_TOKEN_ROTATION_THRESHOLD_DAYS
    
    # ===================================
    # TOKEN UTILITIES
    # ===================================
    
    def is_token_format_valid(self, token: str) -> bool:
        """
        Verifica formato básico del token sin desencriptar
        
        Args:
            token: Token a verificar
            
        Returns:
            True si el formato es válido
        """
        try:
            # JWE tiene formato: header.encrypted_key.iv.ciphertext.tag
            parts = token.split('.')
            return len(parts) == 5
        except Exception:
            return False
    
    def get_token_metadata(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene metadatos del token sin validación completa
        
        Args:
            token: Token JWE
            
        Returns:
            Metadatos básicos o None
        """
        try:
            # Decodificar header sin verificar
            import base64
            header = token.split('.')[0]
            # Agregar padding si es necesario
            missing_padding = len(header) % 4
            if missing_padding:
                header += '=' * (4 - missing_padding)
            
            header_data = json.loads(base64.urlsafe_b64decode(header))
            
            return {
                "algorithm": header_data.get("alg"),
                "encryption": header_data.get("enc"),
                "type": header_data.get("typ", "JWE")
            }
        except Exception:
            return None
    
    def create_token_blacklist_entry(self, token: str, reason: str = "revoked") -> Dict[str, Any]:
        """
        Crea entrada para blacklist de tokens (para casos especiales)
        
        Args:
            token: Token a agregar a blacklist
            reason: Razón de revocación
            
        Returns:
            Entrada de blacklist
        """
        user_info = self.extract_user_info(token)
        
        return {
            "token_jti": user_info.get("jti") if user_info else None,
            "revoked_at": datetime.utcnow().isoformat(),
            "reason": reason,
            "user_id": user_info.get("user_id") if user_info else None,
            "user_type": user_info.get("user_type") if user_info else None
        }
    
    # ===================================
    # SECURITY HELPERS
    # ===================================
    
    def analyze_token_usage_pattern(self, tokens_used: list) -> Dict[str, Any]:
        """
        Analiza patrón de uso de tokens para detectar anomalías
        
        Args:
            tokens_used: Lista de tokens usados recientemente
            
        Returns:
            Análisis de patrones de uso
        """
        analysis = {
            "total_tokens": len(tokens_used),
            "unique_sessions": set(),
            "unique_devices": set(),
            "time_spread_hours": 0,
            "suspicious_patterns": []
        }
        
        if not tokens_used:
            return analysis
        
        timestamps = []
        
        for token in tokens_used:
            user_info = self.extract_user_info(token)
            if user_info:
                analysis["unique_sessions"].add(user_info.get("session_id"))
                analysis["unique_devices"].add(user_info.get("device_name"))
        
        # Convertir sets a conteos
        analysis["unique_sessions"] = len(analysis["unique_sessions"])
        analysis["unique_devices"] = len(analysis["unique_devices"])
        
        # Detectar patrones sospechosos
        if analysis["unique_devices"] > 3:
            analysis["suspicious_patterns"].append("multiple_devices")
        
        if analysis["unique_sessions"] > 5:
            analysis["suspicious_patterns"].append("multiple_sessions")
        
        return analysis

    async def get_token_health_status(self) -> Dict[str, Any]:
        """
        Obtiene estado de salud del sistema de tokens
        
        Returns:
            Estado de salud del servicio de tokens
        """
        health = {
            "token_service_available": True,
            "jwe_encryption_working": False,
            "key_rotation_due": False,
            "errors": []
        }
        
        try:
            # Test de creación y validación de token
            test_session = {
                "user_id": 1,
                "user_type": "test",
                "session_id": "test_session",
                "ip_address": "127.0.0.1"
            }
            
            test_token = self.create_access_token(test_session)
            validated_payload = await self.validate_access_token(test_token, verify_session=False)
            
            if validated_payload and validated_payload["user_id"] == 1:
                health["jwe_encryption_working"] = True
            else:
                health["errors"].append("Token validation test failed")
        
        except Exception as e:
            health["token_service_available"] = False
            health["errors"].append(f"Token service test failed: {str(e)}")
        
        return health


# Instancia singleton
token_service = TokenService()