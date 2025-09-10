from flask import Blueprint, request, jsonify
from Services.ProductService import ProductService

product_bp = Blueprint('product_bp', __name__)

# Ruta GET: Obtener todos los productos
@product_bp.route('/productos', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    return jsonify([product.to_dict() for product in products])

# Ruta GET: Obtener un producto por ID
@product_bp.route('/productos/<int:id>', methods=['GET'])
def get_product(id):
    product = ProductService.get_product_by_id(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Producto no encontrado"}), 404

# Ruta POST: Crear un nuevo producto
@product_bp.route('/productos', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = ProductService.create_product(data)
    return jsonify(new_product.to_dict()), 201

# Ruta PUT/PATCH: Actualizar un producto
@product_bp.route('/productos/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    updated_product = ProductService.update_product(id, data)
    if updated_product:
        return jsonify(updated_product.to_dict())
    return jsonify({"error": "Producto no encontrado"}), 404

# Ruta DELETE: Eliminar un producto
@product_bp.route('/productos/<int:id>', methods=['DELETE'])
def delete_product(id):
    if ProductService.delete_product(id):
        return jsonify({"message": "Producto eliminado"})
    return jsonify({"error": "Producto no encontrado"}), 404
