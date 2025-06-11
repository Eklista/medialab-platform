# backend/app/modules/organizations/seeds.py
"""
Organizations Module Seeds - Initial data for areas and academic units
"""
from sqlalchemy.orm import Session
from app.models import Area, AcademicUnitType, AcademicUnit


class OrganizationsSeeder:
    """Organizations module seeder"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def seed_all(self):
        """Seed all organizations data"""
        self.seed_areas()
        self.seed_academic_unit_types()
        self.seed_academic_units()
    
    def seed_areas(self):
        """Seed MediaLab areas"""
        areas_data = [
            # Production Areas
            {
                "name": "Transmisión en Vivo",
                "short_name": "Transmisión",
                "description": "Área especializada en transmisiones en vivo de eventos, conferencias y ceremonias",
                "category": "production",
                "specialization": "Live Streaming y Broadcasting",
                "color": "#e74c3c",
                "icon": "video",
                "sort_order": 10,
                "can_lead_projects": True,
                "requires_collaboration": False,
                "max_concurrent_projects": 3,
                "estimated_capacity_hours": 120,
                "contact_email": "transmision@medialab.galileo.edu",
                "location": "Estudio Principal - Edificio MediaLab"
            },
            {
                "name": "Producción Audiovisual",
                "short_name": "Producción",
                "description": "Área encargada de la producción completa de contenido audiovisual",
                "category": "production",
                "specialization": "Video Production y Post-producción",
                "color": "#3498db",
                "icon": "film",
                "sort_order": 20,
                "can_lead_projects": True,
                "requires_collaboration": True,
                "max_concurrent_projects": 5,
                "estimated_capacity_hours": 200,
                "contact_email": "produccion@medialab.galileo.edu",
                "location": "Salas de Edición - Edificio MediaLab"
            },
            {
                "name": "Fotografía Digital",
                "short_name": "Fotografía",
                "description": "Área especializada en fotografía digital para eventos y contenido promocional",
                "category": "creative",
                "specialization": "Fotografía Institucional y de Eventos",
                "color": "#f39c12",
                "icon": "camera",
                "sort_order": 30,
                "can_lead_projects": True,
                "requires_collaboration": False,
                "max_concurrent_projects": 8,
                "estimated_capacity_hours": 160,
                "contact_email": "fotografia@medialab.galileo.edu",
                "location": "Estudio Fotográfico - Edificio MediaLab"
            },
            
            # Creative Areas
            {
                "name": "Diseño Gráfico",
                "short_name": "Diseño",
                "description": "Área de diseño gráfico y comunicación visual para todos los proyectos",
                "category": "creative",
                "specialization": "Diseño Digital y Branding",
                "color": "#9b59b6",
                "icon": "palette",
                "sort_order": 40,
                "can_lead_projects": True,
                "requires_collaboration": True,
                "max_concurrent_projects": 10,
                "estimated_capacity_hours": 160,
                "contact_email": "diseno@medialab.galileo.edu",
                "location": "Área Creativa - Edificio MediaLab"
            },
            {
                "name": "Animación y Motion Graphics",
                "short_name": "Animación",
                "description": "Área especializada en animación 2D/3D y motion graphics",
                "category": "creative",
                "specialization": "Animación Digital y VFX",
                "color": "#e67e22",
                "icon": "play-circle",
                "sort_order": 50,
                "can_lead_projects": True,
                "requires_collaboration": True,
                "max_concurrent_projects": 4,
                "estimated_capacity_hours": 120,
                "contact_email": "animacion@medialab.galileo.edu",
                "location": "Área Creativa - Edificio MediaLab"
            },
            
            # Technical Areas
            {
                "name": "Soporte Técnico",
                "short_name": "Soporte",
                "description": "Área de soporte técnico y mantenimiento de equipos",
                "category": "technical",
                "specialization": "Mantenimiento y Configuración de Equipos",
                "color": "#2c3e50",
                "icon": "settings",
                "sort_order": 60,
                "can_lead_projects": False,
                "requires_collaboration": False,
                "max_concurrent_projects": None,
                "estimated_capacity_hours": 80,
                "contact_email": "soporte@medialab.galileo.edu",
                "contact_phone": "2423-8000 ext. 7890",
                "location": "Área Técnica - Edificio MediaLab"
            },
            {
                "name": "Desarrollo Web",
                "short_name": "Web",
                "description": "Área de desarrollo y mantenimiento de plataformas web",
                "category": "technical",
                "specialization": "Desarrollo Frontend y Backend",
                "color": "#27ae60",
                "icon": "code",
                "sort_order": 70,
                "can_lead_projects": True,
                "requires_collaboration": True,
                "max_concurrent_projects": 6,
                "estimated_capacity_hours": 160,
                "contact_email": "desarrollo@medialab.galileo.edu",
                "location": "Área de Desarrollo - Edificio MediaLab"
            },
            
            # Administrative Areas
            {
                "name": "Coordinación General",
                "short_name": "Coordinación",
                "description": "Área de coordinación y gestión general de proyectos",
                "category": "administrative",
                "specialization": "Project Management y Coordinación",
                "color": "#34495e",
                "icon": "users",
                "sort_order": 80,
                "can_lead_projects": True,
                "requires_collaboration": True,
                "max_concurrent_projects": 15,
                "estimated_capacity_hours": 160,
                "contact_email": "coordinacion@medialab.galileo.edu",
                "contact_phone": "2423-8000 ext. 7800",
                "location": "Oficinas Administrativas - Edificio MediaLab"
            },
            {
                "name": "Logística y Producción",
                "short_name": "Logística",
                "description": "Área de logística, transporte y coordinación de producción",
                "category": "administrative",
                "specialization": "Logística de Eventos y Producción",
                "color": "#7f8c8d",
                "icon": "truck",
                "sort_order": 90,
                "can_lead_projects": False,
                "requires_collaboration": True,
                "max_concurrent_projects": 8,
                "estimated_capacity_hours": 120,
                "contact_email": "logistica@medialab.galileo.edu",
                "location": "Almacén - Edificio MediaLab"
            }
        ]
        
        for area_data in areas_data:
            # Check if area already exists
            existing = self.db.query(Area).filter(Area.name == area_data["name"]).first()
            if not existing:
                area = Area(**area_data)
                self.db.add(area)
        
        self.db.flush()
    
    def seed_academic_unit_types(self):
        """Seed academic unit types"""
        unit_types_data = [
            {
                "name": "facultad",
                "display_name": "Facultad",
                "description": "Unidad académica de nivel superior que agrupa escuelas y programas académicos",
                "hierarchy_level": 1,
                "abbreviation": "FAC",
                "category": "academic",
                "sort_order": 10,
                "allows_students": True,
                "allows_faculty": True,
                "requires_approval": False
            },
            {
                "name": "escuela",
                "display_name": "Escuela",
                "description": "Unidad académica que imparte programas de estudio específicos",
                "hierarchy_level": 2,
                "abbreviation": "ESC",
                "category": "academic",
                "sort_order": 20,
                "allows_students": True,
                "allows_faculty": True,
                "requires_approval": False
            },
            {
                "name": "instituto",
                "display_name": "Instituto",
                "description": "Unidad especializada en investigación y servicios académicos",
                "hierarchy_level": 2,
                "abbreviation": "INST",
                "category": "research",
                "sort_order": 30,
                "allows_students": True,
                "allows_faculty": True,
                "requires_approval": False
            },
            {
                "name": "departamento",
                "display_name": "Departamento",
                "description": "División académica especializada en un área de conocimiento",
                "hierarchy_level": 3,
                "abbreviation": "DEPT",
                "category": "academic",
                "sort_order": 40,
                "allows_students": True,
                "allows_faculty": True,
                "requires_approval": False
            },
            {
                "name": "centro",
                "display_name": "Centro",
                "description": "Unidad especializada en servicios o investigación específica",
                "hierarchy_level": 3,
                "abbreviation": "CENT",
                "category": "service",
                "sort_order": 50,
                "allows_students": False,
                "allows_faculty": True,
                "requires_approval": True
            },
            {
                "name": "laboratorio",
                "display_name": "Laboratorio",
                "description": "Unidad de investigación y práctica especializada",
                "hierarchy_level": 4,
                "abbreviation": "LAB",
                "category": "research",
                "sort_order": 60,
                "allows_students": True,
                "allows_faculty": True,
                "requires_approval": True
            },
            {
                "name": "direccion",
                "display_name": "Dirección",
                "description": "Unidad administrativa de gestión y coordinación",
                "hierarchy_level": 2,
                "abbreviation": "DIR",
                "category": "administrative",
                "sort_order": 70,
                "allows_students": False,
                "allows_faculty": False,
                "requires_approval": True
            },
            {
                "name": "decanato",
                "display_name": "Decanato",
                "description": "Unidad administrativa de una facultad",
                "hierarchy_level": 1,
                "abbreviation": "DEC",
                "category": "administrative",
                "sort_order": 80,
                "allows_students": False,
                "allows_faculty": True,
                "requires_approval": True
            }
        ]
        
        for type_data in unit_types_data:
            # Check if type already exists
            existing = self.db.query(AcademicUnitType).filter(AcademicUnitType.name == type_data["name"]).first()
            if not existing:
                unit_type = AcademicUnitType(**type_data)
                self.db.add(unit_type)
        
        self.db.flush()
    
    def seed_academic_units(self):
        """Seed initial academic units"""
        # Get academic unit types
        facultad_type = self.db.query(AcademicUnitType).filter(AcademicUnitType.name == "facultad").first()
        escuela_type = self.db.query(AcademicUnitType).filter(AcademicUnitType.name == "escuela").first()
        instituto_type = self.db.query(AcademicUnitType).filter(AcademicUnitType.name == "instituto").first()
        
        if not all([facultad_type, escuela_type, instituto_type]):
            return  # Types not seeded yet
        
        academic_units_data = [
            # Facultades
            {
                "name": "Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación",
                "short_name": "Facultad de Ingeniería",
                "abbreviation": "FISICC",
                "description": "Facultad especializada en ingeniería de sistemas, informática y ciencias de la computación",
                "academic_unit_type_id": facultad_type.id,
                "website": "https://fisicc.galileo.edu",
                "email": "info@fisicc.galileo.edu",
                "phone": "2423-8000 ext. 7101",
                "address": "7a. Avenida calle Dr. Eduardo Suger Cofiño, Zona 10, Guatemala",
                "building": "Edificio Galileo",
                "logo_url": "/static/logos/fisicc.png",
                "color_primary": "#1e40af",
                "color_secondary": "#3b82f6",
                "sort_order": 10,
                "allows_public_content": True,
                "requires_approval": False
            },
            {
                "name": "Facultad de Ingeniería",
                "short_name": "FING",
                "abbreviation": "FING",
                "description": "Facultad de Ingeniería con diversas especialidades",
                "academic_unit_type_id": facultad_type.id,
                "website": "https://fing.galileo.edu",
                "email": "info@fing.galileo.edu",
                "phone": "2423-8000 ext. 7201",
                "address": "7a. Avenida calle Dr. Eduardo Suger Cofiño, Zona 10, Guatemala",
                "building": "Edificio Galileo",
                "logo_url": "/static/logos/fing.png",
                "color_primary": "#dc2626",
                "color_secondary": "#ef4444",
                "sort_order": 20,
                "allows_public_content": True,
                "requires_approval": False
            },
            {
                "name": "Facultad de Ciencia, Tecnología e Industria",
                "short_name": "FACTI",
                "abbreviation": "FACTI",
                "description": "Facultad enfocada en ciencias aplicadas, tecnología e industria",
                "academic_unit_type_id": facultad_type.id,
                "website": "https://facti.galileo.edu",
                "email": "info@facti.galileo.edu",
                "phone": "2423-8000 ext. 7301",
                "address": "7a. Avenida calle Dr. Eduardo Suger Cofiño, Zona 10, Guatemala",
                "building": "Edificio Galileo",
                "logo_url": "/static/logos/facti.png",
                "color_primary": "#059669",
                "color_secondary": "#10b981",
                "sort_order": 30,
                "allows_public_content": True,
                "requires_approval": False
            },
            
            # Escuelas
            {
                "name": "Escuela de Ingeniería en Sistemas de Información y Ciencias de la Computación",
                "short_name": "EISIC",
                "abbreviation": "EISIC",
                "description": "Escuela especializada en sistemas de información y ciencias de la computación",
                "academic_unit_type_id": escuela_type.id,
                "email": "eisic@galileo.edu",
                "phone": "2423-8000 ext. 7102",
                "building": "Edificio Galileo",
                "color_primary": "#7c3aed",
                "sort_order": 40,
                "allows_public_content": True,
                "requires_approval": False
            },
            {
                "name": "Escuela de Ingeniería Mecatrónica",
                "short_name": "Mecatrónica",
                "abbreviation": "EMEC",
                "description": "Escuela de ingeniería mecatrónica y automatización",
                "academic_unit_type_id": escuela_type.id,
                "email": "mecatronica@galileo.edu",
                "phone": "2423-8000 ext. 7202",
                "building": "Edificio Galileo",
                "color_primary": "#ea580c",
                "sort_order": 50,
                "allows_public_content": True,
                "requires_approval": False
            },
            
            # Institutos
            {
                "name": "Instituto de Investigación de Ciencias y Tecnología Aplicada",
                "short_name": "IICTA",
                "abbreviation": "IICTA",
                "description": "Instituto de investigación en ciencias y tecnología aplicada",
                "academic_unit_type_id": instituto_type.id,
                "website": "https://iicta.galileo.edu",
                "email": "investigacion@iicta.galileo.edu",
                "phone": "2423-8000 ext. 7401",
                "building": "Edificio de Investigación",
                "color_primary": "#0891b2",
                "color_secondary": "#06b6d4",
                "sort_order": 60,
                "allows_public_content": True,
                "requires_approval": True
            },
            {
                "name": "Instituto de Astronomía y Meteorología",
                "short_name": "IAM",
                "abbreviation": "IAM",
                "description": "Instituto especializado en astronomía y meteorología",
                "academic_unit_type_id": instituto_type.id,
                "website": "https://iam.galileo.edu",
                "email": "astronomia@galileo.edu",
                "phone": "2423-8000 ext. 7402",
                "building": "Observatorio",
                "color_primary": "#4338ca",
                "sort_order": 70,
                "allows_public_content": True,
                "requires_approval": True
            }
        ]
        
        for unit_data in academic_units_data:
            # Check if unit already exists
            existing = self.db.query(AcademicUnit).filter(AcademicUnit.abbreviation == unit_data["abbreviation"]).first()
            if not existing:
                unit = AcademicUnit(**unit_data)
                self.db.add(unit)
        
        self.db.flush()
    
    def reset_data(self):
        """Reset organizations data"""
        self.db.query(AcademicUnit).delete()
        self.db.query(AcademicUnitType).delete()
        self.db.query(Area).delete()
        self.db.flush()
    
    def get_stats(self):
        """Get seeding statistics"""
        areas_count = self.db.query(Area).count()
        types_count = self.db.query(AcademicUnitType).count()
        units_count = self.db.query(AcademicUnit).count()
        
        return f"{areas_count} areas, {types_count} unit types, {units_count} academic units"


def seed_organizations_data(db: Session):
    """Convenience function to seed all organizations data"""
    seeder = OrganizationsSeeder(db)
    seeder.seed_all()
    return seeder.get_stats()