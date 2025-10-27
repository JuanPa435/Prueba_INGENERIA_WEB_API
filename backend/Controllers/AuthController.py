from flask import Blueprint, request, jsonify
from Services.AuthService import AuthService
from Middleware.AuthMiddleware import token_required

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    result, status_code = AuthService.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    return jsonify(result), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with username/email and password"""
    data = request.get_json()
    
    if not data or not data.get('username_or_email') or not data.get('password'):
        return jsonify({'error': 'Username/email and password are required'}), 400
    
    result, status_code = AuthService.login_user(
        username_or_email=data['username_or_email'],
        password=data['password']
    )
    
    return jsonify(result), status_code


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user_id, current_user_email):
    """Get current user profile"""
    result, status_code = AuthService.get_user_by_id(current_user_id)
    return jsonify(result), status_code


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user_id, current_user_email):
    """Update current user profile"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    result, status_code = AuthService.update_user_profile(current_user_id, data)
    return jsonify(result), status_code


@auth_bp.route('/verify-email/<int:user_id>', methods=['POST'])
def verify_email(user_id):
    """Verify user email (simplified - normally would use a token)"""
    result, status_code = AuthService.verify_email(user_id)
    return jsonify(result), status_code
