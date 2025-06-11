"""
User service - Business logic for user operations
"""
import re
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.modules.users.models import InternalUser, InstitutionalUser
from app.modules.users.schemas.user_schemas import (
    InternalUserCreate, InternalUserUpdate,
    InstitutionalUserCreate, InstitutionalUserUpdate,
    ProfileCompletion
)


class UserService:
    """Service for user operations"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # ===================================
    # PASSWORD OPERATIONS
    # ===================================
    
    def generate_initial_password(self, first_name: str, last_name: str, year: Optional[int] = None) -> str:
        """
        Generate initial password: PabLac2017 format
        """
        # Clean names
        first_clean = re.sub(r'[^a-zA-Z]', '', first_name).strip()
        last_clean = re.sub(r'[^a-zA-Z]', '', last_name).strip()
        
        # Take first 3 characters
        first_part = first_clean[:3].capitalize() if len(first_clean) >= 3 else first_clean.capitalize()
        last_part = last_clean[:3].capitalize() if len(last_clean) >= 3 else last_clean.capitalize()
        
        # Use provided year or current year
        year_part = str(year) if year else str(datetime.now().year)
        
        return f"{first_part}{last_part}{year_part}"
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    # ===================================
    # USERNAME OPERATIONS
    # ===================================
    
    def generate_username(self, first_name: str, last_name: str, db: Session, user_type: str = "internal") -> str:
        """
        Generate unique username: pablo.lacan format
        """
        # Clean names
        first_clean = re.sub(r'[^a-zA-Z]', '', first_name).lower().strip()
        last_clean = re.sub(r'[^a-zA-Z]', '', last_name).lower().strip()
        
        base_username = f"{first_clean}.{last_clean}"
        username = base_username
        counter = 1
        
        # Check uniqueness across both user types
        while self._username_exists(username, db):
            username = f"{base_username}{counter}"
            counter += 1
        
        return username
    
    def _username_exists(self, username: str, db: Session) -> bool:
        """Check if username exists in either user table"""
        internal_exists = db.query(InternalUser).filter(InternalUser.username == username).first()
        institutional_exists = db.query(InstitutionalUser).filter(InstitutionalUser.username == username).first()
        return internal_exists is not None or institutional_exists is not None
    
    # ===================================
    # EMPLOYEE ID OPERATIONS
    # ===================================
    
    def generate_employee_id(self, db: Session, year: Optional[int] = None) -> str:
        """
        Generate employee ID: EMP-2025-001 format
        """
        current_year = year or datetime.now().year
        
        # Find highest number for current year
        pattern = f"EMP-{current_year}-%"
        last_employee = (
            db.query(InternalUser)
            .filter(InternalUser.employee_id.like(pattern))
            .order_by(InternalUser.employee_id.desc())
            .first()
        )
        
        if last_employee and last_employee.employee_id:
            # Extract number from last employee ID
            parts = last_employee.employee_id.split('-')
            if len(parts) == 3:
                try:
                    last_number = int(parts[2])
                    next_number = last_number + 1
                except ValueError:
                    next_number = 1
            else:
                next_number = 1
        else:
            next_number = 1
        
        return f"EMP-{current_year}-{next_number:03d}"
    
    # ===================================
    # PROFILE COMPLETION
    # ===================================
    
    def calculate_profile_completion(self, user: Any, user_type: str = "internal") -> ProfileCompletion:
        """
        Calculate profile completion percentage and missing fields
        """
        required_fields = self._get_required_fields(user_type)
        optional_fields = self._get_optional_fields(user_type)
        
        completed_required = 0
        completed_optional = 0
        missing_fields = []
        suggestions = []
        
        # Check required fields
        for field, weight in required_fields.items():
            value = getattr(user, field, None)
            if self._is_field_completed(value):
                completed_required += weight
            else:
                missing_fields.append(field)
        
        # Check optional fields
        for field, weight in optional_fields.items():
            value = getattr(user, field, None)
            if self._is_field_completed(value):
                completed_optional += weight
            else:
                suggestions.append(field)
        
        # Calculate percentage (required fields = 70%, optional = 30%)
        required_percentage = (completed_required / sum(required_fields.values())) * 70
        optional_percentage = (completed_optional / sum(optional_fields.values())) * 30 if optional_fields else 0
        
        total_percentage = int(required_percentage + optional_percentage)
        
        return ProfileCompletion(
            completion_percentage=total_percentage,
            missing_fields=missing_fields,
            suggestions=suggestions
        )
    
    def _get_required_fields(self, user_type: str) -> Dict[str, int]:
        """Get required fields with weights"""
        base_required = {
            'first_name': 15,
            'last_name': 15,
            'email': 20,
            'username': 10,
        }
        
        if user_type == "internal":
            base_required.update({
                'employee_id': 10,
                'can_access_dashboard': 5,
            })
        elif user_type == "institutional":
            base_required.update({
                'institution': 10,
                'is_faculty': 5,
                'is_student': 5,
                'is_external_client': 5,
            })
        
        return base_required
    
    def _get_optional_fields(self, user_type: str) -> Dict[str, int]:
        """Get optional fields with weights"""
        base_optional = {
            'phone': 10,
            'bio': 10,
            'profile_photo': 10,
        }
        
        if user_type == "internal":
            base_optional.update({
                'position': 15,
                'banner_photo': 10,
            })
        elif user_type == "institutional":
            base_optional.update({
                'academic_title': 10,
                'position_title': 10,
                'office_phone': 5,
                'office_location': 10,
            })
        
        return base_optional
    
    def _is_field_completed(self, value: Any) -> bool:
        """Check if a field is considered completed"""
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, bool):
            return True  # Boolean fields are always considered complete
        if isinstance(value, (int, float)):
            return value is not None
        if isinstance(value, list):
            return len(value) > 0
        return True
    
    # ===================================
    # VALIDATION HELPERS
    # ===================================
    
    def validate_email_unique(self, email: str, db: Session, exclude_user_id: Optional[int] = None) -> bool:
        """Validate email is unique across both user types"""
        internal_query = db.query(InternalUser).filter(InternalUser.email == email)
        institutional_query = db.query(InstitutionalUser).filter(InstitutionalUser.email == email)
        
        if exclude_user_id:
            internal_query = internal_query.filter(InternalUser.id != exclude_user_id)
            institutional_query = institutional_query.filter(InstitutionalUser.id != exclude_user_id)
        
        internal_exists = internal_query.first()
        institutional_exists = institutional_query.first()
        
        return internal_exists is None and institutional_exists is None
    
    def validate_username_unique(self, username: str, db: Session, exclude_user_id: Optional[int] = None) -> bool:
        """Validate username is unique across both user types"""
        internal_query = db.query(InternalUser).filter(InternalUser.username == username)
        institutional_query = db.query(InstitutionalUser).filter(InstitutionalUser.username == username)
        
        if exclude_user_id:
            internal_query = internal_query.filter(InternalUser.id != exclude_user_id)
            institutional_query = institutional_query.filter(InstitutionalUser.id != exclude_user_id)
        
        internal_exists = internal_query.first()
        institutional_exists = institutional_query.first()
        
        return internal_exists is None and institutional_exists is None
    
    # ===================================
    # USER CREATION HELPERS
    # ===================================
    
    def prepare_internal_user_data(self, user_data: InternalUserCreate, db: Session) -> Dict[str, Any]:
        """Prepare internal user data for creation"""
        # Generate username if not provided
        if not user_data.username:
            user_data.username = self.generate_username(user_data.first_name, user_data.last_name, db)
        
        # Generate employee ID
        employee_id = self.generate_employee_id(db)
        
        # Generate initial password
        current_year = datetime.now().year
        initial_password = self.generate_initial_password(user_data.first_name, user_data.last_name, current_year)
        password_hash = self.hash_password(initial_password)
        
        return {
            **user_data.dict(exclude={'area_ids'}),
            'employee_id': employee_id,
            'password_hash': password_hash,
            'password_changed_at': datetime.utcnow(),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    def prepare_institutional_user_data(self, user_data: InstitutionalUserCreate, db: Session) -> Dict[str, Any]:
        """Prepare institutional user data for creation"""
        # Generate username if not provided
        if not user_data.username:
            user_data.username = self.generate_username(user_data.first_name, user_data.last_name, db)
        
        # Generate initial password
        current_year = datetime.now().year
        initial_password = self.generate_initial_password(user_data.first_name, user_data.last_name, current_year)
        password_hash = self.hash_password(initial_password)
        
        return {
            **user_data.dict(exclude={'academic_unit_ids'}),
            'password_hash': password_hash,
            'password_changed_at': datetime.utcnow(),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    # ===================================
    # SEARCH AND FILTERING
    # ===================================
    
    def build_search_filter(self, query: str) -> List[Any]:
        """Build search filters for user queries"""
        search_terms = query.strip().split()
        filters = []
        
        for term in search_terms:
            term_filter = []
            # Add search conditions here when we implement repositories
            filters.append(term_filter)
        
        return filters


# Create service instance
user_service = UserService()