from mongoengine import *
from datetime import datetime as dt


class Appsettings(Document):
    _id = StringField()
    transactionPercentage = IntField()
    deliveryPromo = BooleanField()
    setting = BooleanField()
    v = IntField(db_field='__v')

    def __repr__(self):
        return '<Appsetting %r>' % (self.pk)

    def toJson(self):
        return {
            '_id': self._id,
            'transactionPercentage': self.transactionPercentage,
            'deliveryPromo': self.deliveryPromo,
            'setting': self.setting,
            '__v': self.v,
        }
