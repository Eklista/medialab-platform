# backend/app/modules/users/seeds.py
"""
Users Module Seeds - Initial users for testing and development
"""
from sqlalchemy.orm import Session
from app.models import InternalUser, InstitutionalUser, UserRole, UserArea, UserAcademicUnit
from app.modules.security.models import Role
from app.modules.organizations.models import Area, AcademicUnit
from app.modules.users.services.user_service import user_service
from datetime import datetime


class UsersSeeder:
    """Users module seeder"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def seed_all(self):
        """Seed all users data"""
        self.seed_internal_users()
        self.seed_institutional_users()
    
    def seed_internal_users(self):
        """Seed internal users (MediaLab staff)"""
        internal_users_data = [
            # Super Admin
            {
                "first_name": "Pablo",
                "last_name": "Lacán",
                "email": "pablo.lacan@medialab.galileo.edu",
                "username": "pablo.lacan",
                "position": "Director de MediaLab",
                "can_access_dashboard": True,
                "is_verified": True,
                "role_names": ["system_admin"],
                "area_names": ["Coordinación General"],
                "is_primary_area": True
            },
            # Content Manager
            {
                "first_name": "María",
                "last_name": "González",
                "email": "maria.gonzalez@medialab.galileo.edu",
                "username": "maria.gonzalez",
                "position": "Coordinadora de Contenidos",
                "can_access_dashboard": True,
                "is_verified": True,
                "role_names": ["content_manager"],
                "area_names": ["Producción Audiovisual", "Diseño Gráfico"],
                "is_primary_area": True
            },
            # Project Manager
            {
                "first_name": "Carlos",
                "last_name": "Herrera",
                "email": "carlos.herrera@medialab.galileo.edu",
                "username": "carlos.herrera",
                "position": "Coordinador de Proyectos",
                "can_access_dashboard": True,
                "is_verified": True,
                "role_names": ["project_manager"],
                "area_names": ["Coordinación General"],
                "is_primary_area": True
            },
            # Content Creator
            {
                "first_name": "Ana",
                "last_name": "Morales",
                "email": "ana.morales@medialab.galileo.edu",
                "username": "ana.morales",
                "position": "Especialista en Video",
                "can_access_dashboard": True,
                "is_verified": True,
                "role_names": ["content_creator"],
                "area_names": ["Producción Audiovisual"],
                "is_primary_area": True
            },
            # Technical Support
            {
                "first_name": "Luis",
                "last_name": "Ramírez",
                "email": "luis.ramirez@medialab.galileo.edu",
                "username": "luis.ramirez",
                "position": "Soporte Técnico",
                "can_access_dashboard": True,
                "is_verified": True,
                "role_names": ["content_creator"],
                "area_names": ["Soporte Técnico"],
                "is_primary_area": True
            }
        ]
        
        for user_data in internal_users_data:
            # Extract role and area names
            role_names = user_data.pop("role_names", [])
            area_names = user_data.pop("area_names", [])
            is_primary_area = user_data.pop("is_primary_area", False)
            
            # Check if user already exists
            existing = self.db.query(InternalUser).filter(
                InternalUser.email == user_data["email"]
            ).first()
            
            if not existing:
                # Generate employee ID and password
                user_data["employee_id"] = user_service.generate_employee_id(self.db)
                password = user_service.generate_initial_password(
                    user_data["first_name"], 
                    user_data["last_name"]
                )
                user_data["password_hash"] = user_service.hash_password(password)
                user_data["password_changed_at"] = datetime.utcnow()
                
                # Create user
                user = InternalUser(**user_data)
                self.db.add(user)
                self.db.flush()
                
                # Assign roles
                for role_name in role_names:
                    role = self.db.query(Role).filter(Role.name == role_name).first()
                    if role:
                        user_role = UserRole(
                            user_id=user.id,
                            role_id=role.id,
                            user_type="internal_user",
                            is_primary=True,
                            assigned_reason="Initial user setup"
                        )
                        self.db.add(user_role)
                
                # Assign areas
                for i, area_name in enumerate(area_names):
                    area = self.db.query(Area).filter(Area.name == area_name).first()
                    if area:
                        user_area = UserArea(
                            user_id=user.id,
                            area_id=area.id,
                            is_primary=is_primary_area and i == 0,
                            role_in_area="Coordinador" if is_primary_area and i == 0 else "Miembro",
                            can_lead_projects=is_primary_area and i == 0,
                            time_allocation_percentage=100 if len(area_names) == 1 else 50,
                            assignment_reason="Initial area assignment"
                        )
                        self.db.add(user_area)
        
        self.db.flush()
    
    def seed_institutional_users(self):
        """Seed institutional users (faculty, students, external clients)"""
        institutional_users_data = [
            # Faculty Member
            {
                "first_name": "Dr. Roberto",
                "last_name": "Chinchilla",
                "email": "roberto.chinchilla@galileo.edu",
                "username": "roberto.chinchilla",
                "institution": "Universidad Galileo",
                "faculty_id": "FAC-2025-001",
                "academic_title": "Doctor en Ciencias de la Computación",
                "position_title": "Director de FISICC",
                "office_phone": "2423-8000 ext. 7101",
                "office_location": "Edificio Galileo, Oficina 301",
                "is_faculty": True,
                "is_student": False,
                "is_external_client": False,
                "can_request_projects": True,
                "is_verified": True,
                "role_names": ["faculty_member"],
                "academic_unit_names": ["Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación"],
                "relationship_type": "faculty"
            },
            # Student
            {
                "first_name": "Andrea",
                "last_name": "López",
                "email": "andrea.lopez@est.galileo.edu",
                "username": "andrea.lopez",
                "institution": "Universidad Galileo",
                "faculty_id": "EST-2025-001",
                "position_title": "Estudiante de Ingeniería en Sistemas",
                "is_faculty": False,
                "is_student": True,
                "is_external_client": False,
                "can_request_projects": True,
                "is_verified": True,
                "role_names": ["student"],
                "academic_unit_names": ["Escuela de Ingeniería en Sistemas de Información y Ciencias de la Computación"],
                "relationship_type": "student"
            },
            # External Client
            {
                "first_name": "Sandra",
                "last_name": "Martínez",
                "email": "sandra.martinez@empresa.com",
                "username": "sandra.martinez",
                "institution": "Empresa Externa S.A.",
                "position_title": "Gerente de Marketing",
                "office_phone": "2234-5678",
                "is_faculty": False,
                "is_student": False,
                "is_external_client": True,
                "can_request_projects": True,
                "is_verified": True,
                "role_names": ["external_client"],
                "academic_unit_names": [],
                "relationship_type": "external"
            },
            # Another Faculty Member
            {
                "first_name": "Dra. Elena",
                "last_name": "Vásquez",
                "email": "elena.vasquez@galileo.edu",
                "username": "elena.vasquez",
                "institution": "Universidad Galileo",
                "faculty_id": "FAC-2025-002",
                "academic_title": "Doctora en Comunicación",
                "position_title": "Profesora de Comunicación Digital",
                "office_phone": "2423-8000 ext. 7205",
                "office_location": "Edificio Galileo, Oficina 205",
                "is_faculty": True,
                "is_student": False,
                "is_external_client": False,
                "can_request_projects": True,
                "is_verified": True,
                "role_names": ["faculty_member"],
                "academic_unit_names": ["Facultad de Ciencia, Tecnología e Industria"],
                "relationship_type": "faculty"
            }
        ]
        
        for user_data in institutional_users_data:
            # Extract role and academic unit names
            role_names = user_data.pop("role_names", [])
            academic_unit_names = user_data.pop("academic_unit_names", [])
            relationship_type = user_data.pop("relationship_type", "member")
            
            # Check if user already exists
            existing = self.db.query(InstitutionalUser).filter(
                InstitutionalUser.email == user_data["email"]
            ).first()
            
            if not existing:
                # Generate password
                password = user_service.generate_initial_password(
                    user_data["first_name"], 
                    user_data["last_name"]
                )
                user_data["password_hash"] = user_service.hash_password(password)
                user_data["password_changed_at"] = datetime.utcnow()
                
                # Create user
                user = InstitutionalUser(**user_data)
                self.db.add(user)
                self.db.flush()
                
                # Assign roles
                for role_name in role_names:
                    role = self.db.query(Role).filter(Role.name == role_name).first()
                    if role:
                        user_role = UserRole(
                            user_id=user.id,
                            role_id=role.id,
                            user_type="institutional_user",
                            is_primary=True,
                            assigned_reason="Initial user setup"
                        )
                        self.db.add(user_role)
                
                # Assign academic units
                for i, unit_name in enumerate(academic_unit_names):
                    academic_unit = self.db.query(AcademicUnit).filter(
                        AcademicUnit.name == unit_name
                    ).first()
                    if academic_unit:
                        user_academic_unit = UserAcademicUnit(
                            user_id=user.id,
                            academic_unit_id=academic_unit.id,
                            relationship_type=relationship_type,
                            is_primary=i == 0,
                            can_represent_unit=relationship_type == "faculty" and i == 0,
                            position_title=user_data.get("position_title"),
                            department=user_data.get("academic_title") if relationship_type == "faculty" else None
                        )
                        self.db.add(user_academic_unit)
        
        self.db.flush()
    
    def reset_data(self):
        """Reset users data"""
        # Delete in dependency order
        self.db.query(UserArea).delete()
        self.db.query(UserAcademicUnit).delete()
        self.db.query(UserRole).delete()
        self.db.query(InternalUser).delete()
        self.db.query(InstitutionalUser).delete()
        self.db.flush()
    
    def get_stats(self):
        """Get seeding statistics"""
        internal_count = self.db.query(InternalUser).count()
        institutional_count = self.db.query(InstitutionalUser).count()
        roles_assigned = self.db.query(UserRole).filter(UserRole.is_active == True).count()
        areas_assigned = self.db.query(UserArea).filter(UserArea.is_active == True).count()
        units_assigned = self.db.query(UserAcademicUnit).filter(UserAcademicUnit.is_active == True).count()
        
        return (f"{internal_count} internal users, {institutional_count} institutional users, "
                f"{roles_assigned} role assignments, {areas_assigned} area assignments, "
                f"{units_assigned} academic unit assignments")


def seed_users_data(db: Session):
    """Convenience function to seed all users data"""
    seeder = UsersSeeder(db)
    seeder.seed_all()
    return seeder.get_stats()