# Guía de Pruebas - Sistema de Gestión de Inventario

## 🧪 Guía Completa de Pruebas

Esta guía describe cómo probar todas las funcionalidades del sistema.

---

## Prerrequisitos

1. Backend ejecutándose en `http://127.0.0.1:5000`
2. Frontend accesible (abrir `frontend/index.html` o en servidor local)
3. Base de datos MySQL configurada y accesible

---

## 🔐 Pruebas de Autenticación

### 1. Registro de Usuario

**Interfaz Web:**
1. Ir a `frontend/index.html`
2. Click en "Registrarse"
3. Completar formulario:
   - Usuario: `testuser`
   - Email: `test@example.com`
   - Contraseña: `password123`
   - Confirmar contraseña: `password123`
4. Click "Registrarse"
5. Verificar que se muestra mensaje de éxito
6. Verificar redirección a página de empresas

**API (curl):**
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}'
```

**Resultado Esperado:**
```json
{
  "message": "User registered successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2024-10-27T19:00:00",
    "is_verified": true
  }
}
```

### 2. Inicio de Sesión

**Interfaz Web:**
1. Ir a `frontend/pages/login.html`
2. Completar:
   - Usuario/Email: `testuser` o `test@example.com`
   - Contraseña: `password123`
3. Click "Iniciar Sesión"
4. Verificar redirección a página de empresas

**API (curl):**
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username_or_email": "testuser",
  "password": "password123"
}'
```

### 3. Obtener Perfil

**API (curl):**
```bash
# Reemplazar <TOKEN> con el token recibido al iniciar sesión
curl -X GET http://127.0.0.1:5000/api/auth/profile \
-H "Authorization: Bearer <TOKEN>"
```

---

## 🏢 Pruebas de Empresas

### 1. Crear Empresa

**Interfaz Web:**
1. Iniciar sesión
2. En página de empresas, sección "Crear Nueva Empresa"
3. Completar:
   - Nombre: `Mi Empresa S.A.`
   - Descripción: `Empresa de prueba`
4. Click "Crear Empresa"
5. Verificar mensaje con código único (ej: `ABC12345`)

**API (curl):**
```bash
curl -X POST http://127.0.0.1:5000/api/companies \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
  "name": "Mi Empresa S.A.",
  "description": "Empresa de prueba"
}'
```

### 2. Unirse a Empresa

**Interfaz Web:**
1. Usuario 2: Registrarse con otra cuenta
2. En página de empresas, sección "Unirse a Empresa Existente"
3. Ingresar código único de empresa creada
4. Click "Unirse"

**API (curl):**
```bash
curl -X POST http://127.0.0.1:5000/api/companies/join \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN_USUARIO_2>" \
-d '{
  "unique_code": "ABC12345"
}'
```

### 3. Listar Empresas del Usuario

**API (curl):**
```bash
curl -X GET http://127.0.0.1:5000/api/companies \
-H "Authorization: Bearer <TOKEN>"
```

### 4. Ver Empleados (Admin)

**Interfaz Web:**
1. Entrar al dashboard de una empresa
2. Click en "Ver Empleados" (solo visible para admin)

**API (curl):**
```bash
curl -X GET http://127.0.0.1:5000/api/companies/1/employees \
-H "Authorization: Bearer <TOKEN_ADMIN>"
```

---

## 📦 Pruebas de Productos

### 1. Crear Producto

**Interfaz Web:**
1. Seleccionar una empresa (click en card)
2. En dashboard, click "+ Agregar Producto"
3. Completar formulario:
   - Nombre: `Laptop Dell XPS 15`
   - Descripción: `Laptop de alto rendimiento`
   - Precio: `1500.00`
   - Cantidad: `10`
4. Click "Guardar"

**API (curl):**
```bash
curl -X POST http://127.0.0.1:5000/api/companies/1/productos \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
  "name": "Laptop Dell XPS 15",
  "description": "Laptop de alto rendimiento",
  "price": 1500.00,
  "quantity": 10
}'
```

### 2. Listar Productos

**Interfaz Web:**
- Los productos se muestran automáticamente en el dashboard

**API (curl):**
```bash
curl -X GET http://127.0.0.1:5000/api/companies/1/productos \
-H "Authorization: Bearer <TOKEN>"
```

### 3. Actualizar Producto

**Interfaz Web:**
1. Click en botón "✏️" junto al producto
2. Modificar campos
3. Click "Guardar"

**API (curl):**
```bash
curl -X PUT http://127.0.0.1:5000/api/companies/1/productos/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <TOKEN>" \
-d '{
  "name": "Laptop Dell XPS 15 (Actualizado)",
  "description": "Nueva descripción",
  "price": 1600.00,
  "quantity": 8
}'
```

### 4. Eliminar Producto (Admin)

**Interfaz Web:**
1. Como admin, click en botón "🗑️" junto al producto
2. Confirmar eliminación

**API (curl):**
```bash
curl -X DELETE http://127.0.0.1:5000/api/companies/1/productos/1 \
-H "Authorization: Bearer <TOKEN_ADMIN>"
```

---

## 🔒 Pruebas de Seguridad

### 1. Acceso sin JWT
```bash
# Debe retornar 401 Unauthorized
curl -X GET http://127.0.0.1:5000/api/companies
```

### 2. JWT Inválido
```bash
# Debe retornar 401 Invalid Token
curl -X GET http://127.0.0.1:5000/api/companies \
-H "Authorization: Bearer token_invalido"
```

### 3. Acceso a Empresa sin Permisos
```bash
# Usuario 1 intenta acceder a productos de empresa donde no está
curl -X GET http://127.0.0.1:5000/api/companies/999/productos \
-H "Authorization: Bearer <TOKEN_USUARIO_1>"
```

### 4. Empleado Intentando Eliminar (sin permisos)
```bash
# Debe retornar 403 Forbidden
curl -X DELETE http://127.0.0.1:5000/api/companies/1/productos/1 \
-H "Authorization: Bearer <TOKEN_EMPLEADO>"
```

---

## 🎭 Casos de Prueba Completos

### Escenario 1: Usuario Nuevo Completo

1. **Registrarse** → Éxito
2. **Crear empresa "TechCorp"** → Código `TECH1234`, rol: admin
3. **Crear 3 productos** → Todos creados
4. **Ver empleados** → Solo el creador
5. **Cerrar sesión** → Token removido

### Escenario 2: Empleado se Une

1. **Usuario 2 se registra** → Éxito
2. **Se une con código** `TECH1234` → rol: employee
3. **Ver productos** → Ve los 3 productos
4. **Crear producto** → Éxito
5. **Intentar eliminar** → 403 Forbidden (sin permisos)
6. **Ver empleados** → 403 Forbidden (solo admin)

### Escenario 3: Multi-Empresa

1. **Usuario 1 crea "CompanyA"** → Código `COMPA123`
2. **Usuario 1 crea "CompanyB"** → Código `COMPB456`
3. **En CompanyA: crear producto P1**
4. **En CompanyB: crear producto P2**
5. **Verificar aislamiento**: P1 solo en CompanyA, P2 solo en CompanyB

### Escenario 4: Gestión de Empleados (Admin)

1. **Admin ve lista de empleados** → Éxito
2. **Empleado intenta ver lista** → 403 Forbidden
3. **Admin intenta cambiar rol** → Éxito (cuando implementado)
4. **Admin intenta eliminar empleado** → Éxito (cuando implementado)

---

## ✅ Checklist de Validación

- [ ] Registro exitoso crea usuario y retorna JWT
- [ ] Login con username funciona
- [ ] Login con email funciona
- [ ] JWT inválido es rechazado
- [ ] Sin JWT redirige a login
- [ ] Crear empresa genera código único
- [ ] Creador de empresa es admin
- [ ] Unirse con código añade como employee
- [ ] Productos están aislados por empresa
- [ ] Admin puede eliminar productos
- [ ] Employee no puede eliminar productos
- [ ] Admin puede ver empleados
- [ ] Employee no puede ver empleados
- [ ] Frontend redirige correctamente según auth
- [ ] LocalStorage maneja JWT correctamente
- [ ] Logout limpia toda la sesión

---

## 🐛 Errores Comunes

### Backend no inicia
- Verificar MySQL está ejecutándose
- Revisar credenciales en `.env`
- Verificar todas las dependencias instaladas

### CORS Error
- Verificar Flask-CORS instalado
- Confirmar backend en `http://127.0.0.1:5000`

### 401 Unauthorized
- Token expirado (7 días)
- Token no incluido en header
- Formato incorrecto: debe ser `Bearer <token>`

### 403 Forbidden
- Usuario no tiene rol adecuado
- Usuario no pertenece a la empresa

---

## 📊 Resultados Esperados

Al completar todas las pruebas:
- ✅ Autenticación completa funcional
- ✅ Gestión de empresas operativa
- ✅ Productos aislados por empresa
- ✅ Roles funcionando correctamente
- ✅ Frontend integrado con backend
- ✅ Seguridad JWT implementada

---

¡Éxito en las pruebas! 🎉
