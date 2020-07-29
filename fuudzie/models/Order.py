from mongoengine import *
from datetime import datetime

from fuudzie.models.User import Users

class Orders(Document):
    user = ReferenceField('Users', reverse_delete_rule=CASCADE)
    items = ListField(DynamicField())
    shippingAddress = StringField()
    pickUpTime = StringField()
    paymentId = StringField()
    referenceId = StringField()
    amount = FloatField()
    deliveryFee = FloatField()
    status = StringField(default='paid', choices=('paid', 'not_paid', 'on_route', 'delivered', 'not_delivered','cancelled'))
    createdAt = DateTimeField(default=datetime.utcnow())
    updatedAt = DateTimeField(default=datetime.utcnow())
    v = IntField(db_field='__v')

    def __repr__(self):
        return '<Order for %r>' % (self.user.email)

    def toJson(self):
        return {
            '_id': self.pk,
            'user': self.user,
            'items': self.items,
            'shippingAddress': self.shippingAddress,
            'pickUpTime': self.pickUpTime,
            'paymentId': self.paymentId,
            'referenceId': self.referenceId,
            'amount': self.amount,
            'deliveryFee': self.deliveryFee,
            'status': self.status,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            '__v': self.v,
        }