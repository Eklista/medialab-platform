# backend/app/modules/auth/services/redis_auth_service.py
"""
Redis Auth Service - Gestión de datos temporales de autenticación con encriptación
"""
import json
import redis
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from app.core.config import get_settings
from ..security.crypto_service import crypto_service
from ..config.security_config import rate_limit_config
from ..exceptions.security_exceptions import EncryptionError, RateLimitExceeded


@dataclass
class LoginAttemptData:
    """Estructura para intentos de login en Redis"""
    identifier: str
    ip_address: str
    timestamp: datetime
    failure_reason: str
    user_agent: str
    risk_score: int


@dataclass
class RateLimitResult:
    """Resultado de rate limiting"""
    is_allowed: bool
    attempts_count: int
    max_attempts: int
    reset_time: datetime
    blocked_until: Optional[datetime] = None


class RedisAuthService:
    """Servicio Redis para autenticación temporal con encriptación"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )
        
        # Servicios de seguridad
        self.crypto = crypto_service
        self.rate_config = rate_limit_config
        
        # Configuraciones de rate limiting
        self.RATE_LIMITS = self.rate_config.get_rate_limits()
    
    # ===================================
    # RATE LIMITING
    # ===================================
    
    async def check_rate_limit(self, identifier: str, limit_type: str = 'user') -> RateLimitResult:
        """
        Verifica rate limiting para IP o usuario
        """
        config = self.RATE_LIMITS[limit_type]
        key = f"rate_limit:{limit_type}:{identifier}"
        
        # Verificar bloqueo temporal
        blocked_key = f"blocked:{limit_type}:{identifier}"
        blocked_until = self.redis_client.get(blocked_key)
        
        if blocked_until:
            return RateLimitResult(
                is_allowed=False,
                attempts_count=config['max_attempts'],
                max_attempts=config['max_attempts'],
                reset_time=datetime.fromisoformat(blocked_until),
                blocked_until=datetime.fromisoformat(blocked_until)
            )
        
        # Usar sliding window con sorted sets
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=config['window_minutes'])
        
        # Limpiar intentos antiguos
        self.redis_client.zremrangebyscore(key, 0, window_start.timestamp())
        
        # Contar intentos en ventana actual
        current_attempts = self.redis_client.zcard(key)
        
        # Calcular tiempo de reset
        oldest_attempt = self.redis_client.zrange(key, 0, 0, withscores=True)
        reset_time = now + timedelta(minutes=config['window_minutes'])
        if oldest_attempt:
            reset_time = datetime.fromtimestamp(oldest_attempt[0][1]) + timedelta(minutes=config['window_minutes'])
        
        return RateLimitResult(
            is_allowed=current_attempts < config['max_attempts'],
            attempts_count=current_attempts,
            max_attempts=config['max_attempts'],
            reset_time=reset_time
        )
    
    async def record_failed_attempt(self, identifier: str, limit_type: str = 'user') -> bool:
        """
        Registra intento fallido y aplica bloqueo si es necesario
        """
        config = self.RATE_LIMITS[limit_type]
        key = f"rate_limit:{limit_type}:{identifier}"
        now = datetime.utcnow()
        
        # Agregar intento actual
        self.redis_client.zadd(key, {str(now.timestamp()): now.timestamp()})
        
        # Verificar si se debe bloquear
        current_attempts = self.redis_client.zcard(key)
        
        if current_attempts >= config['max_attempts']:
            # Aplicar bloqueo temporal (escalamiento)
            block_duration = self._calculate_block_duration(identifier, limit_type)
            blocked_until = now + timedelta(minutes=block_duration)
            
            blocked_key = f"blocked:{limit_type}:{identifier}"
            self.redis_client.setex(
                blocked_key, 
                int(timedelta(minutes=block_duration).total_seconds()),
                blocked_until.isoformat()
            )
            
            return True
        
        # Expirar la clave después de la ventana
        self.redis_client.expire(key, config['window_minutes'] * 60)
        return False
    
    def _calculate_block_duration(self, identifier: str, limit_type: str) -> int:
        """Calcula duración de bloqueo con escalamiento"""
        block_count_key = f"block_count:{limit_type}:{identifier}"
        block_count = int(self.redis_client.get(block_count_key) or 0)
        
        # Obtener duraciones de configuración
        durations = self.rate_config.get_block_durations()
        duration = durations[min(block_count, len(durations) - 1)]
        
        # Incrementar contador de bloqueos
        self.redis_client.incr(block_count_key)
        self.redis_client.expire(block_count_key, 24 * 3600)  # Reset cada 24h
        
        return duration
    
    # ===================================
    # INTENTOS FALLIDOS TEMPORALES (ENCRIPTADOS)
    # ===================================
    
    async def store_failed_attempt(self, attempt_data: LoginAttemptData) -> None:
        """Guarda intento fallido temporal ENCRIPTADO en Redis"""
        key = f"failed_attempts:{attempt_data.identifier}"
        
        attempt_info = {
            'ip_address': attempt_data.ip_address,
            'timestamp': attempt_data.timestamp.isoformat(),
            'failure_reason': attempt_data.failure_reason,
            'user_agent': attempt_data.user_agent,
            'risk_score': attempt_data.risk_score
        }
        
        try:
            # 🔐 ENCRIPTAR datos sensibles
            encrypted_attempt = self.crypto.encrypt_session_data(attempt_info)
            
            # Usar lista para mantener orden cronológico
            self.redis_client.lpush(key, encrypted_attempt)
            
            # Mantener solo últimos 50 intentos
            self.redis_client.ltrim(key, 0, 49)
            
            # Expirar después de 24 horas
            self.redis_client.expire(key, 24 * 3600)
            
        except EncryptionError as e:
            # Fallback a almacenamiento sin encriptar si falla
            self.redis_client.lpush(key, json.dumps(attempt_info))
            self.redis_client.ltrim(key, 0, 49)
            self.redis_client.expire(key, 24 * 3600)
    
    async def get_recent_failed_attempts(self, identifier: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtiene intentos fallidos recientes DESENCRIPTADOS"""
        key = f"failed_attempts:{identifier}"
        encrypted_attempts = self.redis_client.lrange(key, 0, limit - 1)
        
        attempts = []
        for encrypted_attempt in encrypted_attempts:
            try:
                # 🔓 DESENCRIPTAR datos
                attempt_data = self.crypto.decrypt_session_data(encrypted_attempt)
                if attempt_data:
                    attempts.append(attempt_data)
            except Exception:
                # Intentar como JSON sin encriptar (fallback)
                try:
                    attempt_data = json.loads(encrypted_attempt)
                    attempts.append(attempt_data)
                except Exception:
                    continue  # Saltar intentos corruptos
        
        return attempts
    
    # ===================================
    # SESIONES ACTIVAS (ENCRIPTADAS)
    # ===================================
    
    async def store_active_session(self, session_id: str, session_data: Dict[str, Any], ttl_hours: int = 24) -> None:
        """Guarda sesión activa ENCRIPTADA en Redis"""
        key = f"active_session:{session_id}"
        
        # Agregar timestamps
        session_data['created_at'] = datetime.utcnow().isoformat()
        session_data['last_activity'] = datetime.utcnow().isoformat()
        
        try:
            # 🔐 ENCRIPTAR datos de sesión
            encrypted_data = self.crypto.encrypt_session_data(session_data)
            
            self.redis_client.setex(
                key,
                int(timedelta(hours=ttl_hours).total_seconds()),
                encrypted_data
            )
            
        except EncryptionError:
            # Fallback a almacenamiento sin encriptar
            self.redis_client.setex(
                key,
                int(timedelta(hours=ttl_hours).total_seconds()),
                json.dumps(session_data, default=str)
            )
        
        # Mantener índice por usuario (solo IDs, no datos sensibles)
        user_sessions_key = f"user_sessions:{session_data['user_type']}:{session_data['user_id']}"
        self.redis_client.sadd(user_sessions_key, session_id)
        self.redis_client.expire(user_sessions_key, ttl_hours * 3600)
    
    async def get_active_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene y DESENCRIPTA datos de sesión activa"""
        key = f"active_session:{session_id}"
        encrypted_data = self.redis_client.get(key)
        
        if not encrypted_data:
            return None
        
        try:
            # 🔓 DESENCRIPTAR datos
            session_data = self.crypto.decrypt_session_data(encrypted_data)
            return session_data
        except Exception:
            # Intentar como JSON sin encriptar (fallback/migración)
            try:
                return json.loads(encrypted_data)
            except Exception:
                return None
    
    async def update_session_activity(self, session_id: str) -> bool:
        """Actualiza última actividad de sesión ENCRIPTADA"""
        key = f"active_session:{session_id}"
        session_data = await self.get_active_session(session_id)
        
        if session_data:
            session_data['last_activity'] = datetime.utcnow().isoformat()
            
            # Mantener TTL actual
            ttl = self.redis_client.ttl(key)
            if ttl > 0:
                try:
                    encrypted_data = self.crypto.encrypt_session_data(session_data)
                    self.redis_client.setex(key, ttl, encrypted_data)
                    return True
                except EncryptionError:
                    # Fallback sin encriptar
                    self.redis_client.setex(key, ttl, json.dumps(session_data, default=str))
                    return True
        
        return False
    
    async def invalidate_session(self, session_id: str) -> bool:
        """Invalida sesión activa"""
        key = f"active_session:{session_id}"
        
        # Obtener datos antes de eliminar
        session_data = await self.get_active_session(session_id)
        if session_data:
            # Remover de índice de usuario
            user_sessions_key = f"user_sessions:{session_data['user_type']}:{session_data['user_id']}"
            self.redis_client.srem(user_sessions_key, session_id)
        
        return bool(self.redis_client.delete(key))
    
    async def get_user_active_sessions(self, user_id: int, user_type: str) -> List[Dict[str, Any]]:
        """Obtiene todas las sesiones activas de un usuario"""
        user_sessions_key = f"user_sessions:{user_type}:{user_id}"
        session_ids = self.redis_client.smembers(user_sessions_key)
        
        sessions = []
        for session_id in session_ids:
            session_data = await self.get_active_session(session_id)
            if session_data:
                # 🔒 ENMASCARAR datos sensibles para logs
                masked_data = self.crypto.mask_sensitive_data(session_data)
                masked_data['session_id'] = session_id
                sessions.append(masked_data)
            else:
                # Limpiar sesión inválida del índice
                self.redis_client.srem(user_sessions_key, session_id)
        
        return sessions
    
    async def invalidate_all_user_sessions(self, user_id: int, user_type: str, except_session: Optional[str] = None) -> int:
        """Invalida todas las sesiones de un usuario"""
        sessions = await self.get_user_active_sessions(user_id, user_type)
        invalidated_count = 0
        
        for session in sessions:
            session_id = session['session_id']
            if session_id != except_session:
                if await self.invalidate_session(session_id):
                    invalidated_count += 1
        
        return invalidated_count
    
    # ===================================
    # 2FA TEMPORAL (ENCRIPTADO)
    # ===================================
    
    async def store_totp_attempt(self, user_id: int, user_type: str, code: str) -> None:
        """Guarda intento de código TOTP ENCRIPTADO"""
        key = f"totp_attempts:{user_type}:{user_id}"
        
        attempt_data = {
            'code': code,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            # 🔐 ENCRIPTAR datos del intento TOTP
            encrypted_attempt = self.crypto.encrypt_session_data(attempt_data)
            
            # Usar sorted set para TTL automático
            self.redis_client.zadd(key, {encrypted_attempt: datetime.utcnow().timestamp()})
            
        except EncryptionError:
            # Fallback sin encriptar
            self.redis_client.zadd(key, {json.dumps(attempt_data): datetime.utcnow().timestamp()})
        
        # Limpiar códigos antiguos (más de 5 minutos)
        cutoff = datetime.utcnow() - timedelta(minutes=5)
        self.redis_client.zremrangebyscore(key, 0, cutoff.timestamp())
        
        # Expirar clave después de 10 minutos
        self.redis_client.expire(key, 10 * 60)
    
    async def is_totp_code_used(self, user_id: int, user_type: str, code: str) -> bool:
        """Verifica si código TOTP ya fue usado recientemente"""
        key = f"totp_attempts:{user_type}:{user_id}"
        
        # Buscar código en intentos recientes
        encrypted_attempts = self.redis_client.zrange(key, 0, -1)
        for encrypted_attempt in encrypted_attempts:
            try:
                # 🔓 DESENCRIPTAR intento
                attempt_data = self.crypto.decrypt_session_data(encrypted_attempt)
                if attempt_data and attempt_data.get('code') == code:
                    return True
            except Exception:
                # Intentar como JSON sin encriptar (fallback)
                try:
                    attempt_data = json.loads(encrypted_attempt)
                    if attempt_data.get('code') == code:
                        return True
                except Exception:
                    continue
        
        return False
    
    # ===================================
    # UTILITIES
    # ===================================
    
    async def clear_user_temp_data(self, identifier: str) -> None:
        """Limpia todos los datos temporales de un usuario después de login exitoso"""
        patterns = [
            f"failed_attempts:{identifier}",
            f"rate_limit:user:{identifier}",
            f"blocked:user:{identifier}"
        ]
        
        for pattern in patterns:
            self.redis_client.delete(pattern)
    
    async def get_security_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de seguridad en tiempo real"""
        # Contar bloqueos activos
        blocked_ips = len(self.redis_client.keys("blocked:ip:*"))
        blocked_users = len(self.redis_client.keys("blocked:user:*"))
        
        # Contar sesiones activas
        active_sessions = len(self.redis_client.keys("active_session:*"))
        
        return {
            'blocked_ips': blocked_ips,
            'blocked_users': blocked_users,
            'active_sessions': active_sessions,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def migrate_unencrypted_sessions(self) -> Dict[str, Any]:
        """
        Utilidad para migrar sesiones no encriptadas a encriptadas
        (Para ejecutar una sola vez durante el despliegue)
        """
        migrated = 0
        failed = 0
        
        session_keys = self.redis_client.keys("active_session:*")
        
        for key in session_keys:
            try:
                data = self.redis_client.get(key)
                if data:
                    # Intentar deserializar como JSON (no encriptado)
                    try:
                        session_data = json.loads(data)
                        
                        # Si es JSON válido, re-encriptar
                        encrypted_data = self.crypto.encrypt_session_data(session_data)
                        
                        # Mantener TTL original
                        ttl = self.redis_client.ttl(key)
                        if ttl > 0:
                            self.redis_client.setex(key, ttl, encrypted_data)
                            migrated += 1
                        
                    except json.JSONDecodeError:
                        # Ya está encriptado o corrupto
                        continue
                        
            except Exception:
                failed += 1
                continue
        
        return {
            "migrated_sessions": migrated,
            "failed_migrations": failed,
            "total_processed": len(session_keys)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica estado de salud del servicio Redis"""
        health = {
            "redis_connected": False,
            "encryption_working": False,
            "services_operational": False,
            "errors": []
        }
        
        try:
            # Test conexión Redis
            self.redis_client.ping()
            health["redis_connected"] = True
            
            # Test encriptación
            test_data = {"test": "encryption_check"}
            encrypted = self.crypto.encrypt_session_data(test_data)
            decrypted = self.crypto.decrypt_session_data(encrypted)
            
            if decrypted == test_data:
                health["encryption_working"] = True
            
            # Test operaciones básicas
            test_key = "health_check_test"
            self.redis_client.set(test_key, "test", ex=60)
            if self.redis_client.get(test_key) == "test":
                self.redis_client.delete(test_key)
                health["services_operational"] = True
            
        except Exception as e:
            health["errors"].append(str(e))
        
        return health


# Instancia singleton
redis_auth_service = RedisAuthService()