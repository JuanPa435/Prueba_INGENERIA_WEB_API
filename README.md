# Sistema de Gestión de Inventario

Sistema completo de gestión de inventario con autenticación JWT, multi-empresa y control de roles (Administrador/Empleado).

---

## 🌟 Características

### Backend (Python/Flask)
- ✅ **Autenticación JWT**: Sistema seguro de registro e inicio de sesión
- ✅ **Multi-Empresa**: Soporte para múltiples empresas con inventarios separados
- ✅ **Roles de Usuario**: Administrador y Empleado con permisos diferenciados
- ✅ **API RESTful**: Endpoints bien estructurados y documentados
- ✅ **Base de Datos**: MySQL con SQLAlchemy ORM
- ✅ **Arquitectura por Capas**: Config, Models, Services, Controllers, Middleware
- ✅ **CORS**: Habilitado para integración con frontend

### Frontend (HTML/CSS/JavaScript)
- ✅ **Página de Inicio**: Presentación atractiva de la aplicación
- ✅ **Registro/Login**: Formularios de autenticación con validación
- ✅ **Gestión de Empresas**: Crear o unirse a empresas existentes
- ✅ **Dashboard**: Interfaz completa para gestión de productos
- ✅ **Panel de Admin**: Visualización y gestión de empleados
- ✅ **Diseño Responsive**: Compatible con dispositivos móviles
- ✅ **JWT Storage**: Manejo seguro de tokens en localStorage

---

## 📁 Estructura del Proyecto

```
/
├── backend/                    # Backend en Python/Flask
│   ├── Config/
│   │   └── Config.py          # Configuración de la app
│   ├── Controllers/
│   │   ├── AuthController.py  # Endpoints de autenticación
│   │   ├── CompanyController.py # Endpoints de empresas
│   │   └── ProductController.py # Endpoints de productos
│   ├── Models/
│   │   └── UserModel.py       # Modelos de BD (User, Company, Product, UserCompany)
│   ├── Services/
│   │   ├── AuthService.py     # Lógica de autenticación
│   │   ├── CompanyService.py  # Lógica de empresas
│   │   └── ProductService.py  # Lógica de productos
│   ├── Middleware/
│   │   └── AuthMiddleware.py  # Middleware de JWT
│   ├── Src/
│   │   └── App.py            # Inicialización de Flask
│   ├── Main.py               # Punto de entrada
│   └── .env                  # Variables de entorno
├── frontend/                  # Frontend en HTML/CSS/JS
│   ├── css/
│   │   └── style.css         # Estilos globales
│   ├── js/
│   │   ├── config.js         # Configuración y utilidades
│   │   ├── auth.js           # Lógica de login
│   │   ├── register.js       # Lógica de registro
│   │   ├── companies.js      # Lógica de empresas
│   │   └── dashboard.js      # Lógica del dashboard
│   ├── pages/
│   │   ├── login.html        # Página de login
│   │   ├── register.html     # Página de registro
│   │   ├── companies.html    # Gestión de empresas
│   │   └── dashboard.html    # Dashboard principal
│   └── index.html            # Página de inicio
├── requirements.txt          # Dependencias de Python
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

---

## ⚙️ Instalación

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd Prueba_INGENERIA_WEB_API
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
```

### 3. Activar Entorno Virtual

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Crear/editar el archivo `backend/.env`:

```env
DATABASE_URL=mysql://usuario:contraseña@host:puerto/base_de_datos
SECRET_KEY=tu_clave_secreta_aqui
JWT_SECRET_KEY=tu_clave_jwt_aqui
```

---

## 🚀 Ejecución

### Backend

```bash
cd backend
python Main.py
```

El backend estará disponible en: `http://127.0.0.1:5000`

### Frontend

Abrir `frontend/index.html` en un navegador web o usar un servidor local:

```bash
cd frontend
python -m http.server 8000
```

Luego visitar: `http://localhost:8000`

**Nota:** Si usas un servidor diferente, actualiza `API_BASE_URL` en `frontend/js/config.js`

---

## 📚 API Endpoints

### Autenticación (`/api/auth`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/register` | Registrar nuevo usuario | No |
| POST | `/login` | Iniciar sesión | No |
| GET | `/profile` | Obtener perfil de usuario | Sí (JWT) |
| PUT | `/profile` | Actualizar perfil | Sí (JWT) |

### Empresas (`/api/companies`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/` | Crear nueva empresa | Sí (JWT) |
| POST | `/join` | Unirse a empresa | Sí (JWT) |
| GET | `/` | Listar empresas del usuario | Sí (JWT) |
| GET | `/:id` | Obtener detalles de empresa | Sí (JWT) |
| GET | `/:id/employees` | Listar empleados (admin) | Sí (JWT + Admin) |
| PUT | `/:id/employees/:emp_id/role` | Cambiar rol (admin) | Sí (JWT + Admin) |
| DELETE | `/:id/employees/:emp_id` | Eliminar empleado (admin) | Sí (JWT + Admin) |

### Productos (`/api/companies/:company_id/productos`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| GET | `/` | Listar productos | Sí (JWT) |
| GET | `/:id` | Obtener producto | Sí (JWT) |
| POST | `/` | Crear producto | Sí (JWT) |
| PUT | `/:id` | Actualizar producto | Sí (JWT) |
| DELETE | `/:id` | Eliminar producto | Sí (JWT + Admin) |

---

## 💡 Uso del Sistema

### 1. Registro de Usuario
- Acceder a la página de registro
- Completar: username, email, contraseña
- El sistema crea la cuenta y genera un token JWT

### 2. Gestión de Empresas
- **Crear Empresa**: Ingresar nombre y descripción. Se genera un código único.
- **Unirse a Empresa**: Usar el código único de una empresa existente.

### 3. Roles
- **Administrador**: 
  - Crear/editar/eliminar productos
  - Ver y gestionar empleados
  - Cambiar roles de empleados
  - Eliminar empleados
  
- **Empleado**:
  - Ver productos
  - Crear/editar productos
  - Ver otros empleados

### 4. Gestión de Inventario
- Agregar productos con nombre, descripción, precio y cantidad
- Editar productos existentes
- Eliminar productos (solo admin)
- Visualizar lista completa de productos

---

## 🔒 Seguridad

- **JWT**: Tokens con expiración de 7 días
- **Contraseñas**: Hasheadas con Werkzeug
- **Autenticación**: Middleware que valida JWT en todas las rutas protegidas
- **CORS**: Configurado para permitir requests del frontend
- **Roles**: Control de acceso basado en roles

---

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.12
- Flask 2.0.3
- Flask-SQLAlchemy 2.5.1
- Flask-JWT-Extended 4.3.1
- Flask-Bcrypt 1.0.1
- Flask-CORS 3.0.10
- PyMySQL 1.0.2
- SQLAlchemy 1.4.25

### Frontend
- HTML5
- CSS3 (Variables CSS, Flexbox, Grid)
- JavaScript (ES6+)
- Fetch API para requests

### Base de Datos
- MySQL (Railway en producción)

---

## 📝 Ejemplos de Uso con curl

### Registrar Usuario
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "juan",
  "email": "juan@example.com",
  "password": "password123"
}'
```

### Iniciar Sesión
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username_or_email": "juan",
  "password": "password123"
}'
```

### Crear Empresa
```bash
curl -X POST http://127.0.0.1:5000/api/companies \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <tu_token_jwt>" \
-d '{
  "name": "Mi Empresa",
  "description": "Descripción de mi empresa"
}'
```

### Crear Producto
```bash
curl -X POST http://127.0.0.1:5000/api/companies/1/productos \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <tu_token_jwt>" \
-d '{
  "name": "Laptop",
  "description": "Laptop Dell XPS 15",
  "price": 1500.00,
  "quantity": 10
}'
```

---

## 🐛 Solución de Problemas

### Error de Conexión a la Base de Datos
- Verificar que MySQL esté ejecutándose
- Revisar credenciales en `backend/.env`
- Asegurar que la base de datos existe

### Error 401 (No autorizado)
- Verificar que el token JWT sea válido
- El token podría haber expirado (7 días)
- Volver a iniciar sesión

### CORS Errors
- Verificar que Flask-CORS esté instalado
- Confirmar que el backend esté en `http://127.0.0.1:5000`
- Actualizar `API_BASE_URL` en `frontend/js/config.js`

---

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y de aprendizaje.

---

## 👥 Autor

Sistema desarrollado para demostración de arquitectura moderna de aplicaciones web con Python Flask.

---

## 🔄 Próximas Mejoras

- [ ] Envío real de emails de verificación
- [ ] Recuperación de contraseña
- [ ] Búsqueda y filtrado de productos
- [ ] Exportación de reportes
- [ ] Historial de cambios
- [ ] Notificaciones en tiempo real
- [ ] Tests unitarios y de integración
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

¡Gracias por usar el Sistema de Gestión de Inventario! 🎉

