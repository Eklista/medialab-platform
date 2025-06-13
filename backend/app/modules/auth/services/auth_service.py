# backend/app/modules/auth/services/auth_service.py
"""
Auth Service Híbrido - Combina MySQL y Redis para máximo rendimiento
"""
import uuid
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.modules.auth.models import AuthSession, LoginAttempt
from app.modules.auth.services.redis_auth_service import redis_auth_service, LoginAttemptData
from app.modules.users.models import InternalUser, InstitutionalUser
from app.modules.users.repositories.user_repository import InternalUserRepository, InstitutionalUserRepository


class AuthService:
    """
    Servicio de autenticación híbrido MySQL + Redis
    
    STRATEGY:
    - Redis: Datos temporales (rate limiting, intentos fallidos, sesiones activas)
    - MySQL: Datos permanentes (logins exitosos, eventos de seguridad, auditoría)
    """
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.internal_user_repo = InternalUserRepository()
        self.institutional_user_repo = InstitutionalUserRepository()
    
    # ===================================
    # LOGIN FLOW HÍBRIDO
    # ===================================
    
    async def authenticate_user(
        self,
        identifier: str,  # username or email
        password: str,
        request_info: Dict[str, Any],  # IP, user_agent, etc.
        db: Session
    ) -> Dict[str, Any]:
        """
        Flow de autenticación completo híbrido
        
        Returns:
            {
                'success': bool,
                'user': User | None,
                'session': dict | None,
                'reason': str,
                'requires_2fa': bool,
                'blocked_until': datetime | None
            }
        """
        
        # 1. Rate limiting check (Redis)
        ip_limit = await redis_auth_service.check_rate_limit(request_info['ip_address'], 'ip')
        user_limit = await redis_auth_service.check_rate_limit(identifier, 'user')
        
        if not ip_limit.is_allowed:
            return {
                'success': False,
                'reason': 'ip_rate_limited',
                'blocked_until': ip_limit.blocked_until,
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        if not user_limit.is_allowed:
            return {
                'success': False,
                'reason': 'user_rate_limited', 
                'blocked_until': user_limit.blocked_until,
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        # 2. Buscar usuario
        user, user_type = await self._find_user_by_identifier(identifier, db)
        
        if not user:
            # Registrar intento fallido en Redis
            await self._record_failed_attempt(
                identifier, request_info, 'user_not_found', db
            )
            return {
                'success': False,
                'reason': 'invalid_credentials',
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        # 3. Verificar password
        if not user.password_hash or not self.pwd_context.verify(password, user.password_hash):
            await self._record_failed_attempt(
                identifier, request_info, 'invalid_password', db, user.id, user_type
            )
            return {
                'success': False,
                'reason': 'invalid_credentials',
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        # 4. Verificar estado de cuenta
        if not user.is_active:
            await self._record_failed_attempt(
                identifier, request_info, 'account_inactive', db, user.id, user_type
            )
            return {
                'success': False,
                'reason': 'account_inactive',
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        if user.account_locked:
            await self._record_failed_attempt(
                identifier, request_info, 'account_locked', db, user.id, user_type
            )
            return {
                'success': False,
                'reason': 'account_locked',
                'user': None,
                'session': None,
                'requires_2fa': False
            }
        
        # 5. Análisis de riesgo
        risk_analysis = await self._analyze_login_risk(user, user_type, request_info, db)
        
        # 6. Verificar si requiere 2FA
        requires_2fa = await self._should_require_2fa(user, user_type, risk_analysis, db)
        
        if requires_2fa:
            # Crear sesión temporal pendiente de 2FA
            temp_session = await self._create_temp_2fa_session(user, user_type, request_info)
            return {
                'success': False,
                'reason': 'requires_2fa',
                'user': user,
                'session': temp_session,
                'requires_2fa': True
            }
        
        # 7. Login exitoso - crear sesión completa
        session_data = await self._create_full_session(user, user_type, request_info, db)
        
        # 8. Registrar login exitoso (MySQL para auditoría)
        await self._record_successful_login(user, user_type, request_info, session_data, risk_analysis, db)
        
        # 9. Limpiar datos temporales de Redis
        await redis_auth_service.clear_user_temp_data(identifier)
        
        # 10. Actualizar estadísticas del usuario
        await self._update_user_login_stats(user, user_type, db)
        
        return {
            'success': True,
            'reason': 'authenticated',
            'user': user,
            'session': session_data,
            'requires_2fa': False
        }
    
    async def complete_2fa_login(
        self,
        temp_session_id: str,
        totp_code: str,
        request_info: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        Completa login después de validar 2FA
        """
        
        # 1. Validar sesión temporal
        temp_session = await redis_auth_service.get_active_session(temp_session_id)
        if not temp_session or temp_session.get('type') != 'temp_2fa':
            return {
                'success': False,
                'reason': 'invalid_temp_session'
            }
        
        # 2. Verificar que no haya expirado (10 minutos)
        created_at = datetime.fromisoformat(temp_session['created_at'])
        if datetime.utcnow() - created_at > timedelta(minutes=10):
            await redis_auth_service.invalidate_session(temp_session_id)
            return {
                'success': False,
                'reason': 'temp_session_expired'
            }
        
        # 3. Obtener usuario
        user, user_type = await self._find_user_by_id(
            temp_session['user_id'], 
            temp_session['user_type'], 
            db
        )
        
        if not user:
            return {
                'success': False,
                'reason': 'user_not_found'
            }
        
        # 4. Validar código TOTP
        totp_valid = await self._validate_totp_code(user, user_type, totp_code, db)
        if not totp_valid:
            return {
                'success': False,
                'reason': 'invalid_2fa_code'
            }
        
        # 5. Invalidar sesión temporal
        await redis_auth_service.invalidate_session(temp_session_id)
        
        # 6. Crear sesión completa
        session_data = await self._create_full_session(user, user_type, request_info, db)
        
        # 7. Registrar login exitoso con 2FA
        risk_analysis = {'risk_score': temp_session.get('risk_score', 0)}
        await self._record_successful_login(
            user, user_type, request_info, session_data, risk_analysis, db, '2fa'
        )
        
        return {
            'success': True,
            'reason': 'authenticated_2fa',
            'user': user,
            'session': session_data
        }
    
    # ===================================
    # SESSION MANAGEMENT
    # ===================================
    
    async def validate_session(self, session_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """
        Valida sesión activa (híbrido Redis + MySQL)
        """
        
        # 1. Verificar en Redis (rápido)
        session_data = await redis_auth_service.get_active_session(session_id)
        
        if not session_data:
            # 2. Fallback a MySQL si no está en Redis
            auth_session = db.query(AuthSession).filter(
                AuthSession.session_id == session_id,
                AuthSession.is_active == True
            ).first()
            
            if not auth_session or auth_session.is_expired:
                return None
            
            # 3. Restaurar en Redis
            session_data = {
                'user_id': auth_session.user_id,
                'user_type': auth_session.user_type,
                'session_id': session_id,
                'ip_address': auth_session.ip_address,
                'device_name': auth_session.device_name,
                'expires_at': auth_session.expires_at.isoformat(),
                'is_2fa_verified': auth_session.is_2fa_verified
            }
            
            # Calcular TTL restante
            remaining_time = auth_session.expires_at - datetime.utcnow()
            if remaining_time.total_seconds() > 0:
                await redis_auth_service.store_active_session(
                    session_id, 
                    session_data, 
                    ttl_hours=remaining_time.total_seconds() / 3600
                )
        
        # 4. Actualizar última actividad
        await redis_auth_service.update_session_activity(session_id)
        
        # 5. Verificar expiración
        expires_at = datetime.fromisoformat(session_data['expires_at'])
        if datetime.utcnow() > expires_at:
            await self.logout_session(session_id, "expired", db)
            return None
        
        return session_data
    
    async def logout_session(self, session_id: str, reason: str = "manual", db: Session = None) -> bool:
        """
        Logout de sesión específica
        """
        
        # 1. Invalidar en Redis
        redis_invalidated = await redis_auth_service.invalidate_session(session_id)
        
        # 2. Actualizar en MySQL para auditoría
        if db:
            auth_session = db.query(AuthSession).filter(
                AuthSession.session_id == session_id
            ).first()
            
            if auth_session:
                auth_session.terminate_session(reason)
                db.commit()
        
        return redis_invalidated
    
    async def logout_all_user_sessions(
        self, 
        user_id: int, 
        user_type: str, 
        except_session: Optional[str] = None,
        db: Session = None
    ) -> int:
        """
        Logout de todas las sesiones de un usuario
        """
        
        # 1. Invalidar en Redis
        redis_count = await redis_auth_service.invalidate_all_user_sessions(
            user_id, user_type, except_session
        )
        
        # 2. Actualizar en MySQL
        if db:
            query = db.query(AuthSession).filter(
                AuthSession.user_id == user_id,
                AuthSession.user_type == user_type,
                AuthSession.is_active == True
            )
            
            if except_session:
                query = query.filter(AuthSession.session_id != except_session)
            
            mysql_count = query.update({
                'is_active': False,
                'logout_reason': 'logout_all',
                'logout_at': datetime.utcnow()
            })
            
            db.commit()
            return max(redis_count, mysql_count)
        
        return redis_count
    
    # ===================================
    # HELPER METHODS
    # ===================================
    
    async def _find_user_by_identifier(self, identifier: str, db: Session) -> Tuple[Optional[Any], Optional[str]]:
        """Busca usuario por email o username en ambas tablas"""
        
        # Buscar en internal users
        internal_user = None
        if '@' in identifier:
            internal_user = self.internal_user_repo.get_by_email(db, identifier)
        else:
            internal_user = self.internal_user_repo.get_by_username(db, identifier)
        
        if internal_user:
            return internal_user, 'internal_user'
        
        # Buscar en institutional users
        institutional_user = None
        if '@' in identifier:
            institutional_user = self.institutional_user_repo.get_by_email(db, identifier)
        else:
            institutional_user = self.institutional_user_repo.get_by_username(db, identifier)
        
        if institutional_user:
            return institutional_user, 'institutional_user'
        
        return None, None
    
    async def _find_user_by_id(self, user_id: int, user_type: str, db: Session) -> Tuple[Optional[Any], Optional[str]]:
        """Busca usuario por ID y tipo"""
        
        if user_type == 'internal_user':
            user = self.internal_user_repo.get_by_id(db, user_id)
        elif user_type == 'institutional_user':
            user = self.institutional_user_repo.get_by_id(db, user_id)
        else:
            return None, None
        
        return user, user_type if user else None
    
    async def _record_failed_attempt(
        self,
        identifier: str,
        request_info: Dict[str, Any],
        failure_reason: str,
        db: Session,
        user_id: Optional[int] = None,
        user_type: Optional[str] = None
    ) -> None:
        """
        Registra intento fallido (Redis + MySQL según riesgo)
        """
        
        # Calcular risk score
        risk_score = await self._calculate_risk_score(request_info, user_id, user_type, db)
        
        # Crear datos del intento
        attempt_data = LoginAttemptData(
            identifier=identifier,
            ip_address=request_info['ip_address'],
            timestamp=datetime.utcnow(),
            failure_reason=failure_reason,
            user_agent=request_info.get('user_agent', ''),
            risk_score=risk_score
        )
        
        # 1. Siempre guardar en Redis (temporal)
        await redis_auth_service.store_failed_attempt(attempt_data)
        
        # 2. Actualizar rate limiting
        await redis_auth_service.record_failed_attempt(request_info['ip_address'], 'ip')
        await redis_auth_service.record_failed_attempt(identifier, 'user')
        
        # 3. Guardar en MySQL solo si es importante
        should_save_mysql = (
            risk_score >= 70 or  # Alto riesgo
            failure_reason in ['account_locked', 'account_inactive'] or  # Eventos de seguridad
            user_id is not None  # Tenemos usuario válido
        )
        
        if should_save_mysql:
            login_attempt = LoginAttempt(
                identifier=identifier,
                identifier_type='email' if '@' in identifier else 'username',
                ip_address=request_info['ip_address'],
                user_agent=request_info.get('user_agent'),
                device_fingerprint=request_info.get('device_fingerprint'),
                attempt_type='password',
                is_successful=False,
                failure_reason=failure_reason,
                user_id=user_id,
                user_type=user_type,
                risk_score=risk_score,
                is_suspicious=risk_score >= 70,
                is_security_event=failure_reason in ['account_locked', 'account_inactive'],
                response_time_ms=request_info.get('response_time_ms')
            )
            
            db.add(login_attempt)
            db.commit()
    
    async def _record_successful_login(
        self,
        user: Any,
        user_type: str,
        request_info: Dict[str, Any],
        session_data: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        db: Session,
        auth_method: str = 'password'
    ) -> None:
        """
        Registra login exitoso (siempre en MySQL para auditoría)
        """
        
        login_attempt = LoginAttempt(
            identifier=user.email,
            identifier_type='email',
            ip_address=request_info['ip_address'],
            user_agent=request_info.get('user_agent'),
            device_fingerprint=request_info.get('device_fingerprint'),
            attempt_type=auth_method,
            is_successful=True,
            user_id=user.id,
            user_type=user_type,
            country=request_info.get('country'),
            city=request_info.get('city'),
            latitude=request_info.get('latitude'),
            longitude=request_info.get('longitude'),
            risk_score=risk_analysis.get('risk_score', 0),
            risk_factors=risk_analysis.get('risk_factors_json'),
            is_suspicious=risk_analysis.get('risk_score', 0) >= 70,
            is_location_change=risk_analysis.get('is_location_change', False),
            is_new_device=risk_analysis.get('is_new_device', False),
            is_security_event=False,
            session_id=session_data['session_id'],
            response_time_ms=request_info.get('response_time_ms')
        )
        
        db.add(login_attempt)
        db.commit()
    
    async def _analyze_login_risk(
        self, 
        user: Any, 
        user_type: str, 
        request_info: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """
        Análisis de riesgo del login
        """
        risk_score = 0
        risk_factors = []
        
        # 1. Verificar intentos fallidos recientes
        recent_failures = await redis_auth_service.get_recent_failed_attempts(user.email, 5)
        if len(recent_failures) >= 3:
            risk_score += 30
            risk_factors.append('recent_failures')
        
        # 2. Verificar nueva ubicación
        is_location_change = await self._is_new_location(user, user_type, request_info, db)
        if is_location_change:
            risk_score += 25
            risk_factors.append('new_location')
        
        # 3. Verificar nuevo dispositivo
        is_new_device = await self._is_new_device(user, user_type, request_info, db)
        if is_new_device:
            risk_score += 20
            risk_factors.append('new_device')
        
        # 4. Verificar hora inusual
        if await self._is_unusual_time(user, user_type, db):
            risk_score += 15
            risk_factors.append('unusual_time')
        
        # 5. Verificar IP sospechosa
        if await self._is_suspicious_ip(request_info['ip_address']):
            risk_score += 35
            risk_factors.append('suspicious_ip')
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'risk_factors_json': str(risk_factors),
            'is_location_change': is_location_change,
            'is_new_device': is_new_device
        }
    
    async def _calculate_risk_score(
        self, 
        request_info: Dict[str, Any],
        user_id: Optional[int],
        user_type: Optional[str],
        db: Session
    ) -> int:
        """Calcula risk score simplificado para intentos fallidos"""
        risk_score = 0
        
        # IP sospechosa
        if await self._is_suspicious_ip(request_info['ip_address']):
            risk_score += 40
        
        # User agent sospechoso
        user_agent = request_info.get('user_agent', '')
        if not user_agent or 'bot' in user_agent.lower():
            risk_score += 30
        
        # Tiempo de respuesta muy rápido (posible bot)
        response_time = request_info.get('response_time_ms', 1000)
        if response_time < 100:
            risk_score += 25
        
        return min(risk_score, 100)
    
    async def _should_require_2fa(
        self, 
        user: Any, 
        user_type: str, 
        risk_analysis: Dict[str, Any], 
        db: Session
    ) -> bool:
        """
        Determina si se requiere 2FA
        """
        
        # 1. Usuario tiene 2FA configurado?
        has_2fa = await self._user_has_2fa_devices(user, user_type, db)
        if not has_2fa:
            return False
        
        # 2. Alto riesgo siempre requiere 2FA
        if risk_analysis['risk_score'] >= 60:
            return True
        
        # 3. Nueva ubicación o dispositivo
        if risk_analysis['is_location_change'] or risk_analysis['is_new_device']:
            return True
        
        # 4. Políticas por tipo de usuario
        if user_type == 'internal_user' and user.can_access_dashboard:
            # Staff interno siempre 2FA
            return True
        
        return False
    
    async def _create_temp_2fa_session(
        self, 
        user: Any, 
        user_type: str, 
        request_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crea sesión temporal para 2FA
        """
        temp_session_id = f"temp_2fa_{secrets.token_urlsafe(32)}"
        
        session_data = {
            'type': 'temp_2fa',
            'user_id': user.id,
            'user_type': user_type,
            'ip_address': request_info['ip_address'],
            'user_agent': request_info.get('user_agent'),
            'risk_score': request_info.get('risk_score', 0)
        }
        
        # Guardar en Redis con TTL de 10 minutos
        await redis_auth_service.store_active_session(
            temp_session_id, session_data, ttl_hours=10/60
        )
        
        return {
            'temp_session_id': temp_session_id,
            'expires_in': 600  # 10 minutos
        }
    
    async def _create_full_session(
        self, 
        user: Any, 
        user_type: str, 
        request_info: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """
        Crea sesión completa después de autenticación exitosa
        """
        
        # Generar IDs únicos
        session_id = secrets.token_urlsafe(32)
        refresh_token_id = secrets.token_urlsafe(32)
        
        # Datos de sesión
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # 1. Guardar en MySQL (auditoría permanente)
        auth_session = AuthSession(
            user_id=user.id,
            user_type=user_type,
            session_id=session_id,
            refresh_token_id=refresh_token_id,
            user_agent=request_info.get('user_agent'),
            ip_address=request_info['ip_address'],
            device_fingerprint=request_info.get('device_fingerprint'),
            device_name=request_info.get('device_name'),
            location=request_info.get('location'),
            expires_at=expires_at,
            is_2fa_verified=True,  # Ya pasó 2FA si era necesario
            login_method='password',
            session_type=request_info.get('session_type', 'web')
        )
        
        db.add(auth_session)
        db.commit()
        
        # 2. Guardar en Redis (acceso rápido)
        session_data = {
            'user_id': user.id,
            'user_type': user_type,
            'session_id': session_id,
            'refresh_token_id': refresh_token_id,
            'ip_address': request_info['ip_address'],
            'device_name': request_info.get('device_name'),
            'expires_at': expires_at.isoformat(),
            'is_2fa_verified': True
        }
        
        await redis_auth_service.store_active_session(session_id, session_data, 24)
        
        return {
            'session_id': session_id,
            'refresh_token_id': refresh_token_id,
            'expires_at': expires_at.isoformat(),
            'user_id': user.id,
            'user_type': user_type
        }
    
    async def _update_user_login_stats(self, user: Any, user_type: str, db: Session) -> None:
        """Actualiza estadísticas de login del usuario"""
        user.last_login = datetime.utcnow()
        user.login_count += 1
        user.failed_login_attempts = 0  # Reset counter
        
        if user_type == 'internal_user':
            user.last_activity = datetime.utcnow()
        
        db.commit()
    
    # ===================================
    # RISK ANALYSIS HELPERS
    # ===================================
    
    async def _is_new_location(self, user: Any, user_type: str, request_info: Dict[str, Any], db: Session) -> bool:
        """Verifica si es una nueva ubicación geográfica"""
        # Buscar logins recientes desde la misma ubicación
        recent_login = db.query(LoginAttempt).filter(
            LoginAttempt.user_id == user.id,
            LoginAttempt.user_type == user_type,
            LoginAttempt.is_successful == True,
            LoginAttempt.country == request_info.get('country'),
            LoginAttempt.created_at >= datetime.utcnow() - timedelta(days=30)
        ).first()
        
        return recent_login is None
    
    async def _is_new_device(self, user: Any, user_type: str, request_info: Dict[str, Any], db: Session) -> bool:
        """Verifica si es un nuevo dispositivo"""
        device_fingerprint = request_info.get('device_fingerprint')
        if not device_fingerprint:
            return True
        
        # Buscar sesiones recientes con mismo fingerprint
        recent_session = db.query(AuthSession).filter(
            AuthSession.user_id == user.id,
            AuthSession.user_type == user_type,
            AuthSession.device_fingerprint == device_fingerprint,
            AuthSession.created_at >= datetime.utcnow() - timedelta(days=30)
        ).first()
        
        return recent_session is None
    
    async def _is_unusual_time(self, user: Any, user_type: str, db: Session) -> bool:
        """Verifica si es una hora inusual para el usuario"""
        # Obtener hora actual del usuario (considerando timezone)
        current_hour = datetime.utcnow().hour
        
        # Buscar patrón de logins del usuario (últimos 30 días)
        recent_logins = db.query(LoginAttempt).filter(
            LoginAttempt.user_id == user.id,
            LoginAttempt.user_type == user_type,
            LoginAttempt.is_successful == True,
            LoginAttempt.created_at >= datetime.utcnow() - timedelta(days=30)
        ).all()
        
        if len(recent_logins) < 5:
            return False  # Insuficientes datos
        
        # Calcular horas usuales
        usual_hours = [login.created_at.hour for login in recent_logins]
        
        # Si la hora actual está fuera del rango usual (±3 horas)
        min_hour = min(usual_hours) - 3
        max_hour = max(usual_hours) + 3
        
        return not (min_hour <= current_hour <= max_hour)
    
    async def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Verifica si la IP es sospechosa"""
        # Lista simple de rangos sospechosos (en producción usar servicios externos)
        suspicious_patterns = [
            '10.0.0.',  # Ejemplo
            '127.0.0.',
            # Agregar más patrones según necesidad
        ]
        
        for pattern in suspicious_patterns:
            if ip_address.startswith(pattern):
                return True
        
        return False
    
    async def _user_has_2fa_devices(self, user: Any, user_type: str, db: Session) -> bool:
        """Verifica si el usuario tiene dispositivos 2FA activos"""  # ✅ BIEN INDENTADO
        from .totp_service import TotpService
        
        totp_service = TotpService()
        devices = totp_service.get_user_2fa_devices(user.id, user_type, db)
        
        return len([d for d in devices if d["is_verified"]]) > 0
    
    async def _validate_totp_code(self, user: Any, user_type: str, code: str, db: Session) -> bool:
        """Valida código TOTP usando el servicio completo"""
        from .totp_service import TotpService
        
        totp_service = TotpService()
        result = totp_service.validate_totp_code(user.id, user_type, code, db)
        
        return result["success"]


# Instancia singleton
auth_service = AuthService()