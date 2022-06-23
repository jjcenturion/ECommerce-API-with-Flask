from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.product import Product, ProductList, ChangeStock
from resources.order import Order, OrderList, OrderTotal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)                      # permite añadir las rutas del resources




jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Product, '/product/<string:name>')
api.add_resource(Order, '/order/<string:datetime_str>')
api.add_resource(OrderList, '/orders')
api.add_resource(ProductList, '/products')
api.add_resource(ChangeStock, '/change_stock/<string:name>')
api.add_resource(OrderTotal, '/total/<string:datetime_str>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)