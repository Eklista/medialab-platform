# backend/app/modules/auth/security/risk_analyzer.py
"""
Risk Analyzer - Análisis inteligente de riesgo para autenticación
"""
import json
import ipaddress
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from geopy.distance import geodesic
import user_agents

from ..config.security_config import risk_analysis_config
from ..exceptions.security_exceptions import SuspiciousActivity


class RiskAnalyzer:
    """Analizador de riesgo para intentos de autenticación"""
    
    def __init__(self):
        self.config = risk_analysis_config
        self.weights = self.config.get_risk_weights()
        self.thresholds = self.config.get_risk_thresholds()
    
    async def analyze_login_risk(
        self,
        user_id: int,
        user_type: str,
        request_info: Dict[str, Any],
        db: Session,
        recent_failures: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Análisis completo de riesgo para intento de login
        
        Args:
            user_id: ID del usuario
            user_type: Tipo de usuario 
            request_info: Información de la request (IP, user_agent, etc.)
            db: Sesión de base de datos
            recent_failures: Intentos fallidos recientes
            
        Returns:
            Diccionario con análisis de riesgo completo
        """
        
        risk_factors = []
        risk_score = 0
        risk_details = {}
        
        # 1. Análisis de intentos fallidos recientes
        failures_risk = await self._analyze_recent_failures(recent_failures or [])
        risk_score += failures_risk["score"]
        if failures_risk["factors"]:
            risk_factors.extend(failures_risk["factors"])
            risk_details["recent_failures"] = failures_risk["details"]
        
        # 2. Análisis de ubicación geográfica
        location_risk = await self._analyze_location_risk(
            user_id, user_type, request_info, db
        )
        risk_score += location_risk["score"]
        if location_risk["factors"]:
            risk_factors.extend(location_risk["factors"])
            risk_details["location"] = location_risk["details"]
        
        # 3. Análisis de dispositivo
        device_risk = await self._analyze_device_risk(
            user_id, user_type, request_info, db
        )
        risk_score += device_risk["score"]
        if device_risk["factors"]:
            risk_factors.extend(device_risk["factors"])
            risk_details["device"] = device_risk["details"]
        
        # 4. Análisis temporal
        temporal_risk = await self._analyze_temporal_patterns(
            user_id, user_type, request_info, db
        )
        risk_score += temporal_risk["score"]
        if temporal_risk["factors"]:
            risk_factors.extend(temporal_risk["factors"])
            risk_details["temporal"] = temporal_risk["details"]
        
        # 5. Análisis de IP y red
        network_risk = await self._analyze_network_risk(request_info)
        risk_score += network_risk["score"]
        if network_risk["factors"]:
            risk_factors.extend(network_risk["factors"])
            risk_details["network"] = network_risk["details"]
        
        # 6. Análisis de comportamiento (bot detection)
        behavior_risk = await self._analyze_behavior_patterns(request_info)
        risk_score += behavior_risk["score"]
        if behavior_risk["factors"]:
            risk_factors.extend(behavior_risk["factors"])
            risk_details["behavior"] = behavior_risk["details"]
        
        # Normalizar score (máximo 100)
        final_risk_score = min(risk_score, 100)
        
        # Determinar nivel de riesgo
        risk_level = self._determine_risk_level(final_risk_score)
        
        # Verificar si requiere acción inmediata
        requires_immediate_action = self._requires_immediate_action(
            final_risk_score, risk_factors
        )
        
        return {
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "risk_details": risk_details,
            "requires_immediate_action": requires_immediate_action,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            
            # Flags específicos para decisiones
            "is_location_change": "new_location" in risk_factors,
            "is_new_device": "new_device" in risk_factors,
            "is_suspicious_timing": "unusual_time" in risk_factors,
            "is_bot_behavior": "bot_behavior" in risk_factors,
            
            # Recomendaciones
            "recommended_actions": self._get_recommended_actions(
                final_risk_score, risk_factors
            )
        }
    
    async def _analyze_recent_failures(
        self, 
        recent_failures: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analiza intentos fallidos recientes"""
        
        if not recent_failures:
            return {"score": 0, "factors": [], "details": {}}
        
        failure_count = len(recent_failures)
        
        # Calcular score basado en número de fallos
        if failure_count >= 5:
            score = self.weights["failed_attempts"]
            factors = ["multiple_recent_failures"]
        elif failure_count >= 3:
            score = self.weights["failed_attempts"] * 0.7
            factors = ["recent_failures"]
        else:
            score = self.weights["failed_attempts"] * 0.3
            factors = ["few_recent_failures"]
        
        # Análisis de patrones en los fallos
        failure_ips = set()
        failure_reasons = {}
        time_span_hours = 0
        
        if recent_failures:
            timestamps = [
                datetime.fromisoformat(f["timestamp"]) 
                for f in recent_failures if "timestamp" in f
            ]
            if len(timestamps) > 1:
                time_span = max(timestamps) - min(timestamps)
                time_span_hours = time_span.total_seconds() / 3600
            
            for failure in recent_failures:
                if "ip_address" in failure:
                    failure_ips.add(failure["ip_address"])
                if "failure_reason" in failure:
                    reason = failure["failure_reason"]
                    failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        # Patrones sospechosos
        if len(failure_ips) > 3:
            score += 10  # Múltiples IPs
            factors.append("multiple_failure_ips")
        
        if time_span_hours > 0 and time_span_hours < 1:
            score += 15  # Fallos muy concentrados en tiempo
            factors.append("rapid_fire_attempts")
        
        return {
            "score": min(score, self.weights["failed_attempts"]),
            "factors": factors,
            "details": {
                "failure_count": failure_count,
                "unique_ips": len(failure_ips),
                "time_span_hours": round(time_span_hours, 2),
                "failure_reasons": failure_reasons
            }
        }
    
    async def _analyze_location_risk(
        self,
        user_id: int,
        user_type: str,
        request_info: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """Analiza riesgo basado en ubicación geográfica"""
        
        current_country = request_info.get("country")
        current_city = request_info.get("city")
        current_lat = request_info.get("latitude")
        current_lon = request_info.get("longitude")
        
        if not current_country:
            return {"score": 0, "factors": [], "details": {"no_location_data": True}}
        
        # Buscar ubicaciones históricas del usuario
        from ..models.login_attempt import LoginAttempt
        
        recent_locations = db.query(LoginAttempt).filter(
            LoginAttempt.user_id == user_id,
            LoginAttempt.user_type == user_type,
            LoginAttempt.is_successful == True,
            LoginAttempt.country.isnot(None),
            LoginAttempt.created_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(LoginAttempt.created_at.desc()).limit(10).all()
        
        if not recent_locations:
            # Usuario nuevo o sin historial
            return {
                "score": 5,  # Riesgo bajo por ser nuevo
                "factors": ["no_location_history"],
                "details": {"is_first_login": True}
            }
        
        # Verificar si la ubicación actual es conocida
        known_countries = set(loc.country for loc in recent_locations if loc.country)
        known_cities = set(f"{loc.city},{loc.country}" for loc in recent_locations if loc.city and loc.country)
        
        factors = []
        score = 0
        details = {
            "current_location": f"{current_city}, {current_country}" if current_city else current_country,
            "known_countries": list(known_countries),
            "known_cities": len(known_cities)
        }
        
        # Verificar país nuevo
        if current_country not in known_countries:
            score += self.weights["new_location"]
            factors.append("new_country")
            details["new_country"] = current_country
        
        # Verificar ciudad nueva
        current_city_country = f"{current_city},{current_country}" if current_city else None
        if current_city_country and current_city_country not in known_cities:
            score += self.weights["new_location"] * 0.5
            factors.append("new_city")
        
        # Calcular distancia si tenemos coordenadas
        if current_lat and current_lon:
            min_distance_km = float('inf')
            
            for location in recent_locations:
                if location.latitude and location.longitude:
                    distance = geodesic(
                        (current_lat, current_lon),
                        (location.latitude, location.longitude)
                    ).kilometers
                    min_distance_km = min(min_distance_km, distance)
            
            if min_distance_km != float('inf'):
                details["min_distance_km"] = round(min_distance_km, 2)
                
                # Distancia muy grande es sospechosa
                if min_distance_km > 1000:  # Más de 1000km
                    score += 15
                    factors.append("large_distance_travel")
                elif min_distance_km > 500:  # Más de 500km
                    score += 8
                    factors.append("significant_travel")
        
        # Verificar velocidad de viaje imposible
        last_location = recent_locations[0] if recent_locations else None
        if (last_location and last_location.latitude and last_location.longitude and 
            current_lat and current_lon):
            
            time_diff = datetime.utcnow() - last_location.created_at
            hours_diff = time_diff.total_seconds() / 3600
            
            if hours_diff > 0:
                distance = geodesic(
                    (current_lat, current_lon),
                    (last_location.latitude, last_location.longitude)
                ).kilometers
                
                # Velocidad promedio en km/h
                speed_kmh = distance / hours_diff
                details["travel_speed_kmh"] = round(speed_kmh, 2)
                
                # Velocidad imposible (avión comercial ~900 km/h)
                if speed_kmh > 1000:
                    score += 25
                    factors.append("impossible_travel_speed")
                elif speed_kmh > 500:  # Muy rápido pero posible
                    score += 10
                    factors.append("very_fast_travel")
        
        return {
            "score": min(score, self.weights["new_location"]),
            "factors": factors,
            "details": details
        }
    
    async def _analyze_device_risk(
        self,
        user_id: int,
        user_type: str,
        request_info: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """Analiza riesgo basado en dispositivo y navegador"""
        
        current_user_agent = request_info.get("user_agent", "")
        current_fingerprint = request_info.get("device_fingerprint")
        
        factors = []
        score = 0
        details = {}
        
        # Parsear user agent
        try:
            ua = user_agents.parse(current_user_agent)
            details["browser"] = f"{ua.browser.family} {ua.browser.version_string}"
            details["os"] = f"{ua.os.family} {ua.os.version_string}"
            details["device_family"] = ua.device.family
            details["is_mobile"] = ua.is_mobile
            details["is_bot"] = ua.is_bot
        except Exception:
            details["user_agent_parse_error"] = True
            score += 5  # Penalizar user agents extraños
        
        # Verificar si es un bot conocido
        if details.get("is_bot"):
            score += self.weights["bot_behavior"]
            factors.append("detected_bot")
        
        # Buscar dispositivos históricos
        from ..models.auth_session import AuthSession
        
        recent_sessions = db.query(AuthSession).filter(
            AuthSession.user_id == user_id,
            AuthSession.user_type == user_type,
            AuthSession.created_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(AuthSession.created_at.desc()).limit(20).all()
        
        if not recent_sessions:
            factors.append("no_device_history")
            score += 5
            details["is_first_device"] = True
        else:
            # Verificar fingerprint conocido
            if current_fingerprint:
                known_fingerprints = set(
                    s.device_fingerprint for s in recent_sessions 
                    if s.device_fingerprint
                )
                
                if current_fingerprint not in known_fingerprints:
                    score += self.weights["new_device"]
                    factors.append("new_device_fingerprint")
                    details["new_fingerprint"] = True
            
            # Verificar user agent conocido
            known_user_agents = set(
                s.user_agent for s in recent_sessions if s.user_agent
            )
            
            if current_user_agent and current_user_agent not in known_user_agents:
                # Verificar si es similar a alguno conocido
                is_similar = self._is_similar_user_agent(current_user_agent, known_user_agents)
                
                if not is_similar:
                    score += self.weights["new_device"] * 0.7
                    factors.append("new_user_agent")
                    details["new_user_agent"] = True
        
        # Verificar patrones sospechosos en user agent
        suspicious_patterns = [
            "curl", "wget", "python", "bot", "crawler", "scraper",
            "automated", "script", "tool", "scanner"
        ]
        
        if any(pattern in current_user_agent.lower() for pattern in suspicious_patterns):
            score += 15
            factors.append("suspicious_user_agent")
        
        # User agent muy corto o vacío
        if len(current_user_agent) < 20:
            score += 10
            factors.append("minimal_user_agent")
        
        return {
            "score": min(score, self.weights["new_device"]),
            "factors": factors,
            "details": details
        }
    
    def _is_similar_user_agent(self, current_ua: str, known_uas: set) -> bool:
        """Verifica si el user agent es similar a alguno conocido"""
        try:
            current_parsed = user_agents.parse(current_ua)
            
            for known_ua in known_uas:
                known_parsed = user_agents.parse(known_ua)
                
                # Mismo browser y OS family
                if (current_parsed.browser.family == known_parsed.browser.family and
                    current_parsed.os.family == known_parsed.os.family):
                    return True
        except Exception:
            pass
        
        return False
    
    async def _analyze_temporal_patterns(
        self,
        user_id: int,
        user_type: str,
        request_info: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """Analiza patrones temporales de acceso"""
        
        current_time = datetime.utcnow()
        current_hour = current_time.hour
        current_weekday = current_time.weekday()  # 0=Monday, 6=Sunday
        
        factors = []
        score = 0
        details = {
            "current_hour": current_hour,
            "current_weekday": current_weekday,
            "is_weekend": current_weekday >= 5,
            "is_night_time": current_hour < 6 or current_hour > 22
        }
        
        # Buscar patrones históricos
        from ..models.login_attempt import LoginAttempt
        
        historical_logins = db.query(LoginAttempt).filter(
            LoginAttempt.user_id == user_id,
            LoginAttempt.user_type == user_type,
            LoginAttempt.is_successful == True,
            LoginAttempt.created_at >= datetime.utcnow() - timedelta(days=30)
        ).all()
        
        if len(historical_logins) < 5:
            # Insuficientes datos para análisis temporal
            return {"score": 0, "factors": [], "details": details}
        
        # Analizar horas usuales
        usual_hours = [login.created_at.hour for login in historical_logins]
        hour_frequency = {}
        for hour in usual_hours:
            hour_frequency[hour] = hour_frequency.get(hour, 0) + 1
        
        # Horas más comunes (top 50%)
        total_logins = len(usual_hours)
        common_hours = set()
        for hour, count in hour_frequency.items():
            if count >= total_logins * 0.1:  # Al menos 10% de los logins
                common_hours.add(hour)
        
        details["common_hours"] = sorted(list(common_hours))
        details["hour_frequency"] = hour_frequency
        
        # Verificar si la hora actual es inusual
        if current_hour not in common_hours:
            score += self.weights["unusual_time"]
            factors.append("unusual_hour")
        
        # Verificar acceso nocturno si no es común
        if details["is_night_time"]:
            night_logins = sum(1 for h in usual_hours if h < 6 or h > 22)
            night_percentage = night_logins / total_logins if total_logins > 0 else 0
            
            if night_percentage < 0.2:  # Menos del 20% de logins nocturnos
                score += 10
                factors.append("unusual_night_access")
        
        # Analizar días de la semana
        usual_weekdays = [login.created_at.weekday() for login in historical_logins]
        weekday_frequency = {}
        for day in usual_weekdays:
            weekday_frequency[day] = weekday_frequency.get(day, 0) + 1
        
        # Verificar acceso en fin de semana si no es común
        if current_weekday >= 5:  # Sábado o domingo
            weekend_logins = sum(1 for d in usual_weekdays if d >= 5)
            weekend_percentage = weekend_logins / total_logins if total_logins > 0 else 0
            
            if weekend_percentage < 0.3:  # Menos del 30% de logins en fin de semana
                score += 8
                factors.append("unusual_weekend_access")
        
        # Verificar velocidad de intentos (tiempo desde último login)
        last_login = max(historical_logins, key=lambda x: x.created_at)
        time_since_last = current_time - last_login.created_at
        hours_since_last = time_since_last.total_seconds() / 3600
        
        details["hours_since_last_login"] = round(hours_since_last, 2)
        
        # Login muy rápido después del anterior (posible sesión robada)
        if hours_since_last < 0.5:  # Menos de 30 minutos
            score += 5
            factors.append("very_recent_login")
        
        return {
            "score": min(score, self.weights["unusual_time"]),
            "factors": factors,
            "details": details
        }
    
    async def _analyze_network_risk(self, request_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza riesgo basado en red e IP"""
        
        ip_address = request_info.get("ip_address", "")
        
        factors = []
        score = 0
        details = {"ip_address": ip_address}
        
        if not ip_address or ip_address == "unknown":
            score += 20
            factors.append("no_ip_address")
            return {"score": score, "factors": factors, "details": details}
        
        try:
            ip = ipaddress.ip_address(ip_address)
            details["ip_version"] = ip.version
            details["is_private"] = ip.is_private
            details["is_loopback"] = ip.is_loopback
            details["is_multicast"] = ip.is_multicast
            
            # IPs privadas en producción son sospechosas
            if ip.is_private and not self._is_development_environment():
                score += 15
                factors.append("private_ip_address")
            
            # IPs de loopback
            if ip.is_loopback:
                score += 10
                factors.append("loopback_ip")
            
            # Verificar rangos sospechosos conocidos
            if self._is_suspicious_ip_range(ip):
                score += self.weights["suspicious_ip"]
                factors.append("suspicious_ip_range")
            
            # TODO: Integrar con servicios de reputación de IP
            # if self._check_ip_reputation(ip_address):
            #     score += 20
            #     factors.append("bad_ip_reputation")
            
        except ValueError:
            score += 15
            factors.append("invalid_ip_format")
        
        return {
            "score": min(score, self.weights["suspicious_ip"]),
            "factors": factors,
            "details": details
        }
    
    async def _analyze_behavior_patterns(self, request_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza patrones de comportamiento para detectar bots"""
        
        factors = []
        score = 0
        details = {}
        
        # Tiempo de respuesta sospechosamente rápido
        response_time_ms = request_info.get("response_time_ms", 1000)
        details["response_time_ms"] = response_time_ms
        
        if response_time_ms < 100:  # Menos de 100ms es sospechoso
            score += self.weights["bot_behavior"] * 0.8
            factors.append("very_fast_response")
        elif response_time_ms < 200:
            score += self.weights["bot_behavior"] * 0.4
            factors.append("fast_response")
        
        # Headers sospechosos o ausentes
        user_agent = request_info.get("user_agent", "")
        if not user_agent:
            score += 15
            factors.append("missing_user_agent")
        
        # Patrones de bot en user agent
        bot_indicators = [
            "bot", "crawler", "spider", "scraper", "automated",
            "curl", "wget", "python-requests", "http"
        ]
        
        if any(indicator in user_agent.lower() for indicator in bot_indicators):
            score += 20
            factors.append("bot_user_agent")
        
        # User agent muy genérico
        generic_patterns = ["mozilla/5.0", "mozilla/4.0"]
        if user_agent.strip() in generic_patterns:
            score += 10
            factors.append("generic_user_agent")
        
        return {
            "score": min(score, self.weights["bot_behavior"]),
            "factors": factors,
            "details": details
        }
    
    def _determine_risk_level(self, risk_score: int) -> str:
        """Determina nivel de riesgo basado en score"""
        if risk_score >= self.thresholds["high"]:
            return "high"
        elif risk_score >= self.thresholds["medium"]:
            return "medium"
        elif risk_score >= self.thresholds["low"]:
            return "low"
        else:
            return "minimal"
    
    def _requires_immediate_action(self, risk_score: int, risk_factors: List[str]) -> bool:
        """Determina si se requiere acción inmediata"""
        
        # Score muy alto
        if risk_score >= 85:
            return True
        
        # Combinaciones específicas peligrosas
        dangerous_combinations = [
            ["impossible_travel_speed", "new_device"],
            ["detected_bot", "multiple_recent_failures"],
            ["suspicious_ip_range", "new_country"],
            ["very_fast_response", "bot_user_agent"]
        ]
        
        for combination in dangerous_combinations:
            if all(factor in risk_factors for factor in combination):
                return True
        
        return False
    
    def _get_recommended_actions(self, risk_score: int, risk_factors: List[str]) -> List[str]:
        """Obtiene acciones recomendadas basadas en el análisis"""
        
        actions = []
        
        if risk_score >= 80:
            actions.append("block_temporarily")
            actions.append("require_2fa")
            actions.append("notify_security_team")
        elif risk_score >= 60:
            actions.append("require_2fa")
            actions.append("log_security_event")
        elif risk_score >= 40:
            actions.append("require_email_verification")
            actions.append("increase_monitoring")
        
        # Acciones específicas por factor
        if "new_location" in risk_factors or "new_country" in risk_factors:
            actions.append("verify_location_change")
        
        if "new_device" in risk_factors:
            actions.append("register_new_device")
        
        if "detected_bot" in risk_factors or "bot_user_agent" in risk_factors:
            actions.append("implement_captcha")
        
        if "impossible_travel_speed" in risk_factors:
            actions.append("flag_account_compromise")
        
        return list(set(actions))  # Remover duplicados
    
    def _is_development_environment(self) -> bool:
        """Verifica si estamos en entorno de desarrollo"""
        import os
        return os.getenv("ENVIRONMENT", "development") == "development"
    
    def _is_suspicious_ip_range(self, ip: ipaddress.IPv4Address) -> bool:
        """Verifica si la IP está en rangos sospechosos conocidos"""
        
        # Lista básica de rangos sospechosos (expandir según necesidad)
        suspicious_ranges = [
            # Tor exit nodes (ejemplo)
            ipaddress.IPv4Network("192.42.116.0/24"),
            # VPN conocidas (ejemplo)
            ipaddress.IPv4Network("185.220.100.0/24"),
        ]
        
        for network in suspicious_ranges:
            if ip in network:
                return True
        
        return False


# Instancia singleton
risk_analyzer = RiskAnalyzer()