# backend/app/modules/auth/controllers/auth_controller.py
"""
Auth Controller - Endpoints de autenticación con arquitectura híbrida
"""
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from app.core.database import get_db
from app.modules.auth.services.auth_service import auth_service
from app.modules.auth.services.redis_auth_service import redis_auth_service
from app.modules.auth.schemas.auth_schemas import (
    LoginRequest, LoginResponse, TwoFactorRequest, TwoFactorResponse,
    SessionResponse, LogoutResponse, SecurityStatsResponse
)


class AuthController:
    """Controller para operaciones de autenticación"""
    
    def __init__(self):
        self.auth_service = auth_service
        self.redis_service = redis_auth_service
    
    # ===================================
    # AUTHENTICATION ENDPOINTS
    # ===================================
    
    async def login(self, login_data: LoginRequest, request: Request, db: Session) -> LoginResponse:
        """
        Login endpoint con flow híbrido completo
        """
        # Extraer información de la request
        request_info = await self._extract_request_info(request)
        
        # Agregar tiempo de inicio para medir response time
        start_time = datetime.utcnow()
        
        try:
            # Autenticar usuario
            auth_result = await self.auth_service.authenticate_user(
                identifier=login_data.identifier,
                password=login_data.password,
                request_info=request_info,
                db=db
            )
            
            # Calcular response time
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            if auth_result['success']:
                return LoginResponse(
                    success=True,
                    message="Login successful",
                    user_id=auth_result['user'].id,
                    user_type=auth_result['session']['user_type'],
                    session_id=auth_result['session']['session_id'],
                    expires_at=auth_result['session']['expires_at'],
                    requires_2fa=False,
                    response_time_ms=int(response_time)
                )
            
            elif auth_result['requires_2fa']:
                return LoginResponse(
                    success=False,
                    message="Two-factor authentication required",
                    temp_session_id=auth_result['session']['temp_session_id'],
                    requires_2fa=True,
                    expires_in=auth_result['session']['expires_in'],
                    response_time_ms=int(response_time)
                )
            
            else:
                # Login fallido
                error_messages = {
                    'invalid_credentials': 'Invalid username or password',
                    'account_inactive': 'Account is not active',
                    'account_locked': 'Account is locked',
                    'ip_rate_limited': 'Too many attempts from this IP address',
                    'user_rate_limited': 'Too many failed attempts for this account'
                }
                
                message = error_messages.get(auth_result['reason'], 'Login failed')
                
                if auth_result.get('blocked_until'):
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail={
                            'message': message,
                            'blocked_until': auth_result['blocked_until'].isoformat(),
                            'response_time_ms': int(response_time)
                        }
                    )
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        'message': message,
                        'response_time_ms': int(response_time)
                    }
                )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Authentication error: {str(e)}"
            )
    
    async def verify_2fa(self, twofa_data: TwoFactorRequest, request: Request, db: Session) -> TwoFactorResponse:
        """
        Verificación de 2FA y completar login
        """
        request_info = await self._extract_request_info(request)
        
        try:
            auth_result = await self.auth_service.complete_2fa_login(
                temp_session_id=twofa_data.temp_session_id,
                totp_code=twofa_data.code,
                request_info=request_info,
                db=db
            )
            
            if auth_result['success']:
                return TwoFactorResponse(
                    success=True,
                    message="Two-factor authentication successful",
                    user_id=auth_result['user'].id,
                    user_type=auth_result['session']['user_type'],
                    session_id=auth_result['session']['session_id'],
                    expires_at=auth_result['session']['expires_at']
                )
            else:
                error_messages = {
                    'invalid_temp_session': 'Invalid or expired temporary session',
                    'temp_session_expired': 'Temporary session has expired',
                    'user_not_found': 'User not found',
                    'invalid_2fa_code': 'Invalid two-factor authentication code'
                }
                
                message = error_messages.get(auth_result['reason'], '2FA verification failed')
                
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={'message': message}
                )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"2FA verification error: {str(e)}"
            )
    
    async def logout(self, session_id: str, db: Session) -> LogoutResponse:
        """
        Logout de sesión específica
        """
        try:
            success = await self.auth_service.logout_session(session_id, "manual", db)
            
            if success:
                return LogoutResponse(
                    success=True,
                    message="Logout successful"
                )
            else:
                return LogoutResponse(
                    success=False,
                    message="Session not found or already expired"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout error: {str(e)}"
            )
    
    async def logout_all(self, user_id: int, user_type: str, current_session: Optional[str], db: Session) -> LogoutResponse:
        """
        Logout de todas las sesiones del usuario
        """
        try:
            count = await self.auth_service.logout_all_user_sessions(
                user_id=user_id,
                user_type=user_type,
                except_session=current_session,
                db=db
            )
            
            return LogoutResponse(
                success=True,
                message=f"Logged out from {count} sessions"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Logout all error: {str(e)}"
            )
    
    # ===================================
    # SESSION MANAGEMENT
    # ===================================
    
    async def validate_session(self, session_id: str, db: Session) -> SessionResponse:
        """
        Validar sesión activa
        """
        try:
            session_data = await self.auth_service.validate_session(session_id, db)
            
            if session_data:
                return SessionResponse(
                    valid=True,
                    user_id=session_data['user_id'],
                    user_type=session_data['user_type'],
                    expires_at=session_data['expires_at'],
                    is_2fa_verified=session_data.get('is_2fa_verified', False)
                )
            else:
                return SessionResponse(
                    valid=False,
                    message="Session not found or expired"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Session validation error: {str(e)}"
            )
    
    async def get_active_sessions(self, user_id: int, user_type: str, db: Session) -> Dict[str, Any]:
        """
        Obtener sesiones activas del usuario
        """
        try:
            # Obtener de Redis (rápido)
            redis_sessions = await self.redis_service.get_user_active_sessions(user_id, user_type)
            
            # Si no hay en Redis, buscar en MySQL
            if not redis_sessions:
                from app.modules.auth.models import AuthSession
                mysql_sessions = db.query(AuthSession).filter(
                    AuthSession.user_id == user_id,
                    AuthSession.user_type == user_type,
                    AuthSession.is_active == True
                ).all()
                
                # Convertir a formato estándar
                redis_sessions = []
                for session in mysql_sessions:
                    if not session.is_expired:
                        session_data = {
                            'session_id': session.session_id,
                            'ip_address': session.ip_address,
                            'device_name': session.device_name,
                            'location': session.location,
                            'created_at': session.created_at.isoformat(),
                            'last_activity': session.last_activity.isoformat(),
                            'expires_at': session.expires_at.isoformat()
                        }
                        redis_sessions.append(session_data)
            
            return {
                'sessions': redis_sessions,
                'total_count': len(redis_sessions)
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving sessions: {str(e)}"
            )
    
    async def extend_session(self, session_id: str, hours: int, db: Session) -> Dict[str, Any]:
        """
        Extender duración de sesión
        """
        try:
            # Validar sesión actual
            session_data = await self.auth_service.validate_session(session_id, db)
            if not session_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Session not found or expired"
                )
            
            # Extender en Redis
            await self.redis_service.store_active_session(
                session_id, session_data, ttl_hours=hours
            )
            
            # Actualizar en MySQL
            from app.modules.auth.models import AuthSession
            auth_session = db.query(AuthSession).filter(
                AuthSession.session_id == session_id
            ).first()
            
            if auth_session:
                auth_session.extend_session(hours)
                db.commit()
            
            return {
                'success': True,
                'message': f"Session extended by {hours} hours",
                'new_expires_at': session_data['expires_at']
            }
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error extending session: {str(e)}"
            )
    
    # ===================================
    # SECURITY MONITORING
    # ===================================
    
    async def get_security_stats(self, db: Session) -> SecurityStatsResponse:
        """
        Obtener estadísticas de seguridad en tiempo real
        """
        try:
            # Stats de Redis (tiempo real)
            redis_stats = await self.redis_service.get_security_stats()
            
            # Stats de MySQL (histórico)
            from app.modules.auth.models import LoginAttempt, AuthSession
            from sqlalchemy import func
            from datetime import timedelta
            
            # Últimas 24 horas
            last_24h = datetime.utcnow() - timedelta(hours=24)
            
            # Login attempts stats
            total_attempts_24h = db.query(LoginAttempt).filter(
                LoginAttempt.created_at >= last_24h
            ).count()
            
            successful_attempts_24h = db.query(LoginAttempt).filter(
                LoginAttempt.created_at >= last_24h,
                LoginAttempt.is_successful == True
            ).count()
            
            suspicious_attempts_24h = db.query(LoginAttempt).filter(
                LoginAttempt.created_at >= last_24h,
                LoginAttempt.is_suspicious == True
            ).count()
            
            # Sessions stats
            active_sessions_mysql = db.query(AuthSession).filter(
                AuthSession.is_active == True,
                AuthSession.expires_at > datetime.utcnow()
            ).count()
            
            # Risk analysis
            high_risk_attempts = db.query(LoginAttempt).filter(
                LoginAttempt.created_at >= last_24h,
                LoginAttempt.risk_score >= 70
            ).count()
            
            return SecurityStatsResponse(
                # Redis stats (tiempo real)
                blocked_ips=redis_stats['blocked_ips'],
                blocked_users=redis_stats['blocked_users'],
                active_sessions_redis=redis_stats['active_sessions'],
                
                # MySQL stats (histórico)
                total_attempts_24h=total_attempts_24h,
                successful_attempts_24h=successful_attempts_24h,
                suspicious_attempts_24h=suspicious_attempts_24h,
                high_risk_attempts_24h=high_risk_attempts,
                active_sessions_mysql=active_sessions_mysql,
                
                # Calculated metrics
                success_rate_24h=round((successful_attempts_24h / total_attempts_24h * 100) if total_attempts_24h > 0 else 0, 2),
                suspicious_rate_24h=round((suspicious_attempts_24h / total_attempts_24h * 100) if total_attempts_24h > 0 else 0, 2),
                
                timestamp=datetime.utcnow().isoformat()
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving security stats: {str(e)}"
            )
    
    async def get_user_login_history(self, user_id: int, user_type: str, db: Session, limit: int = 20) -> Dict[str, Any]:
        """
        Obtener historial de logins del usuario
        """
        try:
            from app.modules.auth.models import LoginAttempt
            
            # Obtener historial reciente de MySQL
            login_history = db.query(LoginAttempt).filter(
                LoginAttempt.user_id == user_id,
                LoginAttempt.user_type == user_type
            ).order_by(LoginAttempt.created_at.desc()).limit(limit).all()
            
            # Obtener intentos fallidos recientes de Redis
            redis_failures = await self.redis_service.get_recent_failed_attempts(
                f"{user_id}_{user_type}", 10
            )
            
            # Formatear respuesta
            history = []
            for attempt in login_history:
                history.append({
                    'timestamp': attempt.created_at.isoformat(),
                    'ip_address': attempt.ip_address,
                    'location': f"{attempt.city}, {attempt.country}" if attempt.city and attempt.country else None,
                    'device': attempt.user_agent,
                    'success': attempt.is_successful,
                    'method': attempt.attempt_type,
                    'risk_score': attempt.risk_score,
                    'suspicious': attempt.is_suspicious,
                    'failure_reason': attempt.failure_reason if not attempt.is_successful else None
                })
            
            return {
                'login_history': history,
                'recent_failures_count': len(redis_failures),
                'total_records': len(history)
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving login history: {str(e)}"
            )
    
    async def check_rate_limits(self, identifier: str, ip_address: str) -> Dict[str, Any]:
        """
        Verificar estado de rate limiting
        """
        try:
            # Verificar rate limits
            ip_limit = await self.redis_service.check_rate_limit(ip_address, 'ip')
            user_limit = await self.redis_service.check_rate_limit(identifier, 'user')
            
            return {
                'ip_rate_limit': {
                    'allowed': ip_limit.is_allowed,
                    'attempts': ip_limit.attempts_count,
                    'max_attempts': ip_limit.max_attempts,
                    'reset_time': ip_limit.reset_time.isoformat(),
                    'blocked_until': ip_limit.blocked_until.isoformat() if ip_limit.blocked_until else None
                },
                'user_rate_limit': {
                    'allowed': user_limit.is_allowed,
                    'attempts': user_limit.attempts_count,
                    'max_attempts': user_limit.max_attempts,
                    'reset_time': user_limit.reset_time.isoformat(),
                    'blocked_until': user_limit.blocked_until.isoformat() if user_limit.blocked_until else None
                }
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error checking rate limits: {str(e)}"
            )
    
    # ===================================
    # HELPER METHODS
    # ===================================
    
    async def _extract_request_info(self, request: Request) -> Dict[str, Any]:
        """
        Extrae información relevante de la request HTTP
        """
        # Headers de IP (considerando proxies)
        ip_address = (
            request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or
            request.headers.get('X-Real-IP') or
            request.client.host if request.client else 'unknown'
        )
        
        # User agent
        user_agent = request.headers.get('User-Agent', '')
        
        # Device fingerprint (si está disponible)
        device_fingerprint = request.headers.get('X-Device-Fingerprint')
        
        # Geolocalización (si está disponible)
        country = request.headers.get('CF-IPCountry')  # Cloudflare
        city = request.headers.get('CF-IPCity')
        
        # Tipo de sesión basado en User-Agent
        session_type = 'web'
        if 'Mobile' in user_agent:
            session_type = 'mobile'
        elif 'API' in user_agent or 'curl' in user_agent.lower():
            session_type = 'api'
        
        return {
            'ip_address': ip_address,
            'user_agent': user_agent,
            'device_fingerprint': device_fingerprint,
            'country': country,
            'city': city,
            'session_type': session_type,
            'device_name': self._extract_device_name(user_agent),
            'location': f"{city}, {country}" if city and country else None
        }
    
    def _extract_device_name(self, user_agent: str) -> str:
        """
        Extrae nombre del dispositivo del User-Agent
        """
        if not user_agent:
            return 'Unknown Device'
        
        # Detectar tipo de dispositivo
        if 'iPhone' in user_agent:
            return 'iPhone'
        elif 'iPad' in user_agent:
            return 'iPad'
        elif 'Android' in user_agent:
            return 'Android Device'
        elif 'Windows' in user_agent:
            return 'Windows PC'
        elif 'Macintosh' in user_agent:
            return 'Mac'
        elif 'Linux' in user_agent:
            return 'Linux PC'
        else:
            return 'Unknown Device'


# Instancia del controller
auth_controller = AuthController()