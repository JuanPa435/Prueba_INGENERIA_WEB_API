# Prueba_INGENERIA_WEB_API
# Proyecto de Gestión de Productos

Este proyecto es una base para la gestión de productos de un inventario o tienda, implementado siguiendo el **patrón arquitectónico por capas**. Utiliza **Python**, **Flask** como framework web y **SQLAlchemy** como ORM para la interacción con bases de datos relacionales.

---

## 💡 Funcionalidades principales

- Crear productos con información básica: nombre, descripción, precio y cantidad.
- Listar todos los productos existentes.
- Consultar un producto por su ID.
- Actualizar la información de un producto.
- Eliminar un producto.
- Gestión segura de la base de datos utilizando SQLAlchemy y variables de entorno para las credenciales.

---

## 🏗 Estructura del Proyecto

```
/project-root
│
├── /Config
│   └── Config.py              # Configuración general de la app (DB, rutas, variables de entorno)
│
├── /Controllers
│   └── ProductController.py   # Controlador que define los endpoints de la API
│
├── /Models
│   └── ProductModel.py        # Modelo ORM para la tabla de productos
│
├── /Services
│   └── ProductService.py      # Lógica de negocio para productos (CRUD)
│
├── /Src
│   └── App.py                 # Inicialización de la app y registro de rutas
│
├── Main.py                    # Punto de entrada para ejecutar la aplicación
├── requirements.txt           # Dependencias necesarias para ejecutar el proyecto
├── .gitignore                 # Archivos y carpetas a ignorar en Git
└── README.md                  # Documentación del proyecto
```

---

## ⚙ Instalación para uso

1. Clonar el repositorio
2. Crear y activar un entorno virtual:


-- Instala virtualenv si no lo tienes:

```bash
pip install virtualenv
```

-- Crea el entorno virtual:

```bash
python -m venv venv
```

-- Activa el entorno virtual:

* **En Linux/Mac**:

```bash
source venv/bin/activate
```

* **En Windows**:

```bash
venv\Scripts\activate
```

-- Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## Importancia de usar un entorno virtual

* **Aislamiento:** Evita conflictos entre dependencias de diferentes proyectos.
* **Reproducibilidad:** Permite que otros desarrolladores instalen exactamente las mismas versiones de las librerías.
* **Facilidad de despliegue:** Simplifica la migración y despliegue en diferentes entornos (desarrollo, pruebas, producción).
* **Limpieza:** Mantiene tu instalación global de Python libre de paquetes innecesarios.

---

## 💻 Ejecución de la aplicación

Para ejecutar la aplicación localmente:

```bash
python Main.py
```

La API estará disponible en:

```
http://127.0.0.1:5000
```

## 💻 Ejemplos de uso con curl

Crear producto

```bash
curl -X POST http://127.0.0.1:5000/productos \
-H "Content-Type: application/json" \
-d '{
  "name": "Papas fritas",
  "description": "Comida sabrosa",
  "price": 100000,
  "quantity": 5000
}'
```

Actualizar producto

```bash
curl -X PUT http://127.0.0.1:5000/productos/1 \
-H "Content-Type: application/json" \
-d '{
  "name": "Papas a la francesa",
  "description": "Deliciosas y crujientes",
  "price": 120000,
  "quantity": 4500
}'
```

Eliminar producto

```bash
curl -X DELETE http://127.0.0.1:5000/productos/1
```

Listar productos

```bash
curl http://127.0.0.1:5000/productos
```

---

## Endpoints principales

| Método | Endpoint        | Descripción                      |
| ------ | --------------- | -------------------------------- |
| GET    | /productos      | Listar todos los productos       |
| GET    | /productos/<id> | Obtener un producto por ID       |
| POST   | /productos      | Crear un nuevo producto          |
| PUT    | /productos/<id> | Actualizar un producto existente |
| DELETE | /productos/<id> | Eliminar un producto             |

---

## Licencia

Este proyecto es de uso libre para fines educativos y de aprendizaje.

---


