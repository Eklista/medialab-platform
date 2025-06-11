"""
Institutional Users Controller - Business logic for institutional user endpoints
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.users.models import InstitutionalUser
from app.modules.users.schemas.user_schemas import (
    InstitutionalUserCreate, InstitutionalUserUpdate, InstitutionalUserResponse,
    UserSearchParams, UserListResponse, ProfileCompletion
)
from app.modules.users.repositories.user_repository import (
    InstitutionalUserRepository, UserRoleRepository
)
from app.modules.users.services.user_service import user_service


class InstitutionalUsersController:
    """Controller for institutional user operations"""
    
    def __init__(self):
        self.repo = InstitutionalUserRepository()
        self.role_repo = UserRoleRepository()
        self.service = user_service
    
    async def create_institutional_user(
        self, 
        user_data: InstitutionalUserCreate, 
        db: Session
    ) -> InstitutionalUserResponse:
        """Create new institutional user"""
        # Validate email uniqueness
        if not self.service.validate_email_unique(user_data.email, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Validate username uniqueness if provided
        if user_data.username and not self.service.validate_username_unique(user_data.username, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Validate user type flags
        user_type_count = sum([user_data.is_faculty, user_data.is_student, user_data.is_external_client])
        if user_type_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must be assigned at least one type (faculty, student, or external client)"
            )
        
        try:
            # Prepare user data
            prepared_data = self.service.prepare_institutional_user_data(user_data, db)
            
            # Create user
            user = self.repo.create(db, prepared_data)
            
            # Assign academic units if provided
            if user_data.academic_unit_ids:
                self.repo.assign_academic_units(db, user.id, user_data.academic_unit_ids)
            
            db.commit()
            
            # Refresh user with relationships
            user = self.repo.get_by_id(db, user.id)
            
            return self._build_user_response(user)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )
    
    async def get_institutional_user(self, user_id: int, db: Session) -> InstitutionalUserResponse:
        """Get institutional user by ID"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self._build_user_response(user)
    
    async def get_institutional_user_by_uuid(self, uuid: str, db: Session) -> InstitutionalUserResponse:
        """Get institutional user by UUID"""
        user = self.repo.get_by_uuid(db, uuid)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self._build_user_response(user)
    
    async def get_institutional_users(self, params: UserSearchParams, db: Session, minimal: bool = True) -> UserListResponse:
        """Get paginated list of institutional users (optimized)"""
        skip = (params.page - 1) * params.per_page
        
        # Use minimal mode by default for listings
        users, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            is_active=params.is_active,
            academic_unit_id=params.academic_unit_id,
            minimal=minimal
        )
        
        user_responses = [self._build_user_response(user, minimal=minimal) for user in users]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=(total + params.per_page - 1) // params.per_page
        )
    
    async def update_institutional_user(
        self, 
        user_id: int, 
        update_data: InstitutionalUserUpdate, 
        db: Session
    ) -> InstitutionalUserResponse:
        """Update institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate email uniqueness if changed
        if update_data.email and update_data.email != user.email:
            if not self.service.validate_email_unique(update_data.email, db, exclude_user_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Validate username uniqueness if changed
        if update_data.username and update_data.username != user.username:
            if not self.service.validate_username_unique(update_data.username, db, exclude_user_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
        
        try:
            # Update user
            update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
            updated_user = self.repo.update(db, user, update_dict)
            
            db.commit()
            
            # Refresh user with relationships
            updated_user = self.repo.get_by_id(db, user_id)
            
            return self._build_user_response(updated_user)
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating user: {str(e)}"
            )
    
    async def delete_institutional_user(self, user_id: int, db: Session) -> Dict[str, str]:
        """Delete institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            self.repo.delete(db, user)
            db.commit()
            
            return {"message": "User deleted successfully"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting user: {str(e)}"
            )
    
    async def assign_academic_units_to_user(
        self, 
        user_id: int, 
        academic_unit_ids: List[int], 
        db: Session
    ) -> Dict[str, str]:
        """Assign academic units to institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            self.repo.assign_academic_units(db, user_id, academic_unit_ids)
            db.commit()
            
            return {"message": f"Academic units assigned successfully to user {user.username}"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error assigning academic units: {str(e)}"
            )
    
    async def assign_roles_to_user(
        self, 
        user_id: int, 
        role_ids: List[int], 
        db: Session
    ) -> Dict[str, str]:
        """Assign roles to institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            self.role_repo.assign_multiple_roles(db, user_id, role_ids, "institutional_user")
            db.commit()
            
            return {"message": f"Roles assigned successfully to user {user.username}"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error assigning roles: {str(e)}"
            )
    
    async def get_user_profile_completion(self, user_id: int, db: Session) -> ProfileCompletion:
        """Get user profile completion status"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self.service.calculate_profile_completion(user, "institutional")
    
    async def get_users_by_type(
        self, 
        user_type: str, 
        params: UserSearchParams, 
        db: Session,
        minimal: bool = True
    ) -> UserListResponse:
        """Get users filtered by type (faculty, student, external) (optimized)"""
        skip = (params.page - 1) * params.per_page
        
        users, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            is_active=params.is_active,
            academic_unit_id=params.academic_unit_id,
            user_type_filter=user_type,
            minimal=minimal
        )
        
        user_responses = [self._build_user_response(user, minimal=minimal) for user in users]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=(total + params.per_page - 1) // params.per_page
        )
    
    async def deactivate_user(self, user_id: int, reason: str, db: Session) -> Dict[str, str]:
        """Deactivate institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            update_data = {"is_active": False}
            self.repo.update(db, user, update_data)
            db.commit()
            
            return {"message": f"User {user.username} deactivated successfully"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deactivating user: {str(e)}"
            )
    
    async def activate_user(self, user_id: int, db: Session) -> Dict[str, str]:
        """Activate institutional user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            update_data = {"is_active": True}
            self.repo.update(db, user, update_data)
            db.commit()
            
            return {"message": f"User {user.username} activated successfully"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error activating user: {str(e)}"
            )
    
    def _build_user_response(self, user: InstitutionalUser, minimal: bool = False) -> InstitutionalUserResponse:
        """Build user response with calculated fields (optimized)"""
        
        if minimal:
            # For listings, return essential data only
            completion = 75  # Default completion for minimal mode
            academic_units = []
            roles = []
        else:
            # For details, calculate everything
            academic_units = []
            if hasattr(user, 'user_academic_units') and user.user_academic_units:
                for user_unit in user.user_academic_units:
                    if user_unit.is_active and user_unit.academic_unit:
                        academic_units.append({
                            "id": user_unit.academic_unit.id,
                            "name": user_unit.academic_unit.name,
                            "abbreviation": user_unit.academic_unit.abbreviation,
                            "relationship_type": user_unit.relationship_type,
                            "is_primary": user_unit.is_primary
                        })
            
            roles = []
            if hasattr(user, 'user_roles') and user.user_roles:
                for user_role in user.user_roles:
                    if user_role.is_active and user_role.role:
                        roles.append({
                            "id": user_role.role.id,
                            "name": user_role.role.name,
                            "display_name": user_role.role.display_name,
                            "is_primary": user_role.is_primary
                        })
            
            # Calculate profile completion
            completion_obj = self.service.calculate_profile_completion(user, "institutional")
            completion = completion_obj.completion_percentage
        
        return InstitutionalUserResponse(
            id=user.id,
            uuid=user.uuid,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            profile_photo=user.profile_photo,
            bio=user.bio if not minimal else None,
            preferred_language=user.preferred_language,
            timezone=user.timezone,
            is_active=user.is_active,
            is_verified=user.is_verified,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at,
            full_name=f"{user.first_name} {user.last_name}",
            profile_completion=completion,
            institution=user.institution,
            faculty_id=user.faculty_id,
            academic_title=user.academic_title if not minimal else None,
            position_title=user.position_title if not minimal else None,
            office_phone=user.office_phone if not minimal else None,
            office_location=user.office_location if not minimal else None,
            is_faculty=user.is_faculty,
            is_student=user.is_student,
            is_external_client=user.is_external_client,
            can_request_projects=user.can_request_projects,
            academic_units=academic_units,
            roles=roles
        )


# Create controller instance
institutional_users_controller = InstitutionalUsersController()