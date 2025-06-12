# backend/app/modules/auth/utils/device_detector.py
"""
Device Detector - Detección y fingerprinting de dispositivos para autenticación
"""
import hashlib
import json
import re
from typing import Dict, Any, Optional, List
import user_agents
from user_agents.parsers import UserAgent


class DeviceDetector:
    """Detector de dispositivos y generador de fingerprints"""
    
    def __init__(self):
        self.known_bots = self._load_known_bots()
        self.suspicious_patterns = self._load_suspicious_patterns()
    
    def generate_device_fingerprint(
        self, 
        user_agent: str, 
        accept_language: Optional[str] = None,
        accept_encoding: Optional[str] = None,
        additional_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """Genera fingerprint único del dispositivo"""
        
        fingerprint_components = []
        
        # User Agent procesado
        ua_info = self.parse_user_agent(user_agent)
        fingerprint_components.extend([
            ua_info.get("browser_family", ""),
            ua_info.get("browser_version_major", ""),
            ua_info.get("os_family", ""),
            ua_info.get("os_version", ""),
            ua_info.get("device_family", "")
        ])
        
        # Headers de idioma y encoding
        if accept_language:
            fingerprint_components.append(self._normalize_accept_language(accept_language))
        
        if accept_encoding:
            fingerprint_components.append(self._normalize_accept_encoding(accept_encoding))
        
        # Headers adicionales relevantes
        if additional_headers:
            relevant_headers = [
                "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
                "sec-fetch-site", "sec-fetch-mode", "sec-fetch-dest"
            ]
            
            for header in relevant_headers:
                if header in additional_headers:
                    fingerprint_components.append(additional_headers[header])
        
        # Crear hash del fingerprint
        fingerprint_string = "|".join(str(component) for component in fingerprint_components)
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()[:16]
        
        return fingerprint_hash
    
    def parse_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Parsea User-Agent y extrae información del dispositivo"""
        
        if not user_agent:
            return self._get_empty_device_info()
        
        try:
            ua: UserAgent = user_agents.parse(user_agent)
            
            device_info = {
                "browser_family": ua.browser.family,
                "browser_version": ua.browser.version_string,
                "browser_version_major": str(ua.browser.version[0]) if ua.browser.version else "",
                "os_family": ua.os.family,
                "os_version": ua.os.version_string,
                "os_version_major": str(ua.os.version[0]) if ua.os.version else "",
                "device_family": ua.device.family,
                "device_brand": ua.device.brand,
                "device_model": ua.device.model,
                "is_mobile": ua.is_mobile,
                "is_tablet": ua.is_tablet,
                "is_pc": ua.is_pc,
                "is_bot": ua.is_bot,
                "user_agent": user_agent,
                "user_agent_string": user_agent
            }
            
            device_info.update(self._analyze_device_characteristics(user_agent))
            return device_info
            
        except Exception as e:
            return {
                **self._get_empty_device_info(),
                "parse_error": str(e),
                "user_agent": user_agent
            }
    
    def detect_device_type(self, user_agent: str) -> str:
        """Detecta tipo de dispositivo basado en User-Agent"""
        device_info = self.parse_user_agent(user_agent)
        
        if device_info.get("is_bot"):
            return "bot"
        elif device_info.get("is_mobile"):
            return "mobile"
        elif device_info.get("is_tablet"):
            return "tablet"
        elif device_info.get("is_pc"):
            return "desktop"
        else:
            return "unknown"
    
    def is_suspicious_device(self, user_agent: str) -> Dict[str, Any]:
        """Analiza si el dispositivo es sospechoso"""
        
        suspicion_flags = []
        suspicion_score = 0
        analysis = {}
        
        if not user_agent:
            return {
                "is_suspicious": True,
                "suspicion_score": 100,
                "flags": ["missing_user_agent"],
                "analysis": {"empty_user_agent": True}
            }
        
        # Verificar patrones de bots conocidos
        bot_check = self._check_bot_patterns(user_agent)
        if bot_check["is_bot"]:
            suspicion_score += 50
            suspicion_flags.extend(bot_check["patterns"])
            analysis["bot_detection"] = bot_check
        
        # Verificar User-Agent muy genérico
        if self._is_generic_user_agent(user_agent):
            suspicion_score += 30
            suspicion_flags.append("generic_user_agent")
        
        # Verificar longitud anormal
        if len(user_agent) < 20:
            suspicion_score += 20
            suspicion_flags.append("unusually_short")
        elif len(user_agent) > 1000:
            suspicion_score += 15
            suspicion_flags.append("unusually_long")
        
        # Verificar caracteres sospechosos
        if self._has_suspicious_characters(user_agent):
            suspicion_score += 25
            suspicion_flags.append("suspicious_characters")
        
        # Verificar herramientas automatizadas
        automation_patterns = [
            r"curl/", r"wget/", r"python-requests/", r"python-urllib/",
            r"java/", r"okhttp/", r"apache-httpclient/", r"node-fetch/"
        ]
        
        for pattern in automation_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                suspicion_score += 40
                suspicion_flags.append("automation_tool")
                break
        
        return {
            "is_suspicious": suspicion_score >= 40,
            "suspicion_score": min(suspicion_score, 100),
            "flags": suspicion_flags,
            "analysis": analysis
        }
    
    def get_device_summary(self, user_agent: str) -> Dict[str, Any]:
        """Obtiene resumen completo del dispositivo"""
        
        device_info = self.parse_user_agent(user_agent)
        suspicion_analysis = self.is_suspicious_device(user_agent)
        device_type = self.detect_device_type(user_agent)
        
        return {
            "device_info": device_info,
            "device_type": device_type,
            "suspicion_analysis": suspicion_analysis,
            "fingerprint": self.generate_device_fingerprint(user_agent),
            "analysis_timestamp": "2024-01-01T00:00:00Z"
        }
    
    # ===================================
    # HELPER METHODS
    # ===================================
    
    def _get_empty_device_info(self) -> Dict[str, Any]:
        """Retorna información vacía de dispositivo"""
        return {
            "browser_family": "Unknown",
            "browser_version": "",
            "browser_version_major": "",
            "os_family": "Unknown", 
            "os_version": "",
            "os_version_major": "",
            "device_family": "Unknown",
            "device_brand": "",
            "device_model": "",
            "is_mobile": False,
            "is_tablet": False,
            "is_pc": False,
            "is_bot": False,
            "user_agent": "",
            "user_agent_string": ""
        }
    
    def _analyze_device_characteristics(self, user_agent: str) -> Dict[str, Any]:
        """Análisis adicional de características del dispositivo"""
        characteristics = {}
        
        # Detectar WebView
        if "wv" in user_agent or "WebView" in user_agent:
            characteristics["is_webview"] = True
        
        # Detectar aplicaciones móviles
        mobile_app_patterns = [
            r"FBAV/", r"Instagram", r"WhatsApp", r"Telegram",
            r"Twitter", r"LinkedIn", r"TikTok"
        ]
        
        for pattern in mobile_app_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                characteristics["is_mobile_app"] = True
                break
        
        # Detectar modo headless
        headless_indicators = ["HeadlessChrome", "PhantomJS", "Selenium"]
        for indicator in headless_indicators:
            if indicator in user_agent:
                characteristics["is_headless"] = True
                break
        
        return characteristics
    
    def _normalize_accept_language(self, accept_language: str) -> str:
        """Normaliza header Accept-Language"""
        if not accept_language:
            return ""
        
        languages = []
        for lang_part in accept_language.split(","):
            lang = lang_part.split(";")[0].strip()
            if lang:
                languages.append(lang.lower())
        
        return ",".join(sorted(languages[:3]))
    
    def _normalize_accept_encoding(self, accept_encoding: str) -> str:
        """Normaliza header Accept-Encoding"""
        if not accept_encoding:
            return ""
        
        encodings = []
        for encoding_part in accept_encoding.split(","):
            encoding = encoding_part.split(";")[0].strip()
            if encoding:
                encodings.append(encoding.lower())
        
        return ",".join(sorted(encodings))
    
    def _check_bot_patterns(self, user_agent: str) -> Dict[str, Any]:
        """Verifica patrones de bots conocidos"""
        detected_patterns = []
        
        bot_patterns = [
            r"bot\b", r"crawler", r"spider", r"scraper",
            r"facebook", r"google", r"bing", r"yahoo",
            r"baidu", r"yandex", r"twitterbot", r"linkedinbot"
        ]
        
        for pattern in bot_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                detected_patterns.append(pattern)
        
        for known_bot in self.known_bots:
            if known_bot.lower() in user_agent.lower():
                detected_patterns.append(f"known_bot:{known_bot}")
        
        return {
            "is_bot": len(detected_patterns) > 0,
            "patterns": detected_patterns,
            "confidence": min(len(detected_patterns) * 25, 100)
        }
    
    def _is_generic_user_agent(self, user_agent: str) -> bool:
        """Verifica si el User-Agent es muy genérico"""
        generic_patterns = [
            "Mozilla/5.0",
            "Mozilla/4.0 (compatible; MSIE",
            "User-Agent",
            "curl/",
            "wget/"
        ]
        
        for pattern in generic_patterns:
            if user_agent.strip() == pattern:
                return True
        
        return False
    
    def _has_suspicious_characters(self, user_agent: str) -> bool:
        """Verifica caracteres sospechosos en User-Agent"""
        suspicious_chars = ["<", ">", "{", "}", "[", "]", "|", "\\", "^"]
        
        for char in suspicious_chars:
            if char in user_agent:
                return True
        
        suspicious_sequences = ["null", "undefined", "test", "xxx"]
        for sequence in suspicious_sequences:
            if sequence in user_agent.lower():
                return True
        
        return False
    
    def _load_known_bots(self) -> List[str]:
        """Carga lista de bots conocidos"""
        return [
            "Googlebot", "Bingbot", "Slurp", "DuckDuckBot",
            "Baiduspider", "YandexBot", "facebookexternalhit",
            "Twitterbot", "LinkedInBot", "WhatsApp", "Telegram",
            "curl", "wget", "python-requests", "PostmanRuntime",
            "Apache-HttpClient", "Java", "Go-http-client"
        ]
    
    def _load_suspicious_patterns(self) -> List[str]:
        """Carga patrones sospechosos"""
        return [
            r"null", r"undefined", r"test", r"admin",
            r"script", r"inject", r"<script", r"javascript:",
            r"eval\(", r"alert\(", r"document\."
        ]


# Instancia singleton
device_detector = DeviceDetector()