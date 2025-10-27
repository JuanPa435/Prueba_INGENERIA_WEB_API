from functools import wraps
from flask import request, jsonify
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode the token
            secret_key = os.getenv('SECRET_KEY', 'mysecretkey')
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user_email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        # Pass the current user info to the route
        return f(current_user_id=current_user_id, current_user_email=current_user_email, *args, **kwargs)
    
    return decorated


def company_access_required(f):
    """Decorator to ensure user has access to a specific company"""
    @wraps(f)
    def decorated(current_user_id, *args, **kwargs):
        from Models.UserModel import UserCompany
        
        # Get company_id from kwargs or request
        company_id = kwargs.get('company_id') or request.json.get('company_id')
        
        if not company_id:
            return jsonify({'error': 'Company ID is required'}), 400
        
        # Check if user belongs to this company
        user_company = UserCompany.query.filter_by(
            user_id=current_user_id,
            company_id=company_id
        ).first()
        
        if not user_company:
            return jsonify({'error': 'Access denied to this company'}), 403
        
        # Pass the user's role to the route
        kwargs['user_role'] = user_company.role
        return f(current_user_id=current_user_id, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """Decorator to ensure user is an admin of the company"""
    @wraps(f)
    def decorated(current_user_id, user_role=None, *args, **kwargs):
        if user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(current_user_id=current_user_id, user_role=user_role, *args, **kwargs)
    
    return decorated
