"""
User controllers - Business logic for user endpoints
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.modules.users.models import InternalUser
from app.modules.users.schemas.user_schemas import (
    InternalUserCreate, InternalUserUpdate, InternalUserResponse,
    UserSearchParams, UserListResponse, ProfileCompletion
)
from app.modules.users.repositories.user_repository import (
    InternalUserRepository, UserRoleRepository
)
from app.modules.users.services.user_service import user_service


class InternalUsersController:
    """Controller for internal user operations"""
    
    def __init__(self):
        self.repo = InternalUserRepository()
        self.role_repo = UserRoleRepository()
        self.service = user_service
    
    async def create_internal_user(self, user_data: InternalUserCreate, db: Session) -> InternalUserResponse:
        """Create new internal user"""
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
        
        try:
            # Prepare user data
            prepared_data = self.service.prepare_internal_user_data(user_data, db)
            
            # Create user
            user = self.repo.create(db, prepared_data)
            
            # Assign areas if provided
            if user_data.area_ids:
                self.repo.assign_areas(db, user.id, user_data.area_ids)
            
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
    
    async def get_internal_user(self, user_id: int, db: Session) -> InternalUserResponse:
        """Get internal user by ID"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self._build_user_response(user)
    
    async def get_internal_user_by_uuid(self, uuid: str, db: Session) -> InternalUserResponse:
        """Get internal user by UUID"""
        user = self.repo.get_by_uuid(db, uuid)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self._build_user_response(user)
    
    async def get_internal_users(self, params: UserSearchParams, db: Session, minimal: bool = True) -> UserListResponse:
        """Get paginated list of internal users (optimized)"""
        skip = (params.page - 1) * params.per_page
        
        # Use minimal mode by default for listings
        users, total = self.repo.get_all(
            db=db,
            skip=skip,
            limit=params.per_page,
            search=params.q,
            is_active=params.is_active,
            area_id=params.area_id,
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
    
    async def update_internal_user(
        self, 
        user_id: int, 
        update_data: InternalUserUpdate, 
        db: Session
    ) -> InternalUserResponse:
        """Update internal user"""
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
    
    async def delete_internal_user(self, user_id: int, db: Session) -> Dict[str, str]:
        """Delete internal user"""
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
    
    async def assign_areas_to_user(
        self, 
        user_id: int, 
        area_ids: List[int], 
        db: Session
    ) -> Dict[str, str]:
        """Assign areas to internal user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            self.repo.assign_areas(db, user_id, area_ids)
            db.commit()
            
            return {"message": f"Areas assigned successfully to user {user.username}"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error assigning areas: {str(e)}"
            )
    
    async def assign_roles_to_user(
        self, 
        user_id: int, 
        role_ids: List[int], 
        db: Session
    ) -> Dict[str, str]:
        """Assign roles to internal user"""
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        try:
            self.role_repo.assign_multiple_roles(db, user_id, role_ids, "internal_user")
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
        
        return self.service.calculate_profile_completion(user, "internal")
    
    async def deactivate_user(self, user_id: int, reason: str, db: Session) -> Dict[str, str]:
        """Deactivate internal user"""
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
        """Activate internal user"""
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
    
    def _build_user_response(self, user: InternalUser, minimal: bool = False) -> InternalUserResponse:
        """Build user response with calculated fields (optimized)"""
        
        if minimal:
            # For listings, return essential data only
            completion = 75  # Default completion for minimal mode
            areas = []
            roles = []
        else:
            # For details, calculate everything
            areas = []
            if hasattr(user, 'user_areas') and user.user_areas:
                for user_area in user.user_areas:
                    if user_area.is_active and user_area.area:
                        areas.append({
                            "id": user_area.area.id,
                            "name": user_area.area.name,
                            "role_in_area": user_area.role_in_area,
                            "is_primary": user_area.is_primary
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
            completion_obj = self.service.calculate_profile_completion(user, "internal")
            completion = completion_obj.completion_percentage
        
        return InternalUserResponse(
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
            employee_id=user.employee_id,
            position=user.position if not minimal else None,
            banner_photo=user.banner_photo if not minimal else None,
            last_activity=user.last_activity if not minimal else None,
            can_access_dashboard=user.can_access_dashboard,
            areas=areas,
            roles=roles
        )


# Create controller instance
internal_users_controller = InternalUsersController()