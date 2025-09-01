
from flask import Blueprint, request, jsonify
from services.band_service import BandService
band_bp =Blueprint('band_bp',__name__)

# Importar la sesión de la base de datos desde config/database.py
from config.database import get_db_session

# Instancia global de servicio (en producción usar contexto de app o request)
service = BandService(get_db_session())

band_bp =Blueprint('band_bp',__name__)


@band_bp.route('/bands', methods=['GET'])
def get_bands():
	bands = service.listar_bandas()
	return jsonify([{'id': b.id, 'name': b.name} for b in bands]), 200



@band_bp.route('/bands/<int:band_id>', methods=['GET'])
def get_band(band_id):
	band = service.obtener_banda(band_id)
	if band:
		return jsonify({'id': band.id, 'name': band.name}), 200
	return jsonify({'error': 'Banda no encontrada'}), 404



@band_bp.route('/bands', methods=['POST'])
def create_band():
	data = request.get_json()
	name = data.get('name')
	if not name:
		return jsonify({'error': 'El nombre es obligatorio'}), 400
	band = service.crear_banda(name)
	return jsonify({'id': band.id, 'name': band.name}), 201



@band_bp.route('/bands/<int:band_id>', methods=['PUT'])
def update_band(band_id):
	data = request.get_json()
	name = data.get('name')
	band = service.actualizar_banda(band_id, name)
	if band:
		return jsonify({'id': band.id, 'name': band.name}), 200
	return jsonify({'error': 'Banda no encontrada'}), 404



@band_bp.route('/bands/<int:band_id>', methods=['DELETE'])
def delete_band(band_id):
	band = service.eliminar_banda(band_id)
	if band:
		return jsonify({'message': 'Banda eliminada'}), 200
	return jsonify({'error': 'Banda no encontrada'}), 404
