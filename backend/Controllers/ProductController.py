from flask import Blueprint, request, jsonify
from Services.ProductService import ProductService
from Middleware.AuthMiddleware import token_required
from Models.UserModel import UserCompany

product_bp = Blueprint('product_bp', __name__)

# Helper function to check company access
def check_company_access(user_id, company_id):
    """Check if user has access to the company"""
    user_company = UserCompany.query.filter_by(
        user_id=user_id,
        company_id=company_id
    ).first()
    return user_company

# Ruta GET: Obtener todos los productos de una empresa
@product_bp.route('/companies/<int:company_id>/productos', methods=['GET'])
@token_required
def get_products(current_user_id, current_user_email, company_id):
    """Get all products for a specific company"""
    # Check if user has access to this company
    if not check_company_access(current_user_id, company_id):
        return jsonify({"error": "Access denied to this company"}), 403
    
    products = ProductService.get_all_products(company_id)
    return jsonify([product.to_dict() for product in products])

# Ruta GET: Obtener un producto por ID
@product_bp.route('/companies/<int:company_id>/productos/<int:id>', methods=['GET'])
@token_required
def get_product(current_user_id, current_user_email, company_id, id):
    """Get a specific product by ID"""
    # Check if user has access to this company
    if not check_company_access(current_user_id, company_id):
        return jsonify({"error": "Access denied to this company"}), 403
    
    product = ProductService.get_product_by_id(id, company_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Producto no encontrado"}), 404

# Ruta POST: Crear un nuevo producto
@product_bp.route('/companies/<int:company_id>/productos', methods=['POST'])
@token_required
def create_product(current_user_id, current_user_email, company_id):
    """Create a new product"""
    # Check if user has access to this company
    user_company = check_company_access(current_user_id, company_id)
    if not user_company:
        return jsonify({"error": "Access denied to this company"}), 403
    
    # Only admins can create products (optional - remove if employees should also create)
    # if user_company.role != 'admin':
    #     return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    new_product = ProductService.create_product(data, company_id)
    return jsonify(new_product.to_dict()), 201

# Ruta PUT/PATCH: Actualizar un producto
@product_bp.route('/companies/<int:company_id>/productos/<int:id>', methods=['PUT'])
@token_required
def update_product(current_user_id, current_user_email, company_id, id):
    """Update a product"""
    # Check if user has access to this company
    user_company = check_company_access(current_user_id, company_id)
    if not user_company:
        return jsonify({"error": "Access denied to this company"}), 403
    
    # Only admins can update products (optional)
    # if user_company.role != 'admin':
    #     return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    updated_product = ProductService.update_product(id, data, company_id)
    if updated_product:
        return jsonify(updated_product.to_dict())
    return jsonify({"error": "Producto no encontrado"}), 404

# Ruta DELETE: Eliminar un producto
@product_bp.route('/companies/<int:company_id>/productos/<int:id>', methods=['DELETE'])
@token_required
def delete_product(current_user_id, current_user_email, company_id, id):
    """Delete a product"""
    # Check if user has access to this company
    user_company = check_company_access(current_user_id, company_id)
    if not user_company:
        return jsonify({"error": "Access denied to this company"}), 403
    
    # Only admins can delete products
    if user_company.role != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    if ProductService.delete_product(id, company_id):
        return jsonify({"message": "Producto eliminado"})
    return jsonify({"error": "Producto no encontrado"}), 404
