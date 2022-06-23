from db import db


class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision=2))
    stock = db.Column(db.Integer)

    order_detail = db.relationship('OrderDetailModel', backref='product')

    def __init__(self, name, price, stock):

        self.name = name
        self.price = price
        self.stock = stock

    def json(self):
        return {'name': self.name, 'price': self.price, 'stock': self.stock}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

