from Models.UserModel import db, Company, UserCompany, User
import secrets
import string

class CompanyService:
    
    @staticmethod
    def generate_unique_code():
        """Generate a unique company code"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not Company.query.filter_by(unique_code=code).first():
                return code
    
    @staticmethod
    def create_company(name, description, created_by_user_id):
        """Create a new company"""
        unique_code = CompanyService.generate_unique_code()
        
        new_company = Company(
            name=name,
            description=description,
            unique_code=unique_code,
            created_by=created_by_user_id
        )
        
        db.session.add(new_company)
        db.session.flush()  # Get the company ID
        
        # Add creator as admin
        user_company = UserCompany(
            user_id=created_by_user_id,
            company_id=new_company.id,
            role='admin'
        )
        
        db.session.add(user_company)
        db.session.commit()
        
        return {
            'message': 'Company created successfully',
            'company': new_company.to_dict(),
            'unique_code': unique_code
        }, 201
    
    @staticmethod
    def join_company(unique_code, user_id):
        """Join an existing company using unique code"""
        company = Company.query.filter_by(unique_code=unique_code).first()
        
        if not company:
            return {'error': 'Invalid company code'}, 404
        
        # Check if user already belongs to this company
        existing = UserCompany.query.filter_by(
            user_id=user_id,
            company_id=company.id
        ).first()
        
        if existing:
            return {'error': 'Already a member of this company'}, 400
        
        # Add user as employee
        user_company = UserCompany(
            user_id=user_id,
            company_id=company.id,
            role='employee'
        )
        
        db.session.add(user_company)
        db.session.commit()
        
        return {
            'message': 'Successfully joined company',
            'company': company.to_dict()
        }, 200
    
    @staticmethod
    def get_user_companies(user_id):
        """Get all companies a user belongs to"""
        user_companies = UserCompany.query.filter_by(user_id=user_id).all()
        
        companies = []
        for uc in user_companies:
            company_dict = uc.company.to_dict()
            company_dict['role'] = uc.role
            company_dict['joined_at'] = uc.joined_at.isoformat() if uc.joined_at else None
            companies.append(company_dict)
        
        return {'companies': companies}, 200
    
    @staticmethod
    def get_company_by_id(company_id, user_id):
        """Get company details if user has access"""
        # Check access
        user_company = UserCompany.query.filter_by(
            user_id=user_id,
            company_id=company_id
        ).first()
        
        if not user_company:
            return {'error': 'Access denied'}, 403
        
        company = Company.query.get(company_id)
        if not company:
            return {'error': 'Company not found'}, 404
        
        company_dict = company.to_dict()
        company_dict['role'] = user_company.role
        
        return {'company': company_dict}, 200
    
    @staticmethod
    def get_company_employees(company_id, user_id):
        """Get all employees of a company (admin only)"""
        # Check if user is admin
        user_company = UserCompany.query.filter_by(
            user_id=user_id,
            company_id=company_id
        ).first()
        
        if not user_company or user_company.role != 'admin':
            return {'error': 'Admin access required'}, 403
        
        # Get all employees
        user_companies = UserCompany.query.filter_by(company_id=company_id).all()
        
        employees = []
        for uc in user_companies:
            user = User.query.get(uc.user_id)
            if user:
                employee_dict = user.to_dict()
                employee_dict['role'] = uc.role
                employee_dict['joined_at'] = uc.joined_at.isoformat() if uc.joined_at else None
                employees.append(employee_dict)
        
        return {'employees': employees}, 200
    
    @staticmethod
    def update_employee_role(company_id, employee_id, new_role, admin_user_id):
        """Update employee role (admin only)"""
        # Check if requesting user is admin
        admin_company = UserCompany.query.filter_by(
            user_id=admin_user_id,
            company_id=company_id
        ).first()
        
        if not admin_company or admin_company.role != 'admin':
            return {'error': 'Admin access required'}, 403
        
        # Get employee's company relationship
        employee_company = UserCompany.query.filter_by(
            user_id=employee_id,
            company_id=company_id
        ).first()
        
        if not employee_company:
            return {'error': 'Employee not found in company'}, 404
        
        # Don't allow changing creator's role
        company = Company.query.get(company_id)
        if company.created_by == employee_id and new_role != 'admin':
            return {'error': 'Cannot change creator role'}, 400
        
        employee_company.role = new_role
        db.session.commit()
        
        return {'message': 'Employee role updated successfully'}, 200
    
    @staticmethod
    def remove_employee(company_id, employee_id, admin_user_id):
        """Remove employee from company (admin only)"""
        # Check if requesting user is admin
        admin_company = UserCompany.query.filter_by(
            user_id=admin_user_id,
            company_id=company_id
        ).first()
        
        if not admin_company or admin_company.role != 'admin':
            return {'error': 'Admin access required'}, 403
        
        # Don't allow removing creator
        company = Company.query.get(company_id)
        if company.created_by == employee_id:
            return {'error': 'Cannot remove company creator'}, 400
        
        # Get and remove employee
        employee_company = UserCompany.query.filter_by(
            user_id=employee_id,
            company_id=company_id
        ).first()
        
        if not employee_company:
            return {'error': 'Employee not found in company'}, 404
        
        db.session.delete(employee_company)
        db.session.commit()
        
        return {'message': 'Employee removed successfully'}, 200
