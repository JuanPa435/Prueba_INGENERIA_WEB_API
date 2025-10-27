# 📐 Arquitectura del Sistema - Gestión de Inventario

## Visión General

Sistema de gestión de inventario multi-empresa con autenticación JWT, arquitectura por capas en el backend y SPA (Single Page Application) en el frontend.

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                       FRONTEND                           │
│    HTML5 + CSS3 + JavaScript (Vanilla ES6+)             │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Pages   │  │    CSS   │  │    JS    │             │
│  │  .html   │  │  Styles  │  │  Logic   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST + JWT
                     │
┌────────────────────▼────────────────────────────────────┐
│                     BACKEND                              │
│              Python 3.12 + Flask 2.0                    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Controllers (Blueprints)               │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│  │  │   Auth   │ │ Company  │ │ Product  │        │   │
│  │  └──────────┘ └──────────┘ └──────────┘        │   │
│  └────────┬──────────────────────────────────────┘    │
│           │                                             │
│  ┌────────▼──────────────────────────────────────┐    │
│  │             Middleware                         │    │
│  │      ┌──────────────────────────┐             │    │
│  │      │  JWT Authentication      │             │    │
│  │      │  Role-Based Access       │             │    │
│  │      └──────────────────────────┘             │    │
│  └────────┬──────────────────────────────────────┘    │
│           │                                             │
│  ┌────────▼──────────────────────────────────────┐    │
│  │               Services                         │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐      │    │
│  │  │   Auth   │ │ Company  │ │ Product  │      │    │
│  │  │ Service  │ │ Service  │ │ Service  │      │    │
│  │  └──────────┘ └──────────┘ └──────────┘      │    │
│  └────────┬──────────────────────────────────────┘    │
│           │                                             │
│  ┌────────▼──────────────────────────────────────┐    │
│  │            Models (SQLAlchemy ORM)             │    │
│  │  ┌──────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │    │
│  │  │ User │ │ Company │ │UserComp.│ │Product │ │    │
│  │  └──────┘ └─────────┘ └─────────┘ └────────┘ │    │
│  └────────┬──────────────────────────────────────┘    │
└───────────┼──────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────┐
│                    DATABASE                           │
│                   MySQL Server                        │
│                                                       │
│   ┌──────┐  ┌─────────┐  ┌──────────────┐          │
│   │users │  │companies│  │user_companies│          │
│   └──────┘  └─────────┘  └──────────────┘          │
│                  ┌──────────┐                        │
│                  │ products │                        │
│                  └──────────┘                        │
└──────────────────────────────────────────────────────┘
```

---

## 🔧 Backend - Arquitectura por Capas

### 1. **Config Layer** (Configuración)
- **Propósito:** Configuración de la aplicación
- **Componentes:**
  - `Config.py`: Database URI, SECRET_KEY, JWT settings
- **Responsabilidades:**
  - Cargar variables de entorno
  - Configurar SQLAlchemy
  - Configurar JWT

### 2. **Models Layer** (Modelos de Datos)
- **Propósito:** Definición de estructura de datos
- **Componentes:**
  - `User`: Usuarios del sistema
  - `Company`: Empresas
  - `UserCompany`: Relación usuario-empresa con rol
  - `Product`: Productos del inventario
- **Responsabilidades:**
  - Definir esquema de BD
  - Métodos de serialización
  - Validaciones de datos

### 3. **Services Layer** (Lógica de Negocio)
- **Propósito:** Implementar lógica de negocio
- **Componentes:**
  - `AuthService`: Registro, login, JWT
  - `CompanyService`: Gestión de empresas
  - `ProductService`: CRUD de productos
- **Responsabilidades:**
  - Validar reglas de negocio
  - Operaciones CRUD
  - Generación de tokens
  - Gestión de relaciones

### 4. **Middleware Layer** (Interceptores)
- **Propósito:** Interceptar y validar requests
- **Componentes:**
  - `AuthMiddleware`: Validación JWT
  - `token_required`: Decorador de autenticación
  - `company_access_required`: Validar acceso a empresa
  - `admin_required`: Validar rol de admin
- **Responsabilidades:**
  - Validar JWT
  - Verificar permisos
  - Inyectar contexto de usuario

### 5. **Controllers Layer** (Endpoints)
- **Propósito:** Exponer API REST
- **Componentes:**
  - `AuthController`: `/api/auth/*`
  - `CompanyController`: `/api/companies/*`
  - `ProductController`: `/api/companies/:id/productos/*`
- **Responsabilidades:**
  - Definir rutas HTTP
  - Validar input
  - Llamar services
  - Formatear response

### 6. **App Layer** (Inicialización)
- **Propósito:** Configurar y arrancar Flask
- **Componentes:**
  - `App.py`: Inicialización de Flask
  - Registro de blueprints
  - Configuración de CORS
  - Creación de tablas
- **Responsabilidades:**
  - Inicializar app
  - Registrar rutas
  - Configurar middleware

---

## 🎨 Frontend - Arquitectura SPA

### Estructura de Archivos

```
frontend/
├── index.html              # Landing page
├── pages/
│   ├── login.html         # Autenticación
│   ├── register.html      # Registro
│   ├── companies.html     # Gestión empresas
│   ├── dashboard.html     # Dashboard principal
│   └── profile.html       # Perfil usuario
├── css/
│   └── style.css          # Estilos globales
└── js/
    ├── config.js          # Configuración + utils
    ├── auth.js            # Login
    ├── register.js        # Registro
    ├── companies.js       # Empresas
    ├── dashboard.js       # Productos
    └── profile.js         # Perfil
```

### Módulos JavaScript

#### **config.js** - Configuración Central
- API base URL
- LocalStorage management
- JWT handling
- API request wrapper
- Alert system
- Navigation helpers

#### **auth.js** - Autenticación
- Login form handling
- JWT storage
- Redirect logic

#### **register.js** - Registro
- Registration form
- Password validation
- Account creation

#### **companies.js** - Gestión de Empresas
- Listar empresas
- Crear empresa
- Unirse a empresa
- Seleccionar empresa

#### **dashboard.js** - Dashboard
- Listar productos
- CRUD productos
- Ver empleados (admin)
- Gestión de modales

#### **profile.js** - Perfil
- Ver información de usuario
- Actualizar perfil
- Cambiar contraseña

---

## 🔐 Flujo de Autenticación

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. POST /api/auth/register o /login
     ▼
┌────────────────┐
│   Backend      │
│  AuthService   │ 2. Validate credentials
│                │ 3. Generate JWT (7 days)
└────┬───────────┘
     │ 4. Return token + user data
     ▼
┌──────────┐
│ Frontend │ 5. Store token in localStorage
│          │ 6. Store user data
└────┬─────┘
     │
     │ 7. Subsequent requests
     ▼
┌──────────────────┐
│  Backend         │
│  AuthMiddleware  │ 8. Validate JWT
│                  │ 9. Extract user_id
│                  │ 10. Inject into request
└──────────────────┘
```

---

## 🏢 Flujo Multi-Empresa

```
┌──────────┐
│  User    │ 1. Authenticated
└────┬─────┘
     │
     ├─── 2a. Create Company ────┐
     │    POST /api/companies    │
     │                           ▼
     │                    ┌──────────────┐
     │                    │   Backend    │
     │                    │ Generate code│
     │                    │ Set as admin │
     │                    └──────────────┘
     │
     └─── 2b. Join Company ──────┐
          POST /companies/join   │
          {unique_code}          ▼
                          ┌──────────────┐
                          │   Backend    │
                          │ Find company │
                          │ Add employee │
                          └──────────────┘
```

---

## 📦 Flujo de Gestión de Productos

```
┌─────────┐
│  User   │ Authenticated + Company Selected
└────┬────┘
     │
     │ 1. GET /api/companies/:id/productos
     ▼
┌────────────────┐
│    Backend     │ 2. Verify user in company
│ AuthMiddleware │ 3. Filter by company_id
└────┬───────────┘
     │ 4. Return products
     ▼
┌─────────┐
│Frontend │ Display in dashboard
└─────────┘

     │
     │ 5. Create/Update product
     ▼
┌────────────────┐
│    Backend     │ 6. Verify permissions
│                │ 7. Validate data
│                │ 8. Save to DB
└────────────────┘

     │
     │ 9. Delete product (Admin only)
     ▼
┌────────────────┐
│    Backend     │ 10. Verify admin role
│  admin_required│ 11. Delete from DB
└────────────────┘
```

---

## 🔒 Modelo de Seguridad

### Capas de Seguridad

1. **Autenticación (Who are you?)**
   - JWT tokens con expiración
   - Password hashing con Werkzeug
   - Token en header Authorization

2. **Autorización (What can you do?)**
   - Role-based access (admin/employee)
   - Company membership verification
   - Resource ownership checks

3. **Validación de Datos**
   - Input sanitization
   - Type checking
   - Required fields validation

4. **Aislamiento de Datos**
   - Company-based filtering
   - User-specific queries
   - No cross-company access

### Permisos por Rol

| Acción | Admin | Employee |
|--------|-------|----------|
| Ver productos | ✅ | ✅ |
| Crear productos | ✅ | ✅ |
| Editar productos | ✅ | ✅ |
| Eliminar productos | ✅ | ❌ |
| Ver empleados | ✅ | ❌ |
| Cambiar roles | ✅ | ❌ |
| Eliminar empleados | ✅ | ❌ |

---

## 📊 Modelo de Datos

### Relaciones

```
User ──< UserCompany >── Company
                           │
                           │
                           └──< Product
```

### User
```python
- id (PK)
- username (unique)
- email (unique)
- password_hash
- is_verified
- created_at
```

### Company
```python
- id (PK)
- name
- description
- unique_code (unique)
- created_by (FK → User)
- created_at
```

### UserCompany
```python
- id (PK)
- user_id (FK → User)
- company_id (FK → Company)
- role (admin/employee)
- joined_at
- UNIQUE(user_id, company_id)
```

### Product
```python
- id (PK)
- name
- description
- price
- quantity
- company_id (FK → Company)
- created_at
- updated_at
```

---

## 🚀 Tecnologías Utilizadas

### Backend
- **Framework:** Flask 2.0.3
- **ORM:** SQLAlchemy 1.4.25
- **Database:** MySQL (pymysql)
- **Auth:** PyJWT 2.3.0, Werkzeug
- **CORS:** Flask-CORS 3.0.10
- **Environment:** python-dotenv

### Frontend
- **HTML5:** Semantic markup
- **CSS3:** Variables, Flexbox, Grid
- **JavaScript:** ES6+, Fetch API
- **Storage:** localStorage

### Database
- **RDBMS:** MySQL
- **Hosting:** Railway (producción)

---

## 📈 Escalabilidad

### Backend
- **Horizontal:** Múltiples instancias Flask con load balancer
- **Vertical:** Optimización de queries, indexación BD
- **Caching:** Redis para sesiones y queries frecuentes
- **CDN:** Assets estáticos

### Database
- **Read Replicas:** Para distribución de carga
- **Partitioning:** Por company_id
- **Indexing:** En campos de búsqueda frecuente

### Frontend
- **CDN:** Distribución de assets
- **Lazy Loading:** Carga bajo demanda
- **Code Splitting:** Módulos separados
- **Service Workers:** Caching offline

---

## 🔄 Próximas Mejoras

### Funcionalidades
- [ ] Búsqueda y filtrado avanzado
- [ ] Exportación de reportes (PDF, Excel)
- [ ] Historial de cambios (audit log)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Dashboard analytics

### Técnicas
- [ ] Tests unitarios (pytest)
- [ ] Tests de integración
- [ ] CI/CD pipeline
- [ ] Docker containerization
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Rate limiting
- [ ] Request logging

---

Esta arquitectura proporciona una base sólida, escalable y mantenible para el sistema de gestión de inventario multi-empresa.
