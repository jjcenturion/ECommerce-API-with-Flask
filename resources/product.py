from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.product import ProductModel


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('stock',
                        type=int,
                        required=True)

    def put(self, name):
        data = Product.parser.parse_args()

        product = ProductModel.find_by_name(name)

        if product:
            product.price = data['price']
            product.stock = data['stock']
        else:
            product = ProductModel(name, **data)

        product.save_to_db()

        return product.json()

    @jwt_required()
    def delete(self, name):
        product = ProductModel.find_by_name(name)

        if product:
            product.delete_from_db()
            return {'message': 'product deleted'}
        else:
            return {'message': 'Product not found.'}, 404

    @jwt_required()
    def get(self, name):
        product = ProductModel.find_by_name(name)

        if product:
            return product.json()
        return {'message': 'Product not found'}, 404


class ChangeStock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stock',
                        type=int,
                        required=True)

    def put(self, name):
        data = ChangeStock.parser.parse_args()
        product = ProductModel.find_by_name(name)

        if product:
            product.stock = data['stock']
            product.update_to_db()
            return product.json()
        return {'message': 'Stock not updated'}, 404


class ProductList(Resource):
    def get(self):
        return {'products': list(map(lambda x: x.json(), ProductModel.query.all()))}


