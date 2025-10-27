from flask import Flask
from flask_cors import CORS
from Config.Config import Config
from Controllers.ProductController import product_bp
from Controllers.AuthController import auth_bp
from Controllers.CompanyController import company_bp
from Models.UserModel import db

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(company_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')

# Root route with app info
@app.route('/')
def home():
    return {
        'message': 'Welcome to Inventory Management API',
        'description': 'A comprehensive inventory management system with multi-tenant support',
        'features': [
            'User authentication with JWT',
            'Company-based inventory management',
            'Role-based access control (Admin/Employee)',
            'Secure API endpoints'
        ],
        'endpoints': {
            'auth': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login',
                'profile': 'GET /api/auth/profile (requires JWT)',
                'update_profile': 'PUT /api/auth/profile (requires JWT)'
            },
            'companies': {
                'create': 'POST /api/companies (requires JWT)',
                'join': 'POST /api/companies/join (requires JWT)',
                'list': 'GET /api/companies (requires JWT)',
                'details': 'GET /api/companies/:id (requires JWT)',
                'employees': 'GET /api/companies/:id/employees (requires JWT, admin only)'
            },
            'products': {
                'list': 'GET /api/companies/:company_id/productos (requires JWT)',
                'get': 'GET /api/companies/:company_id/productos/:id (requires JWT)',
                'create': 'POST /api/companies/:company_id/productos (requires JWT)',
                'update': 'PUT /api/companies/:company_id/productos/:id (requires JWT)',
                'delete': 'DELETE /api/companies/:company_id/productos/:id (requires JWT, admin only)'
            }
        }
    }

if __name__ == '__main__':
    app.run(debug=True)
