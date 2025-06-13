# backend/app/modules/auth/services/totp_service.py
"""
TOTP Service - Implementación completa de códigos TOTP
"""
import pyotp
import qrcode
import secrets
import bcrypt
import base64
from io import BytesIO
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from ..models import TotpDevice, BackupCode
from ..config.security_config import two_factor_config


class TotpService:
    """Servicio completo de TOTP"""
    
    def __init__(self):
        self.config = two_factor_config
        self.backup_config = self.config.get_backup_codes_config()  # ✅ FIJO: Faltaba esta línea
    
    # ===================================
    # SETUP INICIAL DE 2FA
    # ===================================
    
    def setup_2fa_for_user(
        self, 
        user_id: int, 
        user_type: str, 
        device_name: str,
        db: Session
    ) -> Dict[str, Any]:
        """Configura 2FA para un usuario por primera vez"""
        
        # 1. Generar secret key
        secret_key = pyotp.random_base32()
        
        # 2. Crear dispositivo TOTP (sin verificar aún)
        device_id = secrets.token_urlsafe(16)
        totp_device = TotpDevice(
            user_id=user_id,
            user_type=user_type,
            device_name=device_name,
            device_id=device_id,
            secret_key=secret_key,
            algorithm="SHA1",
            digits=6,
            period=30,
            is_verified=False  # Usuario debe verificar primero
        )
        
        db.add(totp_device)
        db.commit()
        
        # 3. Generar QR code
        qr_code = self._generate_qr_code(user_id, user_type, secret_key, device_name)
        
        # 4. Generar códigos de backup
        backup_codes = self._generate_backup_codes(user_id, user_type, db)
        
        return {
            "device_id": device_id,
            "secret_key": secret_key,  # Solo para mostrar al usuario una vez
            "qr_code": qr_code,
            "backup_codes": backup_codes,
            "setup_instructions": self._get_setup_instructions()
        }
    
    def verify_2fa_setup(
        self, 
        device_id: str, 
        verification_code: str,
        db: Session
    ) -> Dict[str, Any]:
        """Verifica configuración inicial de 2FA"""
        
        device = db.query(TotpDevice).filter(
            TotpDevice.device_id == device_id,
            TotpDevice.is_active == True
        ).first()
        
        if not device:
            return {"success": False, "reason": "device_not_found"}
        
        if device.is_verified:
            return {"success": False, "reason": "already_verified"}
        
        # Verificar código TOTP
        totp = pyotp.TOTP(device.secret_key)
        if totp.verify(verification_code, valid_window=1):
            device.verify_device()
            device.is_primary = True  # Primer dispositivo es primario
            db.commit()
            
            return {
                "success": True,
                "message": "2FA setup completed successfully"
            }
        
        return {"success": False, "reason": "invalid_code"}
    
    # ===================================
    # VALIDACIÓN DE CÓDIGOS
    # ===================================
    
    def validate_totp_code(
        self, 
        user_id: int, 
        user_type: str, 
        code: str,
        db: Session
    ) -> Dict[str, Any]:
        """Valida código TOTP durante login"""
        
        # 1. Buscar dispositivos activos del usuario
        devices = db.query(TotpDevice).filter(
            TotpDevice.user_id == user_id,
            TotpDevice.user_type == user_type,
            TotpDevice.is_active == True,
            TotpDevice.is_verified == True
        ).all()
        
        if not devices:
            return {"success": False, "reason": "no_2fa_devices"}
        
        # 2. Intentar validar con cada dispositivo
        for device in devices:
            totp = pyotp.TOTP(device.secret_key)
            
            # Ventana de tiempo más amplia para compensar delay
            if totp.verify(code, valid_window=2):
                # Verificar que no sea replay attack
                current_counter = totp.timecode(datetime.utcnow())
                if current_counter <= device.last_counter:
                    continue  # Código ya usado
                
                # Actualizar dispositivo
                device.mark_as_used(current_counter)
                db.commit()
                
                return {
                    "success": True,
                    "device_used": device.device_name,
                    "method": "totp"
                }
        
        # 3. Intentar con backup codes
        backup_result = self._try_backup_code(user_id, user_type, code, db)
        if backup_result["success"]:
            return backup_result
        
        return {"success": False, "reason": "invalid_code"}
    
    def _try_backup_code(
        self, 
        user_id: int, 
        user_type: str, 
        code: str,
        db: Session
    ) -> Dict[str, Any]:
        """Intenta validar como backup code"""
        
        backup_codes = db.query(BackupCode).filter(
            BackupCode.user_id == user_id,
            BackupCode.user_type == user_type,
            BackupCode.is_active == True,
            BackupCode.is_used == False
        ).all()
        
        for backup_code in backup_codes:
            if bcrypt.checkpw(code.encode(), backup_code.code_hash.encode()):
                # Marcar como usado
                backup_code.mark_as_used("127.0.0.1", "user_agent")
                db.commit()
                
                return {
                    "success": True,
                    "method": "backup_code",
                    "remaining_codes": len([bc for bc in backup_codes if not bc.is_used]) - 1
                }
        
        return {"success": False, "reason": "invalid_backup_code"}
    
    # ===================================
    # GESTIÓN DE DISPOSITIVOS
    # ===================================
    
    def get_user_2fa_devices(self, user_id: int, user_type: str, db: Session) -> List[Dict[str, Any]]:
        """Obtiene dispositivos 2FA del usuario"""
        
        devices = db.query(TotpDevice).filter(
            TotpDevice.user_id == user_id,
            TotpDevice.user_type == user_type,
            TotpDevice.is_active == True
        ).all()
        
        return [{
            "device_id": device.device_id,
            "device_name": device.device_name,
            "is_verified": device.is_verified,
            "is_primary": device.is_primary,
            "created_at": device.created_at.isoformat(),
            "last_used": device.last_used_at.isoformat() if device.last_used_at else None,
            "use_count": device.use_count
        } for device in devices]
    
    def remove_2fa_device(self, device_id: str, db: Session) -> bool:
        """Elimina dispositivo 2FA"""
        device = db.query(TotpDevice).filter(
            TotpDevice.device_id == device_id
        ).first()
        
        if device:
            device.deactivate()
            db.commit()
            return True
        
        return False
    
    # ===================================
    # BACKUP CODES
    # ===================================
    
    def _generate_backup_codes(self, user_id: int, user_type: str, db: Session) -> List[str]:
        """Genera códigos de backup"""
        
        batch_id = secrets.token_urlsafe(16)
        codes = []
        
        for i in range(self.backup_config["count"]):
            # Generar código legible
            code = f"{secrets.randbelow(10000):04d}-{secrets.randbelow(10000):04d}"
            codes.append(code)
            
            # Hash del código
            code_hash = bcrypt.hashpw(code.encode(), bcrypt.gensalt()).decode()
            
            backup_code = BackupCode(
                user_id=user_id,
                user_type=user_type,
                code=code[:8],  # Solo parte para referencia
                code_hash=code_hash,
                batch_id=batch_id,
                sequence_number=i + 1,
                expires_at=datetime.utcnow() + timedelta(days=self.backup_config["expiry_days"])
            )
            
            db.add(backup_code)
        
        db.commit()
        return codes
    
    # ===================================
    # UTILIDADES
    # ===================================
    
    def _generate_qr_code(self, user_id: int, user_type: str, secret_key: str, device_name: str) -> str:
        """Genera código QR para configuración"""
        
        # Crear TOTP URI
        issuer = "MediaLab Universidad Galileo"
        account_name = f"{user_type}_{user_id}@medialab.galileo.edu"
        
        totp_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
            name=account_name,
            issuer_name=issuer
        )
        
        # Generar QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def _get_setup_instructions(self) -> Dict[str, Any]:
        """Instrucciones de configuración"""
        return {
            "step1": "Descarga una app autenticadora (Google Authenticator, Authy, etc.)",
            "step2": "Escanea el código QR con la app",
            "step3": "Ingresa el código de verificación de 6 dígitos",
            "step4": "Guarda los códigos de backup en un lugar seguro",
            "apps_recommended": [
                "Google Authenticator",
                "Microsoft Authenticator", 
                "Authy",
                "1Password",
                "Bitwarden"
            ]
        }
