from mongoengine import *
from datetime import datetime, timedelta

from fuudzie.models.Order import Orders
from fuudzie.models.Vendor import Vendors


class Escrows(Document):
    vendor = ReferenceField('Vendors', reverse_delete_rule=CASCADE)
    order = ReferenceField('Orders', reverse_delete_rule=CASCADE)
    amount= FloatField()
    due_time = DateTimeField(default=datetime.utcnow() + timedelta(hours=8))
    createdAt = DateTimeField(default=datetime.utcnow())
    updatedAt = DateTimeField(default=datetime.utcnow())
    v = IntField(db_field='__v')


    def __repr__(self):
        return '<Escrow %r>' % (self.pk)

    def toJson(self):
        return {
            'vendor': self.vendor,
            'order': self.orders,
            'amount': self.amount,
            'due_time': self.due_time,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }