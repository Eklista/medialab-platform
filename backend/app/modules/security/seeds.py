# ==========================================
# 3. backend/app/modules/security/seeds.py
# ==========================================
"""
Security Module Seeds - Refactored as a class
"""
from sqlalchemy.orm import Session
from app.models import Permission, Role, RolePermission


class SecuritySeeder:
    """Security module seeder"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def seed_all(self):
        """Seed all security data"""
        self.seed_permissions()
        self.seed_initial_roles()
    
    def seed_permissions(self):
        """Seed initial permissions"""
        permissions_data = [
            # User Management Permissions
            {
                "name": "users.view",
                "display_name": "View Users",
                "description": "View user profiles and basic information",
                "category": "users",
                "resource": "users",
                "action": "view",
                "sort_order": 10
            },
            {
                "name": "users.create",
                "display_name": "Create Users",
                "description": "Create new user accounts",
                "category": "users",
                "resource": "users",
                "action": "create",
                "sort_order": 20
            },
            {
                "name": "users.edit",
                "display_name": "Edit Users",
                "description": "Edit user profiles and information",
                "category": "users",
                "resource": "users",
                "action": "edit",
                "sort_order": 30
            },
            {
                "name": "users.delete",
                "display_name": "Delete Users",
                "description": "Delete or deactivate user accounts",
                "category": "users",
                "resource": "users",
                "action": "delete",
                "sort_order": 40
            },
            {
                "name": "users.assign_roles",
                "display_name": "Assign User Roles",
                "description": "Assign and manage user roles",
                "category": "users",
                "resource": "users",
                "action": "assign_roles",
                "sort_order": 50
            },
            
            # Content Management Permissions
            {
                "name": "content.view",
                "display_name": "View Content",
                "description": "View published content and media",
                "category": "content",
                "resource": "content",
                "action": "view",
                "sort_order": 10
            },
            {
                "name": "content.create",
                "display_name": "Create Content",
                "description": "Create new content and media",
                "category": "content",
                "resource": "content",
                "action": "create",
                "sort_order": 20
            },
            {
                "name": "content.edit",
                "display_name": "Edit Content",
                "description": "Edit existing content and media",
                "category": "content",
                "resource": "content",
                "action": "edit",
                "sort_order": 30
            },
            {
                "name": "content.delete",
                "display_name": "Delete Content",
                "description": "Delete content and media",
                "category": "content",
                "resource": "content",
                "action": "delete",
                "sort_order": 40
            },
            {
                "name": "content.publish",
                "display_name": "Publish Content",
                "description": "Publish and unpublish content",
                "category": "content",
                "resource": "content",
                "action": "publish",
                "sort_order": 50
            },
            {
                "name": "content.moderate",
                "display_name": "Moderate Content",
                "description": "Review and approve content before publication",
                "category": "content",
                "resource": "content",
                "action": "moderate",
                "sort_order": 60
            },
            
            # Project Management Permissions
            {
                "name": "projects.view",
                "display_name": "View Projects",
                "description": "View project details and progress",
                "category": "projects",
                "resource": "projects",
                "action": "view",
                "sort_order": 10
            },
            {
                "name": "projects.request",
                "display_name": "Request Projects",
                "description": "Submit new project requests",
                "category": "projects",
                "resource": "projects",
                "action": "request",
                "sort_order": 15
            },
            {
                "name": "projects.create",
                "display_name": "Create Projects",
                "description": "Create and setup new projects",
                "category": "projects",
                "resource": "projects",
                "action": "create",
                "sort_order": 20
            },
            {
                "name": "projects.edit",
                "display_name": "Edit Projects",
                "description": "Edit project details and settings",
                "category": "projects",
                "resource": "projects",
                "action": "edit",
                "sort_order": 30
            },
            {
                "name": "projects.delete",
                "display_name": "Delete Projects",
                "description": "Delete or archive projects",
                "category": "projects",
                "resource": "projects",
                "action": "delete",
                "sort_order": 40
            },
            {
                "name": "projects.assign",
                "display_name": "Assign Project Teams",
                "description": "Assign team members to projects",
                "category": "projects",
                "resource": "projects",
                "action": "assign",
                "sort_order": 50
            },
            {
                "name": "projects.manage_budget",
                "display_name": "Manage Project Budget",
                "description": "Manage project financial aspects",
                "category": "projects",
                "resource": "projects",
                "action": "manage_budget",
                "sort_order": 60
            },
            
            # System Administration Permissions
            {
                "name": "roles.view",
                "display_name": "View Roles",
                "description": "View system roles and permissions",
                "category": "admin",
                "resource": "roles",
                "action": "view",
                "sort_order": 10
            },
            {
                "name": "roles.create",
                "display_name": "Create Roles",
                "description": "Create new system roles",
                "category": "admin",
                "resource": "roles",
                "action": "create",
                "sort_order": 20
            },
            {
                "name": "roles.edit",
                "display_name": "Edit Roles",
                "description": "Edit existing roles and permissions",
                "category": "admin",
                "resource": "roles",
                "action": "edit",
                "sort_order": 30
            },
            {
                "name": "roles.delete",
                "display_name": "Delete Roles",
                "description": "Delete system roles",
                "category": "admin",
                "resource": "roles",
                "action": "delete",
                "sort_order": 40
            },
            {
                "name": "system.admin",
                "display_name": "System Administration",
                "description": "Full system administration access",
                "category": "admin",
                "resource": "system",
                "action": "admin",
                "sort_order": 100
            },
            {
                "name": "system.settings",
                "display_name": "System Settings",
                "description": "Manage system configuration and settings",
                "category": "admin",
                "resource": "system",
                "action": "settings",
                "sort_order": 90
            },
            
            # Dashboard Access Permissions
            {
                "name": "dashboard.access",
                "display_name": "Dashboard Access",
                "description": "Access to internal dashboard",
                "category": "dashboard",
                "resource": "dashboard",
                "action": "access",
                "sort_order": 10
            },
            {
                "name": "dashboard.admin",
                "display_name": "Admin Dashboard",
                "description": "Access to administrative dashboard sections",
                "category": "dashboard",
                "resource": "dashboard",
                "action": "admin",
                "sort_order": 20
            },
            {
                "name": "dashboard.analytics",
                "display_name": "Dashboard Analytics",
                "description": "View analytics and insights in dashboard",
                "category": "dashboard",
                "resource": "dashboard",
                "action": "analytics",
                "sort_order": 30
            },
            
            # Reporting Permissions
            {
                "name": "reports.view",
                "display_name": "View Reports",
                "description": "View generated reports and analytics",
                "category": "reports",
                "resource": "reports",
                "action": "view",
                "sort_order": 10
            },
            {
                "name": "reports.create",
                "display_name": "Create Reports",
                "description": "Generate new reports",
                "category": "reports",
                "resource": "reports",
                "action": "create",
                "sort_order": 20
            },
            {
                "name": "reports.export",
                "display_name": "Export Reports",
                "description": "Export reports in various formats",
                "category": "reports",
                "resource": "reports",
                "action": "export",
                "sort_order": 30
            },
            {
                "name": "reports.all",
                "display_name": "All Reports Access",
                "description": "Access to all reports including sensitive data",
                "category": "reports",
                "resource": "reports",
                "action": "all",
                "sort_order": 100
            },
            
            # Profile Management Permissions
            {
                "name": "profile.edit",
                "display_name": "Edit Own Profile",
                "description": "Edit own user profile and settings",
                "category": "users",
                "resource": "profile",
                "action": "edit",
                "sort_order": 5
            },
            {
                "name": "profile.view_others",
                "display_name": "View Other Profiles",
                "description": "View other users' public profiles",
                "category": "users",
                "resource": "profile",
                "action": "view_others",
                "sort_order": 6
            }
        ]
        
        for perm_data in permissions_data:
            # Check if permission already exists
            existing = self.db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not existing:
                permission = Permission(**perm_data)
                self.db.add(permission)
        
        self.db.flush()
    
    def seed_initial_roles(self):
        """Seed initial system roles"""
        roles_data = [
            # System Administrator Role
            {
                "name": "system_admin",
                "display_name": "System Administrator",
                "description": "Full system access for platform administrators",
                "level": 1000,
                "role_type": "system",
                "target_user_type": "internal_user",
                "color": "#dc2626",
                "icon": "shield-check",
                "sort_order": 10,
                "is_system": True,
                "permissions": [
                    "system.admin", "system.settings", "users.create", "users.edit", 
                    "users.delete", "users.view", "users.assign_roles", "roles.create", 
                    "roles.edit", "roles.delete", "roles.view", "dashboard.admin", 
                    "dashboard.access", "dashboard.analytics", "reports.all", "reports.create", 
                    "reports.export", "content.create", "content.edit", "content.delete", 
                    "content.publish", "content.moderate", "content.view", "projects.create", 
                    "projects.edit", "projects.delete", "projects.view", "projects.assign", 
                    "projects.manage_budget", "profile.edit", "profile.view_others"
                ]
            },
            
            # Content Manager Role
            {
                "name": "content_manager",
                "display_name": "Content Manager",
                "description": "Manages content creation and publication",
                "level": 700,
                "role_type": "standard",
                "target_user_type": "internal_user",
                "color": "#059669",
                "icon": "document-text",
                "sort_order": 20,
                "is_system": True,
                "permissions": [
                    "content.create", "content.edit", "content.delete", "content.publish", 
                    "content.moderate", "content.view", "dashboard.access", "dashboard.analytics",
                    "reports.view", "reports.create", "users.view", "profile.edit", 
                    "profile.view_others", "projects.view"
                ]
            },
            
            # Project Manager Role
            {
                "name": "project_manager",
                "display_name": "Project Manager",
                "description": "Manages projects and team assignments",
                "level": 600,
                "role_type": "standard",
                "target_user_type": "internal_user",
                "color": "#7c3aed",
                "icon": "briefcase",
                "sort_order": 30,
                "is_system": True,
                "permissions": [
                    "projects.create", "projects.edit", "projects.view", "projects.assign",
                    "users.view", "content.view", "dashboard.access", "dashboard.analytics",
                    "reports.view", "reports.create", "profile.edit", "profile.view_others"
                ]
            },
            
            # Content Creator Role
            {
                "name": "content_creator",
                "display_name": "Content Creator",
                "description": "Creates and edits content",
                "level": 400,
                "role_type": "standard",
                "target_user_type": "internal_user",
                "color": "#2563eb",
                "icon": "pencil",
                "sort_order": 40,
                "is_system": True,
                "permissions": [
                    "content.create", "content.edit", "content.view", "dashboard.access",
                    "reports.view", "profile.edit", "projects.view"
                ]
            },
            
            # Faculty Member Role
            {
                "name": "faculty_member",
                "display_name": "Faculty Member",
                "description": "University faculty with project request capabilities",
                "level": 300,
                "role_type": "standard",
                "target_user_type": "institutional_user",
                "color": "#0891b2",
                "icon": "academic-cap",
                "sort_order": 50,
                "is_system": True,
                "permissions": [
                    "projects.request", "projects.view", "content.view", "profile.edit",
                    "profile.view_others"
                ]
            },
            
            # Student Role
            {
                "name": "student",
                "display_name": "Student",
                "description": "University student with basic access",
                "level": 200,
                "role_type": "standard",
                "target_user_type": "institutional_user",
                "color": "#65a30d",
                "icon": "user",
                "sort_order": 60,
                "is_system": True,
                "permissions": [
                    "content.view", "profile.edit", "projects.view"
                ]
            },
            
            # External Client Role
            {
                "name": "external_client",
                "display_name": "External Client",
                "description": "External clients who can request services",
                "level": 250,
                "role_type": "standard",
                "target_user_type": "institutional_user",
                "color": "#ea580c",
                "icon": "building-office",
                "sort_order": 70,
                "is_system": True,
                "permissions": [
                    "projects.request", "projects.view", "content.view", "profile.edit"
                ]
            },
            
            # Viewer Role (Basic Access)
            {
                "name": "viewer",
                "display_name": "Viewer",
                "description": "Basic viewing access only",
                "level": 100,
                "role_type": "standard",
                "target_user_type": "both",
                "color": "#6b7280",
                "icon": "eye",
                "sort_order": 80,
                "is_system": True,
                "permissions": [
                    "content.view", "profile.edit"
                ]
            }
        ]
        
        for role_data in roles_data:
            # Extract permissions list
            permission_names = role_data.pop("permissions", [])
            
            # Check if role already exists
            existing_role = self.db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                # Create role
                role = Role(**role_data)
                self.db.add(role)
                self.db.flush()  # Get the ID
                
                # Assign permissions
                for perm_name in permission_names:
                    permission = self.db.query(Permission).filter(Permission.name == perm_name).first()
                    if permission:
                        role_permission = RolePermission(
                            role_id=role.id,
                            permission_id=permission.id,
                            grant_type="direct",
                            assigned_reason="Initial system role setup"
                        )
                        self.db.add(role_permission)
        
        self.db.flush()
    
    def reset_data(self):
        """Reset security data"""
        self.db.query(RolePermission).delete()
        self.db.query(Role).delete()
        self.db.query(Permission).delete()
        self.db.flush()
    
    def get_stats(self):
        """Get seeding statistics"""
        permissions_count = self.db.query(Permission).count()
        roles_count = self.db.query(Role).count()
        assignments_count = self.db.query(RolePermission).filter(RolePermission.is_active == True).count()
        
        return f"{permissions_count} permissions, {roles_count} roles, {assignments_count} assignments"

