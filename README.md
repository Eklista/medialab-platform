# Plataforma MediaLab Universidad Galileo

Una plataforma integral full-stack para el MediaLab de Universidad Galileo, que proporciona gestión de contenido, coordinación de proyectos y administración de recursos educativos para la comunidad universitaria.

## 🚀 Características

### 📱 **Experiencia Multi-Usuario**
- **Interfaz Pública**: Navegación y descubrimiento de contenido para la comunidad universitaria
- **Dashboard Interno**: Herramientas de gestión y administración para el personal de MediaLab
- **Dashboard Institucional**: Interfaz para facultad y estudiantes universitarios
- **Panel de Administración**: Administración y analíticas de todo el sistema

### 📝 **Sistema de Gestión de Contenido**
- Integración con videos de YouTube y gestión de metadatos
- Creación y gestión de galerías fotográficas
- Categorización inteligente con filtrado por unidad académica
- Optimización SEO con slugs y metadatos
- Flujo de trabajo de publicación y sistema de aprobación

### 👥 **Gestión de Usuarios**
- **Arquitectura Dual de Usuarios**: Personal interno y usuarios institucionales
- **Control de Acceso Basado en Roles**: Sistema de permisos granular
- **Integración Académica**: Gestión de facultad, estudiantes y clientes externos
- **Estructura Organizacional**: Áreas, unidades académicas y jerarquías

### 🎯 **Gestión de Proyectos**
- Desarrollo de cursos y creación de contenido educativo
- Producción de podcasts y gestión de contenido de audio
- Manejo de solicitudes de servicio y comunicación con clientes
- Asignación de recursos y gestión de equipos
- Seguimiento de cronograma y gestión de hitos

### 🔧 **Herramientas Operativas**
- **Gestión de Inventario**: Catálogo de equipos y sistema de reservas
- **Integración de Calendario**: Programación y gestión de disponibilidad
- **Gestión de Archivos**: Subida, almacenamiento y control de versiones
- **Flujos de Aprobación**: Procesos de aprobación multi-etapa
- **Registro de Auditoría**: Seguimiento completo de actividades y cumplimiento

### 🤖 **Características Modernas**
- **Integración de Chat IA**: Asistencia inteligente y soporte de contenido
- **Comunicación en Tiempo Real**: Notificaciones y actualizaciones basadas en WebSocket
- **Analíticas Avanzadas**: Métricas de actividad de usuarios y rendimiento de contenido
- **Responsive Mobile**: Optimizado para todos los tipos de dispositivos

## 🏗️ Arquitectura

### **Backend (FastAPI + Python)**
```
backend/
├── app/
│   ├── core/           # Configuración y setup de base de datos
│   ├── modules/        # Módulos basados en características
│   │   ├── auth/       # Autenticación y autorización
│   │   ├── users/      # Gestión de usuarios (internos/institucionales)
│   │   ├── cms/        # Sistema de gestión de contenido
│   │   ├── projects/   # Gestión del ciclo de vida de proyectos
│   │   ├── security/   # RBAC y permisos
│   │   ├── organizations/ # Gestión de estructura académica
│   │   └── ...         # Módulos de negocio adicionales
│   └── shared/         # Utilidades comunes y clases base
├── alembic/           # Migraciones de base de datos
└── scripts/           # Datos semilla y scripts de mantenimiento
```

### **Frontend (React + TypeScript)**
```
frontend/src/
├── app/               # Configuración a nivel de aplicación
│   ├── config/        # Variables de entorno y feature flags
│   ├── layouts/       # Componentes de layout para diferentes tipos de usuario
│   ├── router/        # Routing y guards de navegación
│   └── store/         # Gestión de estado global
├── modules/           # Módulos basados en características (espeja backend)
│   ├── auth/          # Flujos de autenticación
│   ├── userManagement/ # Administración de usuarios
│   ├── cmsDashboard/  # Interfaz de gestión de contenido
│   ├── cmsFrontend/   # Visualización pública de contenido
│   ├── projects/      # Herramientas de gestión de proyectos
│   ├── aiChat/        # Integración de asistencia IA
│   └── ...            # Módulos de características adicionales
└── shared/            # Componentes reutilizables y utilidades
    ├── api/           # Cliente HTTP y comunicación con backend
    ├── components/    # Librería de componentes UI
    ├── hooks/         # Custom React hooks
    ├── services/      # Servicios de lógica de negocio
    └── types/         # Definiciones TypeScript
```

## 🛠️ Stack Tecnológico

### **Backend**
- **Framework**: FastAPI (Python 3.12)
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Caché**: Redis para sesiones y caché de datos
- **Migraciones**: Alembic para versionado de base de datos
- **Autenticación**: Tokens JWT con permisos basados en roles
- **Almacenamiento de Archivos**: Almacenamiento local con estructura de directorios organizada
- **Documentación API**: Generación automática OpenAPI/Swagger

### **Frontend**
- **Framework**: React 19 con TypeScript
- **Herramienta de Build**: Vite para desarrollo rápido y builds optimizados
- **Estilos**: Tailwind CSS con sistema de diseño personalizado
- **Componentes UI**: Primitivos Radix UI para accesibilidad
- **Gestión de Estado**: Zustand para estado global
- **Formularios**: React Hook Form con validación Zod
- **Animaciones**: Framer Motion para interacciones suaves
- **Cliente HTTP**: Axios con interceptors y manejo de errores

### **Infraestructura**
- **Containerización**: Docker con builds multi-etapa
- **Desarrollo**: Docker Compose para desarrollo local
- **Base de Datos**: PostgreSQL 15 con connection pooling optimizado
- **Reverse Proxy**: Configuración Nginx lista
- **Manejo de Archivos**: Integración OpenCV para procesamiento de imágenes

## 🚀 Inicio Rápido

### **Prerrequisitos**
- Docker y Docker Compose
- Node.js 18+ (para desarrollo local del frontend)
- Python 3.12+ (para desarrollo local del backend)

### **Configuración de Desarrollo**

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd medialab-platform
```

2. **Configuración del Entorno**
```bash
# Copiar plantilla de variables de entorno
cp .env.example .env

# Configurar las variables de entorno
# - Credenciales de base de datos
# - Claves secretas
# - Configuraciones de API
```

3. **Iniciar con Docker Compose**
```bash
# Iniciar todos los servicios (backend, base de datos, redis)
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

4. **Configuración de Base de Datos**
```bash
# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Cargar datos iniciales
docker-compose exec backend python -m scripts.seed_data
```

5. **Desarrollo del Frontend**
```bash
cd frontend
npm install
npm run dev
```

### **Acceder a la Aplicación**
- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8547
- **Documentación API**: http://localhost:8547/docs

## 📚 Documentación de Módulos

### **Módulos Principales**

#### **Autenticación y Seguridad**
- Autenticación basada en JWT con tokens de actualización
- Control de acceso basado en roles (RBAC) con permisos granulares
- Soporte para autenticación multi-factor
- Gestión de sesiones y logging de seguridad

#### **Gestión de Usuarios**
- **Usuarios Internos**: Personal de MediaLab con asignaciones de área
- **Usuarios Institucionales**: Facultad, estudiantes y clientes externos
- Gestión de perfiles con seguimiento de completitud
- Mapeo de relaciones organizacionales

#### **Gestión de Contenido**
- Integración con videos de YouTube con metadatos
- Creación y gestión de galerías fotográficas
- Organización basada en categorías con filtrado por unidad académica
- Optimización SEO y compartición social

#### **Gestión de Proyectos**
- Soporte multi-tipo de proyectos (cursos, podcasts, personalizados)
- Asignación de recursos y gestión de equipos
- Seguimiento de cronograma y reportes de hitos
- Comunicación con clientes y recolección de feedback

## 🔧 Guías de Desarrollo

### **Desarrollo Backend**
- Seguir la arquitectura de módulos basada en características
- Usar patrón repository para acceso a datos
- Implementar manejo comprehensivo de errores
- Escribir pruebas unitarias para lógica de negocio
- Documentar endpoints de API con esquemas apropiados

### **Desarrollo Frontend**
- Usar organización de módulos basada en características
- Implementar tipado TypeScript apropiado
- Seguir patrones de composición de componentes
- Usar custom hooks para lógica de negocio
- Mantener principios de diseño responsivo

### **Gestión de Base de Datos**
- Usar Alembic para todos los cambios de esquema
- Seguir convenciones de nomenclatura para tablas y columnas
- Implementar indexado apropiado para rendimiento
- Usar transacciones para consistencia de datos

## 📖 Documentación de API

La documentación de la API se genera automáticamente y está disponible en:
- **Desarrollo**: http://localhost:8547/docs
- **Swagger UI Interactivo**: http://localhost:8547/redoc

### **Endpoints Principales de API**
- `/api/auth/` - Autenticación y autorización
- `/api/users/` - Operaciones de gestión de usuarios
- `/api/cms/` - Sistema de gestión de contenido
- `/api/projects/` - Gestión del ciclo de vida de proyectos
- `/api/security/` - Gestión de roles y permisos

## 🤝 Contribuir

1. Hacer fork del repositorio
2. Crear una rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Seguir los estándares y convenciones de código
4. Escribir pruebas para nueva funcionalidad
5. Hacer commit de los cambios (`git commit -m 'Agregar característica increíble'`)
6. Push a la rama (`git push origin feature/caracteristica-increible`)
7. Abrir un Pull Request

## 📄 Licencia

Este proyecto es software propietario desarrollado para el MediaLab de Universidad Galileo. Todos los derechos reservados.

## 🏛️ MediaLab Universidad Galileo

Esta plataforma está desarrollada específicamente para el MediaLab de Universidad Galileo para mejorar la creación de contenido educativo, gestión de proyectos y participación de la comunidad dentro del ecosistema universitario.

**Contacto**: Equipo MediaLab - Universidad Galileo
**Sitio Web**: [Universidad Galileo](https://www.galileo.edu)

---

**Construido con ❤️ para la educación e innovación en Universidad Galileo**