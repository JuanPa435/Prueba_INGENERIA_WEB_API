from Models.UserModel import db, Product, UserCompany

class ProductService:
    
    @staticmethod
    def get_all_products(company_id):
        """Get all products for a specific company"""
        return Product.query.filter_by(company_id=company_id).all()

    @staticmethod
    def get_product_by_id(product_id, company_id):
        """Get a product by ID if it belongs to the company"""
        return Product.query.filter_by(id=product_id, company_id=company_id).first()

    @staticmethod
    def create_product(data, company_id):
        """Create a new product for a company"""
        print(data)
        new_product = Product(
            name=data['name'],
            description=data['description'],
            quantity=data['quantity'],
            price=data['price'],
            company_id=company_id
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(product_id, data, company_id):
        """Update a product if it belongs to the company"""
        product = Product.query.filter_by(id=product_id, company_id=company_id).first()
        if product:
            if 'name' in data:
                product.name = data['name']
            if 'description' in data:
                product.description = data['description']
            if 'quantity' in data:
                product.quantity = data['quantity']
            if 'price' in data:
                product.price = data['price']
            db.session.commit()
            return product
        return None

    @staticmethod
    def delete_product(product_id, company_id):
        """Delete a product if it belongs to the company"""
        product = Product.query.filter_by(id=product_id, company_id=company_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
