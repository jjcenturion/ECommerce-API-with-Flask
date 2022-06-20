from flask import Flask
from flask_restful import Api
from db import db


from resources.product import Product, ProductList, ChangeStock
from resources.order import Order, OrderList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)                 # permite añadir facilmente las rutas del resources


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Product, '/product/<string:name>')
api.add_resource(Order, '/order/<string:datetime_str>')
api.add_resource(OrderList, '/orders')
api.add_resource(ProductList, '/products')
api.add_resource(ChangeStock, '/change_stock/<string:name>')





if __name__ == '__main__':

    db.init_app(app)
    app.run(port=5000, debug=True)