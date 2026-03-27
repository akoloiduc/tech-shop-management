from flask import Flask
from flask_cors import CORS
from . import category
from . import product
from . import supplier
from . import purchase_order
from . import purchase_order_detail
from . import product_variant

def create_app():
    # Khởi tạo Flask app
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(category.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(product_variant.bp)
    app.register_blueprint(supplier.bp)
    app.register_blueprint(purchase_order.bp)
    app.register_blueprint(purchase_order_detail.bp)
    return app