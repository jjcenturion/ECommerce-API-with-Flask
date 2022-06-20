from datetime import datetime

from flask_restful import Resource, reqparse

from models.order_detail import OrderDetailModel
from models.order import OrderModel
from models.product import ProductModel


class Order(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('name_product',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def put(self, datetime_str):
        date_time = datetime.fromisoformat(datetime_str)
        data = Order.parser.parse_args()

        product = ProductModel.find_by_name(data['name_product'])
        current_stock = product.stock - data['quantity']

        if product and data['quantity'] > 0:
            order = OrderModel(date_time)
            order.save_to_db()

            find_order = OrderModel.find_by_datetime(date_time)

            order_detail = OrderDetailModel(data['quantity'], find_order.id, product.id)
            order_detail.save_to_db()

            if current_stock >= 0:
                # Actualiza el stock
                product.stock = current_stock
                product.update_to_db()
                # set_stock = ProductModel(data['name_product'], product.price, current_stock)
                # set_stock.save_to_db()
            else:
                return {'message': 'NO hay stock suficiente para la cantidad requerida'}, 404

            return order_detail.json()
        return {'message': 'Ingrese una cantidad mayor que cero'}, 404

    def delete(self, datetime_str):
        #Elimino una orden y sus detalles, por datetime
        date_time = datetime.fromisoformat(datetime_str)
        data = Order.parser.parse_args()

        find_order = OrderModel.find_by_datetime(date_time)
        order_detail = OrderDetailModel.find_by_order_id(find_order.id)

        if find_order and order_detail:
            find_order.delete_from_db()
            order_detail.delete_from_db()

            # Restaura el stick del producto.
            set_stock = ProductModel.find_by_id(order_detail.product_id)
            reset_stock = set_stock.stock + data['quantity']
            set_stock.stock = reset_stock
            set_stock.update_to_db()
            return {'message': 'product deleted'}
        else:
            return {'message': 'Product not found.'}, 404

    def get(self, datetime_str):
        date_time = datetime.fromisoformat(datetime_str)
        order = OrderModel.find_by_datetime(date_time)
        order_detail = OrderDetailModel.find_by_order_id(order.id)

        if order and order_detail:
            json_order = order.json()
            json_detail = order_detail.json()
            res = {**json_order, **json_detail}
            return res
        return {'message': 'Order not found'}, 404

    def get_total(self, datetime_str):
        date_time = datetime.fromisoformat(datetime_str)
        order = OrderModel.find_by_datetime(date_time)
        order_detail = OrderDetailModel.find_by_order_id(order.id)
        product = ProductModel.find_by_id(order_detail.product_id)

        total = order_detail.quantity * product.price
        return total




class OrderList(Resource):
    def get(self):
        return {'orders': list(map(lambda x: x.json(), OrderModel.query.all()))}




