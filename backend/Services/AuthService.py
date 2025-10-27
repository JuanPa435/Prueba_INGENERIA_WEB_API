from Models.UserModel import db, User
import jwt
import os
from datetime import datetime, timedelta

class AuthService:
    
    @staticmethod
    def register_user(username, email, password):
        """Register a new user"""
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 400
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            is_verified=True  # Auto-verify for now (simplified email verification)
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = AuthService.generate_token(new_user)
        
        return {
            'message': 'User registered successfully',
            'token': token,
            'user': new_user.to_dict()
        }, 201
    
    @staticmethod
    def login_user(username_or_email, password):
        """Login user with username/email and password"""
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        if not user.check_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # Generate token
        token = AuthService.generate_token(user)
        
        return {
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def generate_token(user):
        """Generate JWT token for user"""
        secret_key = os.getenv('SECRET_KEY', 'mysecretkey')
        
        payload = {
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
        }
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    
    @staticmethod
    def verify_email(user_id):
        """Mark user email as verified"""
        user = User.query.get(user_id)
        if user:
            user.is_verified = True
            db.session.commit()
            return {'message': 'Email verified successfully'}, 200
        return {'error': 'User not found'}, 404
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404
    
    @staticmethod
    def update_user_profile(user_id, data):
        """Update user profile"""
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Update allowed fields
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 400
            user.username = data['username']
        
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return {'error': 'Email already exists'}, 400
            user.email = data['email']
            user.is_verified = False  # Require re-verification
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return {
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }, 200
