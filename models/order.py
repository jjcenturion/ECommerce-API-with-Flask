from datetime import datetime
from db import db


class OrderModel(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime)

    order_detail = db.relationship('OrderDetailModel', backref='order')

    def __init__(self, date_time):

        self.date_time = date_time

    @classmethod
    def find_by_datetime(cls, date_time):
        return cls.query.filter_by(date_time=date_time).first()

    def json(self):
        dic = {'date_time': self.date_time.strftime("%d/%m/%Y, %H:%M:%S")}
        return dic

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

