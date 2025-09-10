from flask import Flask
from Config.Config import Config
from Controllers.ProductController import product_bp
from Models.ProductModel import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registrar las rutas
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)
