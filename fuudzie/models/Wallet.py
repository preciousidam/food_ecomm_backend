from mongoengine import *
from datetime import datetime as dt

from fuudzie.models.User import Users

class Wallets(Document):

    user = LazyReferenceField('Users', reverse_delete_rule=CASCADE)
    amount = FloatField()
    paymentRef = StringField(default='')
    createdAt = DateTimeField(default=dt.now())
    updatedAt = DateTimeField(default=dt.now())
    v = IntField(db_field='__v')

    def __repr__(self):
        return '<Wallet %r>' % (self.pk)

    def toJson(self):
        return {
            '_id': self.pk,
            'user': self.user,
            'amount': self.amount,
            'paymentRef': self.paymentRef,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }