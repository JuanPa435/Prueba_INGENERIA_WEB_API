from flask import Blueprint, request, jsonify
from Services.CompanyService import CompanyService
from Middleware.AuthMiddleware import token_required

company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/companies', methods=['POST'])
@token_required
def create_company(current_user_id, current_user_email):
    """Create a new company"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Company name is required'}), 400
    
    result, status_code = CompanyService.create_company(
        name=data['name'],
        description=data.get('description', ''),
        created_by_user_id=current_user_id
    )
    
    return jsonify(result), status_code


@company_bp.route('/companies/join', methods=['POST'])
@token_required
def join_company(current_user_id, current_user_email):
    """Join an existing company using unique code"""
    data = request.get_json()
    
    if not data or not data.get('unique_code'):
        return jsonify({'error': 'Unique code is required'}), 400
    
    result, status_code = CompanyService.join_company(
        unique_code=data['unique_code'],
        user_id=current_user_id
    )
    
    return jsonify(result), status_code


@company_bp.route('/companies', methods=['GET'])
@token_required
def get_user_companies(current_user_id, current_user_email):
    """Get all companies the user belongs to"""
    result, status_code = CompanyService.get_user_companies(current_user_id)
    return jsonify(result), status_code


@company_bp.route('/companies/<int:company_id>', methods=['GET'])
@token_required
def get_company(current_user_id, current_user_email, company_id):
    """Get company details"""
    result, status_code = CompanyService.get_company_by_id(company_id, current_user_id)
    return jsonify(result), status_code


@company_bp.route('/companies/<int:company_id>/employees', methods=['GET'])
@token_required
def get_company_employees(current_user_id, current_user_email, company_id):
    """Get all employees of a company (admin only)"""
    result, status_code = CompanyService.get_company_employees(company_id, current_user_id)
    return jsonify(result), status_code


@company_bp.route('/companies/<int:company_id>/employees/<int:employee_id>/role', methods=['PUT'])
@token_required
def update_employee_role(current_user_id, current_user_email, company_id, employee_id):
    """Update employee role (admin only)"""
    data = request.get_json()
    
    if not data or not data.get('role'):
        return jsonify({'error': 'Role is required'}), 400
    
    if data['role'] not in ['admin', 'employee']:
        return jsonify({'error': 'Invalid role. Must be "admin" or "employee"'}), 400
    
    result, status_code = CompanyService.update_employee_role(
        company_id=company_id,
        employee_id=employee_id,
        new_role=data['role'],
        admin_user_id=current_user_id
    )
    
    return jsonify(result), status_code


@company_bp.route('/companies/<int:company_id>/employees/<int:employee_id>', methods=['DELETE'])
@token_required
def remove_employee(current_user_id, current_user_email, company_id, employee_id):
    """Remove employee from company (admin only)"""
    result, status_code = CompanyService.remove_employee(
        company_id=company_id,
        employee_id=employee_id,
        admin_user_id=current_user_id
    )
    
    return jsonify(result), status_code
