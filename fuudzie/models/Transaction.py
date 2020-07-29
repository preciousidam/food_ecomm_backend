from mongoengine import *
from datetime import datetime

from fuudzie.models.User import Users
from fuudzie.models.Wallet import Wallets

class Transactions(Document):
    user = ReferenceField('Users', reverse_delete_rule=CASCADE)
    wallet = ReferenceField('Wallets', reverse_delete_rule=CASCADE)
    amount = FloatField()
    reference = StringField()
    operation = StringField()
    createdAt = DateTimeField(default=datetime.utcnow())
    updatedAt = DateTimeField(default=datetime.utcnow())
    v = IntField(db_field='__v')


    def toJson(self):
        return {
            'user': self.user,
            'wallet': self.wallet,
            'amount': self.amount,
            'reference': self.reference,
            'operation': self.operation,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v
        }