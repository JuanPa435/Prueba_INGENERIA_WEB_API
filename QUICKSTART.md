# 🚀 Inicio Rápido - Sistema de Gestión de Inventario

## Configuración en 5 Minutos

### Paso 1: Requisitos Previos

Asegúrate de tener instalado:
- Python 3.8 o superior
- MySQL Server
- Un navegador web moderno

### Paso 2: Clonar el Repositorio

```bash
git clone <repository-url>
cd Prueba_INGENERIA_WEB_API
```

### Paso 3: Configurar el Backend

#### Opción A: Script Automático (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

#### Opción B: Manual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos

Editar `backend/.env`:

```env
DATABASE_URL=mysql://usuario:contraseña@localhost:3306/nombre_base_datos
SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=tu_clave_jwt
```

**O usar la base de datos de prueba ya configurada en el archivo .env**

### Paso 5: Ejecutar el Backend

```bash
cd backend
python Main.py
```

El backend estará en: `http://127.0.0.1:5000`

### Paso 6: Abrir el Frontend

#### Opción A: Abrir Directamente
Abrir `frontend/index.html` en el navegador

#### Opción B: Servidor Local
```bash
cd frontend
python -m http.server 8000
```
Luego ir a: `http://localhost:8000`

---

## 🎯 Primer Uso

### 1. Registrar Usuario
1. Click en "Registrarse" en la página principal
2. Completar datos: username, email, contraseña
3. Click "Registrarse"

### 2. Crear Empresa
1. Después del registro, serás redirigido a la página de empresas
2. En "Crear Nueva Empresa":
   - Nombre: `Mi Primera Empresa`
   - Descripción: `Prueba inicial`
3. Click "Crear Empresa"
4. **Guardar el código único** generado (ej: `ABC12345`)

### 3. Ver Dashboard
1. Click en la card de la empresa creada
2. Verás el dashboard con inventario vacío

### 4. Agregar Primer Producto
1. Click "+ Agregar Producto"
2. Completar:
   - Nombre: `Producto de Prueba`
   - Descripción: `Mi primer producto`
   - Precio: `100.00`
   - Cantidad: `10`
3. Click "Guardar"
4. El producto aparecerá en la tabla

### 5. Invitar Otro Usuario
1. Otro usuario debe registrarse
2. En su página de empresas, usar "Unirse a Empresa Existente"
3. Ingresar el código único: `ABC12345`
4. Ahora ambos pueden ver los mismos productos

---

## 🎓 Tutoriales Adicionales

### Cambiar entre Empresas
1. Click en "🏢 Empresas" en la barra de navegación
2. Seleccionar la empresa deseada

### Ver Empleados (Solo Admin)
1. En el dashboard, click "Ver Empleados"
2. Se mostrará lista de todos los miembros

### Editar Producto
1. Click en botón "✏️" junto al producto
2. Modificar campos necesarios
3. Click "Guardar"

### Eliminar Producto (Solo Admin)
1. Click en botón "🗑️" junto al producto
2. Confirmar eliminación

---

## 📱 Atajos de Teclado

- En formularios: `Enter` para enviar
- En modales: `Esc` para cerrar (próximamente)

---

## ⚠️ Solución de Problemas Comunes

### "Cannot connect to MySQL server"
**Solución:** Verificar que MySQL esté ejecutándose
```bash
# Linux/Mac
sudo service mysql start

# Windows
net start MySQL
```

### "Token is missing" en API
**Solución:** Iniciar sesión nuevamente desde el frontend

### "Access denied to this company"
**Solución:** Asegurarse de pertenecer a la empresa (crear o unirse)

### CORS Error
**Solución:** 
1. Verificar que el backend esté en `http://127.0.0.1:5000`
2. Si usas otro puerto, actualizar `API_BASE_URL` en `frontend/js/config.js`

---

## 📞 Ayuda

Para más detalles:
- Ver `README.md` - Documentación completa
- Ver `TESTING.md` - Guía de pruebas
- Revisar endpoints en: `http://127.0.0.1:5000/` (root de API)

---

## 🎉 ¡Listo!

Ya tienes el sistema funcionando. Explora todas las características y disfruta gestionando tu inventario.

**Próximos pasos:**
- Agregar más productos
- Invitar colaboradores
- Explorar el panel de admin
- Gestionar múltiples empresas

---

**Nota:** Este es un proyecto educativo. Para uso en producción, considera:
- Usar variables de entorno seguras
- Implementar HTTPS
- Agregar más validaciones
- Implementar backups de BD
- Agregar logging robusto
