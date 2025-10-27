#!/bin/bash

echo "🚀 Setup Script - Sistema de Gestión de Inventario"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3."
    exit 1
fi

echo "✅ Python 3 detectado"

# Create virtual environment
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Install dependencies
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "✅ ¡Instalación completada!"
echo ""
echo "Para ejecutar el backend:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ve a la carpeta backend: cd backend"
echo "  3. Ejecuta: python Main.py"
echo ""
echo "Para abrir el frontend:"
echo "  Abre frontend/index.html en tu navegador"
echo "  O ejecuta un servidor: cd frontend && python -m http.server 8000"
echo ""
