from db import db


class OrderDetailModel(db.Model):
    __tablename__ = 'order_detail'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # order = db.relationship('OrderModel')
    #
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    # product = db.relationship('ProductModel')

    def __init__(self, quantity, order_id, product_id):
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id).first()

    def json(self):
        return {'quantity': self.quantity, 'product_id': self.product_id, 'order_id': self.order_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



